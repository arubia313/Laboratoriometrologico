"""
painel_ia.py — Painel de IA plugavel (Equipe 4 / CamaBier).
Chat que conversa com o usuario e altera o estado do dashboard ao vivo.
Usa um formulario (nao st.chat_input) para funcionar dentro de abas/colunas.

Estado compartilhado (st.session_state["estado"]):
  instrumento : str   -> instrumento em foco
  aba         : str   -> "carta" | "capacidade" | "calibracao" | "incerteza"
  destaque    : str?  -> None | "deriva" | "rastreabilidade" | "anomalias"
"""
import streamlit as st
import sistema_ia as ia

ESTADO_PADRAO = {"instrumento": "TC-201", "aba": "carta", "destaque": None}


def init_estado():
    if "estado" not in st.session_state:
        st.session_state["estado"] = dict(ESTADO_PADRAO)
    if "chat" not in st.session_state:
        st.session_state["chat"] = []


def estado_atual() -> dict:
    init_estado()
    return st.session_state["estado"]


def aplicar_acoes(estado: dict, acoes: dict) -> dict:
    novo = dict(estado)
    if acoes.get("instrumento") in ia.dc.CRITERIOS:
        novo["instrumento"] = acoes["instrumento"]
    if acoes.get("aba") in ia.ABAS_VALIDAS:
        novo["aba"] = acoes["aba"]
    if "destaque" in acoes and acoes["destaque"] in ia.DESTAQUES_VALIDOS:
        novo["destaque"] = acoes["destaque"]
    return novo


def render_chat_ia(titulo: str = "Assistente Metrologico (IA)"):
    init_estado()
    st.markdown(f"**{titulo}**")
    st.caption(f"Modo: {ia._modo().upper()} - pergunte ou comande o dashboard")

    for msg in st.session_state["chat"][-6:]:
        with st.chat_message(msg["role"]):
            st.write(msg["texto"])
            if msg.get("fonte"):
                st.caption(f"Fonte: {msg['fonte']}")

    with st.form("form_ia", clear_on_submit=True):
        pergunta = st.text_input("Comando", label_visibility="collapsed",
                                 placeholder="Ex.: mostre a deriva do TC-201")
        enviar = st.form_submit_button("Enviar", use_container_width=True)

    if enviar and pergunta:
        st.session_state["chat"].append({"role": "user", "texto": pergunta})
        r = ia.interpretar_comando(pergunta, st.session_state["estado"])
        st.session_state["estado"] = aplicar_acoes(st.session_state["estado"], r.get("acoes", {}))
        st.session_state["chat"].append({"role": "assistant",
                                         "texto": r.get("resposta", "(sem resposta)"),
                                         "fonte": r.get("fonte_normativa", "")})
        st.rerun()
