"""
sistema_ia.py — Sistema de apoio metrologico com IA (Equipe 4, CamaBier S.A.)
----------------------------------------------------------------------------
Tres funcionalidades (a 1a obrigatoria pela rubrica):
  1. classificar()    -> diagnostico de nao-conformidade (Ishikawa)
  2. prever_deriva()  -> projecao de deriva e data otima de recalibracao
  3. redigir_laudo()  -> laudo metrologico na estrutura ISO 17025

DOIS MODOS DE EXECUCAO (resolve a dependencia da chave de API):
  - REAL : se a variavel ANTHROPIC_API_KEY existir e o pacote 'anthropic'
           estiver instalado, chama o Claude de verdade.
  - MOCK : caso contrario, usa respostas simuladas (deterministicas) que
           refletem os dados reais. Permite desenvolver e testar SEM chave.
Forcar modo: variavel de ambiente IA_MODO = "real" | "mock".

A chave NUNCA fica no codigo: e lida do ambiente (boa pratica de seguranca).
"""
import os
import json
import data_contract as dc

MODELO = "claude-sonnet-4-6"          # bom equilibrio custo/qualidade
_AQUI = os.path.dirname(__file__)

with open(os.path.join(_AQUI, "system_prompt.txt"), encoding="utf-8") as _f:
    SYSTEM = _f.read()


# --------------------------------------------------------------------------
# Selecao de modo
# --------------------------------------------------------------------------
def _modo():
    forcado = os.environ.get("IA_MODO", "").lower()
    if forcado in ("real", "mock"):
        return forcado
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            import anthropic  # noqa: F401
            return "real"
        except ImportError:
            return "mock"
    return "mock"


