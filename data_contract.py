"""
data_contract.py — ADAPTADOR sobre o dados.py da Equipe 4 (dashboard).
--------------------------------------------------------------------
Objetivo da integracao: a IA precisa citar EXATAMENTE os mesmos numeros
que o dashboard exibe. Em vez de recalcular, este modulo embrulha o
dados.py (fonte unica do dashboard) e expoe a interface que sistema_ia.py
espera. Assim, dashboard e IA falam a mesma verdade.

Mapa:
  CRITERIOS()        <- INSTRUMENTOS.Criterio_T
  carregar_dados()   <- DERIVA (erro medio por calibracao)
  tabela_capacidade()<- CAPACIDADE
  anomalias()        <- INSTRUMENTOS/DERIVA (achados)
  incerteza(id)      <- INCERTEZA (mesmo balanco do dashboard)
"""
import math
import pandas as pd
import dados as d

# Criterio de aceitacao por instrumento (exclui o padrao PAD-MASS-01)
CRITERIOS = {r["ID"]: r["Criterio_T"]
             for _, r in d.INSTRUMENTOS.iterrows()
             if r["Criterio_T"] is not None}


def carregar_dados() -> pd.DataFrame:
    """Serie de erro medio por calibracao (a partir da tabela DERIVA)."""
    df = d.DERIVA.rename(columns={"ID": "instrumento_id", "Cal": "n_calibracao",
                                  "Erro_medio": "erro"}).copy()
    df["criterio_aceitacao"] = df["instrumento_id"].map(CRITERIOS)
    return df


def tabela_capacidade() -> pd.DataFrame:
    return d.CAPACIDADE.rename(columns={"ID": "instrumento_id"})[
        ["instrumento_id", "Cp", "Cpk", "Pp", "Ppk"]].copy()


def anomalias() -> list:
    """As quatro nao-conformidades, com evidencia vinda dos dados do dashboard."""
    out = []
    # (1) Deriva TC-201
    serie = d.DERIVA[d.DERIVA["ID"] == "TC-201"]["Erro_medio"].tolist()
    out.append({"instrumento": "TC-201", "tipo": "deriva", "severidade": "alta",
                "descricao": f"Erro medio ascendente de {serie[0]:+.4f} a {serie[-1]:+.4f} C; "
                             "Cpk da Cal.5 = 0,68 (VERMELHO); projecao ultrapassa +/-0,50 C na Cal.6",
                "norma": "ISO 17025 §6.4; §7.7",
                "evidencia": f"erro_medio_por_calibracao={[round(x,4) for x in serie]}"})
    # (2) Rastreabilidade PAD-MASS-01 -> BAL-101
    out.append({"instrumento": "BAL-101", "tipo": "rastreabilidade", "severidade": "alta",
                "descricao": "Padrao PAD-MASS-01 sem acreditacao RBC usado na calibracao da "
                             "BAL-101; Cpk=4,89 (verde) mas calibracao metrologicamente invalida",
                "norma": "ISO 17025 §6.5",
                "evidencia": "PAD-MASS-01.Alerta_rastr=True"})
    # (3) Deriva leve TRQ-801
    st = d.DERIVA[d.DERIVA["ID"] == "TRQ-801"]["Erro_medio"].tolist()
    out.append({"instrumento": "TRQ-801", "tipo": "deriva", "severidade": "baixa",
                "descricao": f"Tendencia leve ascendente ({st[0]:+.4f} a {st[-1]:+.4f} N.m), "
                             "dentro do criterio +/-0,050",
                "norma": "ISO 17025 §6.4; §7.7",
                "evidencia": f"erro_medio_por_calibracao={[round(x,4) for x in st]}"})
    # (4) Inconsistencia documental
    out.append({"instrumento": "GERAL", "tipo": "registro", "severidade": "media",
                "descricao": "Certificados declaram 15/04/2026; historico registra mar/2026",
                "norma": "ISO 17025 §7.5; §8.4",
                "evidencia": "certificado PDF x tabela VALIDADE"})
    return out


def incerteza(instrumento_id: str) -> dict:
    """Balanco de incerteza — os MESMOS numeros do dashboard (tabela INCERTEZA)."""
    linha = d.INCERTEZA[d.INCERTEZA["ID"] == instrumento_id]
    if linha.empty:
        return {"status": "dado_insuficiente", "faltando": ["instrumento sem balanco"]}
    row = linha.iloc[0]
    info = d.INSTRUMENTOS[d.INSTRUMENTOS["ID"] == instrumento_id].iloc[0]
    uA = row["s_cal5"] / math.sqrt(10)
    uB1 = row["U_pad"] / 2
    uB2 = (row["Resolucao"] / 2) / math.sqrt(3)
    return {
        "instrumento_id": instrumento_id,
        "valor": float(info["Nominal"]), "unidade": row["Unid"],
        "U": float(round(row["U_k2"], 4)), "k": 2, "u_c": float(round(row["uc"], 5)),
        "nu_eff": int(row["nu_eff"]), "norma": "GUM/JCGM 100:2008",
        "fontes": [
            {"fonte": "Repetibilidade (10 medicoes)", "tipo": "A",
             "distribuicao": "normal", "divisor": "raiz(10)", "u_i": float(round(uA, 5))},
            {"fonte": "Certificado do padrao", "tipo": "B",
             "distribuicao": "normal", "divisor": "k=2", "u_i": float(round(uB1, 5))},
            {"fonte": "Resolucao do instrumento", "tipo": "B",
             "distribuicao": "retangular", "divisor": "raiz(3)", "u_i": float(round(uB2, 5))},
        ]}