def _chamar_real(prompt: str) -> dict:
    """Chama a API Anthropic e devolve o JSON parseado, com tratamento de erro."""
    import anthropic
    client = anthropic.Anthropic()                  # le ANTHROPIC_API_KEY do ambiente
    try:
        msg = client.messages.create(
            model=MODELO, max_tokens=1500, system=SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:                           # rede, auth, rate limit...
        return {"status": "erro_api", "detalhe": str(e)}
    texto = "".join(b.text for b in msg.content if b.type == "text").strip()
    for cerca in ("```json", "```"):
        texto = texto.replace(cerca, "")
    try:
        return json.loads(texto.strip())
    except json.JSONDecodeError:
        return {"status": "saida_nao_json", "bruto": texto[:400]}


def _chamar(prompt: str, mock_fn) -> dict:
    """Roteia para a API real ou para o mock conforme o modo vigente."""
    if _modo() == "real":
        return _chamar_real(prompt)
    return mock_fn()


# --------------------------------------------------------------------------
# Funcionalidade 1 (OBRIGATORIA): Classificador de nao-conformidade
# --------------------------------------------------------------------------
def classificar(instrumento_id: str) -> dict:
    casos = [a for a in dc.anomalias()
             if a["instrumento"] in (instrumento_id, "GERAL")]
    if not casos:
        return {"status": "dado_insuficiente",
                "faltando": [f"nenhuma anomalia registrada para {instrumento_id}"]}

    prompt = f"""TAREFA: Classificador de nao-conformidade (diagrama de Ishikawa).
<dados>{json.dumps(casos, ensure_ascii=False)}</dados>
Gere hipoteses de causa-raiz nas 6 categorias (Maquina, Metodo, Medicao,
Material, MeioAmbiente, MaoDeObra). Schema JSON:
{{"instrumento": str, "ishikawa": {{"<categoria>": [str]}},
  "causa_raiz_provavel": str, "fonte_normativa": str, "confianca": str}}"""

    def mock():
        a = casos[0]
        ishikawa = {
            "Maquina": ["Desgaste/degradacao do elemento sensor"] if a["tipo"] == "deriva" else [],
            "Metodo": ["Intervalo de recalibracao possivelmente longo"],
            "Medicao": ["Padrao de referencia sem rastreabilidade RBC"] if a["tipo"] == "rastreabilidade" else [],
            "Material": [],
            "MeioAmbiente": ["Variacao termica do laboratorio"],
            "MaoDeObra": ["Registro de datas inconsistente"] if a["tipo"] == "registro" else [],
        }
        causa = {"deriva": "degradacao do elemento sensor com o tempo",
                 "rastreabilidade": "uso de padrao nao acreditado na cadeia",
                 "registro": "falha no controle de registros de calibracao"}[a["tipo"]]
        return {"instrumento": instrumento_id,
                "ishikawa": {k: v for k, v in ishikawa.items() if v},
                "causa_raiz_provavel": causa,
                "fonte_normativa": a["norma"], "confianca": "alta",
                "_modo": "mock"}

    return _chamar(prompt, mock)


# --------------------------------------------------------------------------
# Funcionalidade 2: Predicao de deriva de calibracao
# --------------------------------------------------------------------------
def prever_deriva(instrumento_id: str) -> dict:
    df = dc.carregar_dados()
    sub = df[df["instrumento_id"] == instrumento_id]
    if sub.empty:
        return {"status": "dado_insuficiente", "faltando": ["instrumento inexistente"]}
    serie = sub.groupby("n_calibracao")["erro"].mean().round(4)
    crit = dc.CRITERIOS.get(instrumento_id)
    dados = {"erro_medio_por_calibracao": list(serie.values), "criterio": crit}

    prompt = f"""TAREFA: Predicao de deriva de calibracao.
<dados>{json.dumps(dados, ensure_ascii=False)}</dados>
Projete em qual calibracao futura o erro medio ultrapassa o criterio (extrapole
a tendencia) e sugira data otima de recalibracao. Schema JSON:
{{"tendencia": str, "passo_medio_por_calibracao": float,
  "calibracao_estimada_de_falha": int, "recomendacao": str,
  "fonte_normativa": str}}"""

    def mock():
        import numpy as np
        y = serie.values
        passo = float(np.mean(np.diff(y))) if len(y) > 1 else 0.0
        atual = abs(y[-1])
        if passo <= 0:
            est = -1
            rec = "Sem tendencia ascendente; manter intervalo padrao."
        else:
            faltam = (crit - atual) / passo
            est = int(len(y) + max(1, round(faltam)))
            rec = (f"Antecipar recalibracao: criterio +/-{crit} deve ser ultrapassado "
                   f"por volta da calibracao {est}.")
        return {"tendencia": "ascendente" if passo > 0 else "estavel",
                "passo_medio_por_calibracao": round(passo, 4),
                "calibracao_estimada_de_falha": est, "recomendacao": rec,
                "fonte_normativa": "ISO 17025 §6.4; §7.7", "_modo": "mock"}

    return _chamar(prompt, mock)


# --------------------------------------------------------------------------
# Funcionalidade 3: Assistente de redacao de laudo (ISO 17025)
# --------------------------------------------------------------------------
def redigir_laudo(instrumento_id: str) -> dict:
    u = dc.incerteza(instrumento_id)
    if u.get("status") == "dado_insuficiente":
        return u

    prompt = f"""TAREFA: Redigir laudo metrologico (estrutura ISO 17025).
<dados>{json.dumps(u, ensure_ascii=False)}</dados>
Inclua resultado, incerteza expandida com k, condicoes e declaracao de
rastreabilidade. Schema JSON:
{{"resultado": str, "incerteza_expandida": str, "fator_k": int,
  "condicoes": str, "rastreabilidade": str, "fonte_normativa": str}}"""

    def mock():
        return {"resultado": f"{u['valor']} {u['unidade']}",
                "incerteza_expandida": f"+/- {u['U']} {u['unidade']}",
                "fator_k": u["k"],
                "condicoes": "(20 +/- 2) C; UR (55 +/- 10) %",
                "rastreabilidade": "Rastreavel a RBC, salvo ressalva de padrao "
                                   "nao acreditado quando aplicavel.",
                "fonte_normativa": "ISO 17025 §6.5; GUM/JCGM 100:2008",
                "_modo": "mock"}

    return _chamar(prompt, mock)


# --------------------------------------------------------------------------
# Funcionalidade 4 (integracao): Interpretador de comandos do dashboard
# Mapeia linguagem natural -> acoes na interface (instrumento, aba, destaque)
# + uma resposta textual fundamentada. E o que permite "conversar com a IA
# e ela alterar o dashboard ao vivo".
# --------------------------------------------------------------------------
ABAS_VALIDAS = ("carta", "capacidade", "calibracao", "incerteza")
DESTAQUES_VALIDOS = (None, "deriva", "rastreabilidade", "anomalias")


def _resposta_mock(texto, inst, acoes):
    """Gera a resposta textual do mock reaproveitando as 3 funcoes do sistema."""
    dest = acoes.get("destaque")
    if dest == "deriva" and inst:
        p = prever_deriva(inst)
        if p.get("tendencia") == "ascendente":
            return (f"{inst}: deriva {p['tendencia']} (passo medio "
                    f"{p['passo_medio_por_calibracao']}/calibracao). "
                    f"{p['recomendacao']}", p.get("fonte_normativa", ""))
        return f"{inst}: sem deriva relevante.", p.get("fonte_normativa", "")
    if dest == "rastreabilidade" and inst:
        c = classificar(inst)
        return (f"{inst}: {c.get('causa_raiz_provavel', 'verificar rastreabilidade')}.",
                c.get("fonte_normativa", ""))
    if acoes.get("aba") == "incerteza" and inst:
        u = redigir_laudo(inst)
        return (f"{inst}: resultado {u.get('resultado','-')}, incerteza "
                f"{u.get('incerteza_expandida','-')} (k={u.get('fator_k','-')}).",
                u.get("fonte_normativa", ""))
    if acoes.get("destaque") == "anomalias":
        n = len(dc.anomalias())
        return f"{n} anomalias registradas no laboratorio.", "ISO 17025 §7.7"
    if inst:
        return f"Exibindo {inst}.", ""
    return "Comando interpretado.", ""


def interpretar_comando(texto: str, estado: dict = None) -> dict:
    """Recebe o texto do usuario + estado atual do dashboard e devolve:
    {"resposta": str, "acoes": {"instrumento","aba","destaque"}, "fonte_normativa": str}.
    As 'acoes' sao aplicadas pelo painel para alterar a tela ao vivo."""
    estado = dict(estado or {})
    catalogo = {"instrumentos": list(dc.CRITERIOS.keys()),
                "abas": list(ABAS_VALIDAS), "destaques": [d for d in DESTAQUES_VALIDOS if d]}

    prompt = f"""TAREFA: Interpretar comando de dashboard metrologico.
<dados>texto_usuario="{texto}"; estado_atual={json.dumps(estado, ensure_ascii=False)};
opcoes={json.dumps(catalogo, ensure_ascii=False)}</dados>
Traduza o pedido em acoes de interface e uma resposta curta. Schema JSON:
{{"resposta": str, "acoes": {{"instrumento": str, "aba": str, "destaque": str}},
  "fonte_normativa": str}}
Use apenas instrumentos/abas/destaques das opcoes; omita chaves nao mencionadas."""

    def mock():
        t = texto.lower()
        acoes = {}
        for inst in dc.CRITERIOS:
            if inst.lower() in t:
                acoes["instrumento"] = inst
        if any(k in t for k in ("carta", "controle", "deriva", "tend")):
            acoes["aba"] = "carta"
        elif any(k in t for k in ("capacidade", "cpk", "semaforo", "semáforo", "capac")):
            acoes["aba"] = "capacidade"
        elif any(k in t for k in ("calibr", "validade", "vencimento", "rastrea")):
            acoes["aba"] = "calibracao"
        elif any(k in t for k in ("incerteza", "laudo", "tipo a", "tipo b")):
            acoes["aba"] = "incerteza"
        if "deriva" in t or "tend" in t:
            acoes["destaque"] = "deriva"
        elif "rastrea" in t:
            acoes["destaque"] = "rastreabilidade"
        elif any(k in t for k in ("anomal", "problema", "conform", "fora de")):
            acoes["destaque"] = "anomalias"
        inst = acoes.get("instrumento", estado.get("instrumento"))
        resposta, fonte = _resposta_mock(t, inst, acoes)
        return {"resposta": resposta, "acoes": acoes,
                "fonte_normativa": fonte, "_modo": "mock"}

    return _chamar(prompt, mock)


if __name__ == "__main__":
    print(f"[modo de execucao: {_modo().upper()}]\n")
    casos = [("classificar", "TC-201"), ("classificar", "BAL-101"),
             ("prever_deriva", "TC-201"), ("redigir_laudo", "FL-501")]
    for fn, inst in casos:
        print(f">>> {fn}({inst})")
        print(json.dumps(globals()[fn](inst), ensure_ascii=False, indent=2), "\n")
