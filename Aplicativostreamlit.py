import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import date
from io import BytesIO
import dados as d

# ── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Metrológica — CamaBier S.A.",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta de cores ──────────────────────────────────────────────────────────
COR_VERDE   = "#00B050"
COR_AMARELO = "#FF9900"
COR_VERMELHO= "#C00000"
COR_AZUL    = "#1F4E79"
COR_CINZA   = "#6B6B6B"

def cor_semaforo(val):
    if val == "VERDE":   return COR_VERDE
    if val == "AMARELO": return COR_AMARELO
    return COR_VERMELHO

# ── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #0D1B2A; }
[data-testid="stSidebar"] * { color: #E0E0E0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #A0B4C8 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-card { background:#F7F9FC; border:1px solid #E2E8F0; border-radius:10px; padding:1rem 1.25rem; }
.metric-card h4 { font-size:0.75rem; color:#64748B; margin:0 0 4px 0; text-transform:uppercase; letter-spacing:0.04em; }
.metric-card .val { font-size:1.9rem; font-weight:600; margin:0; line-height:1.1; }
.metric-card .sub { font-size:0.72rem; color:#94A3B8; margin:4px 0 0 0; }
.alerta-danger { background:#FEF2F2; border-left:4px solid #C00000; border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0; font-size:0.82rem; color:#7F1D1D; }
.alerta-warn { background:#FFFBEB; border-left:4px solid #FF9900; border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0; font-size:0.82rem; color:#78350F; }
.norma-ref { font-size:0.70rem; color:#94A3B8; margin-top:6px; border-top:1px solid #E2E8F0; padding-top:6px; }
.page-title { font-size:1.05rem; font-weight:600; color:#1F4E79; margin-bottom:0; }
.section-label { font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:#94A3B8; margin:0; }
div[data-testid="stTabs"] button { font-size:0.82rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar — Filtros (Req. 5) ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍺 CamaBier S.A.")
    st.markdown("**Dashboard Metrológica — ENG207**")
    st.markdown("---")
    st.markdown("### Filtros")

    etapas_disp = {"Todas": None, "1 — Brassagem": 1, "2 — Envase": 2, "3 — Inspeção": 3}
    etapa_sel = st.selectbox("Etapa do processo", list(etapas_disp.keys()))
    etapa_val = etapas_disp[etapa_sel]

    inst_disp = sorted(d.INSTRUMENTOS[d.INSTRUMENTOS["Etapa"] != 0]["ID"].tolist())
    inst_sel = st.multiselect("Instrumento(s)", inst_disp, default=inst_disp)

    cal_sel = st.selectbox("Calibração", [1, 2, 3, 4, 5], index=4,
                           format_func=lambda x: f"Calibração {x}")

    st.markdown("---")
    st.markdown("### Referência de datas")
    st.markdown(f"**Hoje:** {d.TODAY.strftime('%d/%m/%Y')}")
    st.markdown("**Dataset:** Cal.5 — mar/2026")
    st.markdown("---")
    st.caption("ENG207 · Metrologia Industrial · UFBA · 2026.1")

# ── Filtragem dos dados ──────────────────────────────────────────────────────
df_inst = d.INSTRUMENTOS[d.INSTRUMENTOS["Etapa"] != 0].copy()
if etapa_val:
    df_inst = df_inst[df_inst["Etapa"] == etapa_val]
df_inst = df_inst[df_inst["ID"].isin(inst_sel)]

df_cap = d.CAPACIDADE[d.CAPACIDADE["ID"].isin(df_inst["ID"])]
df_der = d.DERIVA[d.DERIVA["ID"].isin(df_inst["ID"])]
df_carta = d.CARTAS[d.CARTAS["ID"].isin(df_inst["ID"])]
df_val = d.VALIDADE[d.VALIDADE["ID"].isin(df_inst["ID"].tolist() + ["PAD-MASS-01"])]
df_inc = d.INCERTEZA[d.INCERTEZA["ID"].isin(df_inst["ID"])]
df_msa = d.MSA[d.MSA["ID"].isin(df_inst["ID"])]

# ── Cabeçalho ────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<p class="page-title">📊 Dashboard Metrológica — Laboratório CamaBier S.A.</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Sistema metrológico integrado · 12 instrumentos · 5 calibrações · 600 registros</p>', unsafe_allow_html=True)
with col_h2:
    # Req. 6 — Exportação PDF (via download do HTML da página)
    st.markdown("**Exportar relatório**")
    if st.button("⬇ Download PDF", use_container_width=True, help="Exporta um relatório PDF com todos os painéis visíveis"):
        try:
           if st.button("⬇ Download PDF", use_container_width=True, help="Exporta um relatório PDF com todos os painéis visíveis"):
        try:
            from fpdf import FPDF
            import math
            pdf = FPDF()
            pdf.add_page()
            
            # --- Cabeçalho do Relatório ---
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "Dashboard Metrologica - CamaBier S.A.", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, "ENG207 - Metrologia Industrial - UFBA - Equipe 4", ln=True)
            pdf.cell(0, 6, f"Data de emissao: {d.TODAY.strftime('%d/%m/%Y')}", ln=True)
            pdf.cell(0, 6, f"Filtro aplicado: Etapa: {etapa_sel} | Calibracao Selecionada: {cal_sel}", ln=True)
            pdf.ln(5)
            
            # --- Seção 1: Capacidade (Dados Filtrados) ---
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, f"1. Resumo de Capacidade (Calibracao {cal_sel})", ln=True)
            pdf.set_font("Helvetica", "", 9)
            
            # Buscando os mesmos dados da aba 2 (Filtrados)
            der_cal_pdf = d.DERIVA[d.DERIVA["Cal"] == cal_sel].copy()
            der_cal_pdf = der_cal_pdf[der_cal_pdf["ID"].isin(df_inst["ID"])]
            der_cal_pdf = der_cal_pdf.merge(d.CAPACIDADE[["ID","Cp","Pp","Ppk"]], on="ID", how="left")
            
            for _, row in der_cal_pdf.iterrows():
                cp_val = f"{row['Cp']:.2f}" if pd.notna(row.get('Cp')) and row['Cp'] is not None else "—"
                pdf.cell(0, 6, f"  {row['ID']}: Cp = {cp_val} | Cpk = {row['Cpk']:.2f} [{row['Semaforo']}]", ln=True)
            pdf.ln(4)
            
            # --- Seção 2: Validade de Calibração (Dados Filtrados) ---
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, "2. Status de Validade de Calibracao", ln=True)
            pdf.set_font("Helvetica", "", 9)
            for _, row in df_val.iterrows():
                prox = row["proxima_cal"].strftime("%d/%m/%Y")
                pdf.cell(0, 6, f"  {row['ID']}: proxima calibrao em {prox} | Dias rest.: {int(row['dias_restantes'])} [{row['status']}]", ln=True)
            pdf.ln(4)
            
            # --- Seção 3: Incerteza Expandida Dinâmica ---
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, "3. Balanco de Incerteza Expandida U (k=2)", ln=True)
            pdf.set_font("Helvetica", "", 9)
            df_inc_filt = d.INCERTEZA[d.INCERTEZA["ID"].isin(df_inst["ID"])]
            for _, row_i in df_inc_filt.iterrows():
                uA = row_i["s_cal5"] / math.sqrt(10)
                uB1 = row_i["U_pad"] / 2
                uB2 = (row_i["Resolucao"] / 2) / math.sqrt(3)
                uc = math.sqrt(uA**2 + uB1**2 + uB2**2)
                U = 2 * uc
                pdf.cell(0, 6, f"  {row_i['ID']}: uA={uA:.4f} | uB_pad={uB1:.4f} | uc={uc:.4f} | U(k=2)={U:.4f} {row_i['Unid']}", ln=True)
            pdf.ln(4)
            
            # --- Seção 4: Repetibilidade MSA Dinâmica ---
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, "4. Repetibilidade - Estudo MSA (Variacao do Equipamento)", ln=True)
            pdf.set_font("Helvetica", "", 9)
            df_msa_filt = d.MSA[d.MSA["ID"].isin(df_inst["ID"])]
            for _, row_m in df_msa_filt.iterrows():
                pdf.cell(0, 6, f"  {row_m['ID']}: EV={row_m['EV']:.5f} | Razao P/T={row_m['PT_ratio']*100:.1f}%", ln=True)
            pdf.ln(5)
            
            # --- Seção 5: Anomalias ---
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, "5. Anomalias e Analises Identificadas", ln=True)
            pdf.set_font("Helvetica", "", 9)
            anomalias = [
                "ANOMALIA 1 - TC-201: Deriva critica. Cpk caiu de 3,44 para 0,68 (VERMELHO). Vies crescente.",
                "ANOMALIA 2 - BAL-101/PAD-MASS-01: Rastreabilidade invalida. Viola ISO 17025 $6.5.",
                "ANOMALIA 3 - TRQ-801: Deriva leve preventiva. Monotonica, dentro de +-T.",
                "ANOMALIA 4 - Datas: Certificados PDF vs CSV. Divergencia nas datas de registros. Viola ISO 17025 $7.5.",
            ]
            for a in anomalias:
                pdf.multi_cell(180, 6, f" * {a}")
                
            pdf_bytes = pdf.output()
            st.download_button("📄 Salvar PDF", data=bytes(pdf_bytes),
                               file_name="relatorio_metrologico_camabier.pdf",
                               mime="application/pdf", use_container_width=True)
        except ImportError:
            st.error("Instale fpdf2: pip install fpdf2")
                               file_name="relatorio_metrologico_camabier.pdf",
                               mime="application/pdf", use_container_width=True)
        except ImportError:
            st.error("Instale fpdf2: pip install fpdf2")

st.markdown("---")

# ── KPIs ─────────────────────────────────────────────────────────────────────
n_inst = len(df_inst)
der5 = d.DERIVA[d.DERIVA["Cal"] == cal_sel]
n_verde   = len(der5[der5["Semaforo"] == "VERDE"])
n_verm    = len(der5[der5["Semaforo"] == "VERMELHO"])
n_vence   = len(d.VALIDADE[d.VALIDADE["dias_restantes"].between(0, 90)])
n_vencido = len(d.VALIDADE[d.VALIDADE["dias_restantes"] < 0])

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f'<div class="metric-card"><h4>Instrumentos</h4><p class="val" style="color:{COR_AZUL}">{n_inst}</p><p class="sub">monitorados</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="metric-card"><h4>Capazes · Cal.{cal_sel}</h4><p class="val" style="color:{COR_VERDE}">{n_verde}</p><p class="sub">Cpk ≥ 1,33</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="metric-card"><h4>Críticos · Cal.{cal_sel}</h4><p class="val" style="color:{COR_VERMELHO}">{n_verm}</p><p class="sub">Cpk &lt; 1,00</p></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="metric-card"><h4>Vencem em 90 dias</h4><p class="val" style="color:{COR_AMARELO}">{n_vence}</p><p class="sub">próximas calibrações</p></div>', unsafe_allow_html=True)
with k5:
    cor_v = COR_VERMELHO if n_vencido > 0 else COR_VERDE
    st.markdown(f'<div class="metric-card"><h4>Vencidos</h4><p class="val" style="color:{cor_v}">{n_vencido}</p><p class="sub">sem calibração válida</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Abas ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Cartas de controle",
    "🚦 Semáforo Cp/Cpk",
    "📅 Status de calibração",
    "📐 Incerteza expandida",
    "🔬 Repetibilidade MSA",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Cartas de Controle X̄-R (Req. 1)
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### Carta de controle X̄ — erro médio por calibração")
    st.caption("Limites calculados dos próprios dados. Regras Western Electric aplicadas — ponto vermelho = violação.")

    ids_carta = df_carta["ID"].unique().tolist() if len(df_carta) > 0 else []
    if not ids_carta:
        st.info("Nenhum instrumento selecionado com dados de carta de controle.")
    else:
        inst_carta = st.selectbox("Instrumento", ids_carta, key="carta_inst")
        dc = df_carta[df_carta["ID"] == inst_carta].sort_values("Cal")
        info_inst = d.INSTRUMENTOS[d.INSTRUMENTOS["ID"] == inst_carta].iloc[0]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            subplot_titles=("Carta X̄ — erro médio", "Carta R — amplitude"),
                            vertical_spacing=0.12)

        cals = dc["Cal"].tolist()

        # Cores dos pontos — WE Regra 1: fora de LSC ou LIC
        cores_x = []
        for _, row in dc.iterrows():
            if row["xbar"] > row["LSC"] or row["xbar"] < row["LIC"]:
                cores_x.append(COR_VERMELHO)
            else:
                cores_x.append(COR_AZUL)

        fig.add_trace(go.Scatter(x=cals, y=dc["xbar"], mode="lines+markers",
            marker=dict(color=cores_x, size=9, line=dict(width=1.5, color="white")),
            line=dict(color=COR_AZUL, width=1.5), name="X̄"), row=1, col=1)

        for col_nome, cor, dash, nome in [
            ("LSC", COR_VERMELHO, "dash", "LSC"),
            ("LC",  COR_CINZA,   "dot",  "LC"),
            ("LIC", COR_VERDE,   "dash", "LIC"),
        ]:
            val = dc[col_nome].iloc[0]
            fig.add_hline(y=val, line_color=cor, line_dash=dash, line_width=1.2,
                          annotation_text=f"{nome}={val:.4f}", annotation_position="right",
                          annotation_font_size=10, row=1, col=1)

        # Critério ±T
        t = info_inst["Criterio_T"]
        fig.add_hline(y=t, line_color="#9CA3AF", line_dash="longdash", line_width=0.8,
                      annotation_text=f"+T={t}", annotation_position="right",
                      annotation_font_size=9, row=1, col=1)
        fig.add_hline(y=-t, line_color="#9CA3AF", line_dash="longdash", line_width=0.8,
                      annotation_text=f"−T={t}", annotation_position="right",
                      annotation_font_size=9, row=1, col=1)

        # Carta R
        cores_r = []
        for _, row in dc.iterrows():
            if row["R"] > row["LSC_R"]:
                cores_r.append(COR_VERMELHO)
            else:
                cores_r.append(COR_CINZA)

        fig.add_trace(go.Bar(x=cals, y=dc["R"], marker_color=cores_r,
                             name="R", opacity=0.75), row=2, col=1)
        fig.add_hline(y=dc["LSC_R"].iloc[0], line_color=COR_VERMELHO, line_dash="dash",
                      line_width=1, annotation_text="LSC_R",
                      annotation_font_size=9, row=2, col=1)
        fig.add_hline(y=dc["Rbar"].iloc[0], line_color=COR_CINZA, line_dash="dot",
                      line_width=1, annotation_text="R̄",
                      annotation_font_size=9, row=2, col=1)

        fig.update_layout(height=450, showlegend=False,
                          plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(l=10, r=120, t=40, b=10),
                          xaxis2=dict(title="Calibração", tickmode="array",
                                      tickvals=cals, ticktext=[f"Cal.{c}" for c in cals]))
        fig.update_yaxes(gridcolor="#F1F5F9", gridwidth=0.5)
        st.plotly_chart(fig, use_container_width=True)

        # Derivação monotônica TC-201
        if inst_carta == "TC-201":
            st.markdown('<div class="alerta-danger">⚠ <strong>WE Regra 1 — Cal.5 FORA DE CONTROLE:</strong> X̄ = +0,309 °C acima do LSC. Deriva monotônica confirmada (R²=0,994). Causa: envelhecimento da junção do termopar — viés crescente, repetibilidade preservada. <em>Montgomery SQC cap.5; GUM §4.2 Tipo A</em></div>', unsafe_allow_html=True)
        if inst_carta == "TRQ-801":
            st.markdown('<div class="alerta-warn">⚠ <strong>Tendência leve monotônica:</strong> Erro médio de −0,0035 → +0,0040 N·m. Não crítica, mas justifica monitoramento preventivo. <em>AIAG MSA 4ª ed.</em></div>', unsafe_allow_html=True)

        st.markdown(f'<p class="norma-ref">📚 Norma: {info_inst["Norma"]} · Montgomery SQC cap.5 (Western Electric) · AIAG MSA 4ª ed.</p>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Semáforo Cp/Cpk/Pp/Ppk (Req. 2)
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### Índices de capacidade — Cal. " + str(cal_sel))
    st.caption("Verde ≥ 1,33 · Amarelo 1,00–1,33 · Vermelho < 1,00 — AIAG MSA 4ª ed.")

    # Cpk por calibração (deriva)
    der_cal = d.DERIVA[d.DERIVA["Cal"] == cal_sel].copy()
    der_cal = der_cal[der_cal["ID"].isin(df_inst["ID"])]
    der_cal = der_cal.merge(d.CAPACIDADE[["ID","Cp","Pp","Ppk"]], on="ID", how="left")

    def badge(sem):
        if sem == "VERDE":    return "🟢"
        if sem == "AMARELO":  return "🟡"
        return "🔴"

    # Gráfico de barras Cpk
    cores_bar = [cor_semaforo(s) for s in der_cal["Semaforo"]]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=der_cal["ID"], y=der_cal["Cpk"],
        marker_color=cores_bar,
        text=[f"{v:.2f}" for v in der_cal["Cpk"]],
        textposition="outside", textfont_size=11,
        name="Cpk"
    ))
    fig2.add_hline(y=1.33, line_color=COR_VERDE, line_dash="dash", line_width=1.5,
                   annotation_text="≥1,33 (VERDE)", annotation_font_color=COR_VERDE,
                   annotation_position="right", annotation_font_size=10)
    fig2.add_hline(y=1.0, line_color=COR_AMARELO, line_dash="dash", line_width=1.5,
                   annotation_text="≥1,00 (AMARELO)", annotation_font_color=COR_AMARELO,
                   annotation_position="right", annotation_font_size=10)
    fig2.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(l=10, r=120, t=30, b=10),
                       yaxis=dict(title="Cpk", gridcolor="#F1F5F9"),
                       xaxis=dict(title=""))
    st.plotly_chart(fig2, use_container_width=True)

    # Tabela completa
    st.markdown("##### Tabela Cp / Cpk / Pp / Ppk")
    rows_tbl = []
    for _, row in der_cal.iterrows():
        inst_info = d.INSTRUMENTOS[d.INSTRUMENTOS["ID"] == row["ID"]].iloc[0]
        rows_tbl.append({
            "Instrumento": row["ID"],
            "Grandeza": inst_info["Grandeza"],
            "Cp": f'{row["Cp"]:.2f}' if pd.notna(row.get("Cp")) and row["Cp"] is not None else "—",
            "Cpk": f'{row["Cpk"]:.2f}',
            "Pp": f'{row["Pp"]:.2f}' if pd.notna(row.get("Pp")) else "—",
            "Ppk": f'{row["Ppk"]:.2f}' if pd.notna(row.get("Ppk")) else "—",
            "Semáforo": badge(row["Semaforo"]) + " " + row["Semaforo"],
            "Norma": inst_info["Norma"],
        })
    st.dataframe(pd.DataFrame(rows_tbl), use_container_width=True, hide_index=True)

    # Alerta BAL-101
    st.markdown('<div class="alerta-warn">⚠ <strong>BAL-101:</strong> Cpk = 4,89 (VERDE estatístico), mas calibração metrologicamente <strong>inválida</strong> — padrão PAD-MASS-01 sem rastreabilidade RBC. Capacidade boa ≠ validade metrológica. <em>ISO/IEC 17025:2017 §6.5</em></div>', unsafe_allow_html=True)
    st.markdown('<p class="norma-ref">📚 Regras: AIAG MSA 4ª ed. · Montgomery SQC · ISO 5725</p>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Status de calibração (Req. 3)
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### Status de validade — próximas calibrações")
    st.caption(f"Referência: {d.TODAY.strftime('%d/%m/%Y')} · Prazos fundamentados em norma")

    st.markdown('<div class="alerta-danger">🚫 <strong>ANOMALIA 2 — BAL-101 / PAD-MASS-01:</strong> Rastreabilidade metrológica inválida. O padrão PAD-MASS-01 é de fornecedor não acreditado (rbc_acreditado = False). A calibração da BAL-101 é metrologicamente inválida mesmo com Cpk = 4,89. <em>ISO/IEC 17025:2017 §6.5</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="alerta-warn">📋 <strong>ANOMALIA 4 — Inconsistência documental:</strong> Certificados PDF declaram calibração em 15/04/2026; histórico CSV mostra calibrações reais em mar/2026. Datas divergentes. <em>ISO 17025:2017 §7.5 e §8.4 — controle de registros</em></div>', unsafe_allow_html=True)

    df_v = d.VALIDADE.copy()

    def cor_status(s):
        if s in ("RECALIBRAR URGENTE", "VENCIDO", "SEM RASTREABILIDADE"): return COR_VERMELHO
        if s == "VENCE EM BREVE": return COR_AMARELO
        return COR_VERDE

    # Gráfico de barras — dias restantes
    df_v_plot = df_v[df_v["ID"] != "PAD-MASS-01"].copy()
    cores_dias = [cor_status(s) for s in df_v_plot["status"]]
    fig3 = go.Figure(go.Bar(
        y=df_v_plot["ID"],
        x=df_v_plot["dias_restantes"],
        orientation="h",
        marker_color=cores_dias,
        text=[f'{int(v)} dias' if v >= 0 else f'{int(v)} dias (vencido)' for v in df_v_plot["dias_restantes"]],
        textposition="outside",
        textfont_size=10,
    ))
    fig3.add_vline(x=0, line_color=COR_VERMELHO, line_width=1.5)
    fig3.add_vline(x=60, line_color=COR_AMARELO, line_dash="dash", line_width=1,
                   annotation_text="60 dias", annotation_font_size=9)
    fig3.update_layout(height=330, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(l=10, r=80, t=20, b=10),
                       xaxis=dict(title="Dias até próxima calibração", gridcolor="#F1F5F9"),
                       yaxis=dict(title=""))
    st.plotly_chart(fig3, use_container_width=True)

    # Tabela detalhada
    tbl_val = df_v[["ID","prazo","ultima_cal","proxima_cal","dias_restantes","status","norma"]].copy()
    tbl_val.columns = ["Instrumento","Prazo (m)","Última cal.","Próxima cal.","Dias rest.","Status","Fundamento normativo"]
    tbl_val["Última cal."]  = tbl_val["Última cal."].apply(lambda x: x.strftime("%d/%m/%Y"))
    tbl_val["Próxima cal."] = tbl_val["Próxima cal."].apply(lambda x: x.strftime("%d/%m/%Y"))

    def highlight_status(row):
        s = row["Status"]
        if s in ("RECALIBRAR URGENTE","VENCIDO","SEM RASTREABILIDADE"):
            return ["background-color: #FEF2F2"] * len(row)
        if s == "VENCE EM BREVE":
            return ["background-color: #FFFBEB"] * len(row)
        return [""] * len(row)

    st.dataframe(tbl_val.style.apply(highlight_status, axis=1),
                 use_container_width=True, hide_index=True)
    st.markdown('<p class="norma-ref">📚 Prazos: ISO 17025 §6.4.7 · ILAC-G24:2022 · Portaria INMETRO 248/2008 · OIML D10 · AIAG MSA 4ª ed.</p>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Incerteza Expandida U (k=2) (Req. 4)
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("#### Incerteza expandida U (k = 2) — balanço por instrumento")
    st.caption("u_A = s/√10 (Tipo A) · u_pad = U_pad/2 (Tipo B normal) · u_res = (res/2)/√3 (Tipo B retangular) · u_c = √(Σu²) · U = 2·u_c — GUM/JCGM 100:2008")

    inst_inc = st.selectbox("Instrumento", df_inc["ID"].tolist(), key="inc_inst")
    row_i = df_inc[df_inc["ID"] == inst_inc].iloc[0]
    info_i = d.INSTRUMENTOS[d.INSTRUMENTOS["ID"] == inst_inc].iloc[0]

    import math
    uA  = row_i["s_cal5"] / math.sqrt(10)
    uB1 = row_i["U_pad"] / 2
    uB2 = (row_i["Resolucao"] / 2) / math.sqrt(3)
    uc  = math.sqrt(uA**2 + uB1**2 + uB2**2)
    U   = 2 * uc

    ci1, ci2, ci3, ci4 = st.columns(4)
    with ci1:
        st.markdown(f'<div class="metric-card"><h4>u_A (Tipo A)</h4><p class="val" style="color:{COR_AZUL};font-size:1.4rem">{uA:.5f}</p><p class="sub">{row_i["Unid"]}</p></div>', unsafe_allow_html=True)
    with ci2:
        st.markdown(f'<div class="metric-card"><h4>u_B padrão (Tipo B)</h4><p class="val" style="color:{COR_AZUL};font-size:1.4rem">{uB1:.5f}</p><p class="sub">{row_i["Unid"]}</p></div>', unsafe_allow_html=True)
    with ci3:
        st.markdown(f'<div class="metric-card"><h4>u_c combinada</h4><p class="val" style="color:{COR_AZUL};font-size:1.4rem">{uc:.5f}</p><p class="sub">{row_i["Unid"]}</p></div>', unsafe_allow_html=True)
    with ci4:
        cor_u = COR_AZUL
        st.markdown(f'<div class="metric-card"><h4>U expandida (k=2)</h4><p class="val" style="color:{cor_u};font-size:1.4rem">{U:.5f}</p><p class="sub">{row_i["Unid"]}</p></div>', unsafe_allow_html=True)

    st.markdown("")

    # Tabela de balanço
    st.markdown("##### Tabela de balanço de incerteza")
    bal = pd.DataFrame([
        {"Fonte": "Repetibilidade (s/√n)", "Tipo":"A","Distribuição":"Normal",
         "Valor÷divisor": f"{row_i['s_cal5']:.5f} / √10", "ν": 9,
         "u_i": f"{uA:.6f}", "u_i²": f"{uA**2:.8f}"},
        {"Fonte": "Padrão de referência", "Tipo":"B","Distribuição":"Normal",
         "Valor÷divisor": f"{row_i['U_pad']:.5f} / 2", "ν": "∞",
         "u_i": f"{uB1:.6f}", "u_i²": f"{uB1**2:.8f}"},
        {"Fonte": "Resolução", "Tipo":"B","Distribuição":"Retangular",
         "Valor÷divisor": f"({row_i['Resolucao']}/2) / √3", "ν": "∞",
         "u_i": f"{uB2:.6f}", "u_i²": f"{uB2**2:.8f}"},
        {"Fonte": "u_c combinada", "Tipo":"—","Distribuição":"—",
         "Valor÷divisor": f"ν_eff = {row_i['nu_eff']:.0f}", "ν": "—",
         "u_i": f"{uc:.6f}", "u_i²": "—"},
        {"Fonte": "U expandida (k=2)", "Tipo":"—","Distribuição":"—",
         "Valor÷divisor": "k = 2 (~95%)", "ν": "—",
         "u_i": f"{U:.6f}", "u_i²": "—"},
    ])
    st.dataframe(bal, use_container_width=True, hide_index=True)

    # Conformidade
    erro_abs = abs(row_i["Erro_med"])
    banda = erro_abs + U
    conforme = banda <= row_i["T"]
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.metric("|erro médio|", f"{erro_abs:.5f} {row_i['Unid']}")
    with col_c2:
        st.metric("|erro| + U", f"{banda:.5f} {row_i['Unid']}")
    with col_c3:
        st.metric("Critério ±T", f"{row_i['T']:.5f} {row_i['Unid']}")

    if conforme:
        st.success(f"✅ CONFORME — |erro| + U = {banda:.5f} ≤ T = {row_i['T']:.5f} {row_i['Unid']} · ILAC-G8:2019")
    else:
        st.error(f"❌ NÃO CONFORME — |erro| + U = {banda:.5f} > T = {row_i['T']:.5f} {row_i['Unid']}")

    if inst_inc == "TC-201":
        st.markdown('<div class="alerta-danger">⚠ <strong>TC-201 — Projeção de deriva:</strong> Mesmo CONFORME no critério estático, a tendência monotônica projeta ruptura de ±T na Cal.6. u_deriva adicional = 0,022 °C. Recalibração urgente indicada. <em>GUM/JCGM 100:2008 §4.3; ISO 17025 §6.4.7</em></div>', unsafe_allow_html=True)

    # Gráfico todos os instrumentos
    st.markdown("##### Comparação — U (k=2) vs critério ±T")
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=df_inc["ID"], y=df_inc["U_k2"],
                          name="U expandida (k=2)", marker_color=COR_AZUL, opacity=0.8))
    fig4.add_trace(go.Scatter(x=df_inc["ID"], y=df_inc["T"],
                              mode="markers", marker=dict(symbol="line-ew", size=18,
                              color=COR_VERMELHO, line=dict(width=2.5, color=COR_VERMELHO)),
                              name="Critério ±T"))
    fig4.update_layout(height=300, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(l=10, r=20, t=20, b=10),
                       yaxis=dict(title="Valor (unidade do instrumento)", gridcolor="#F1F5F9"),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<p class="norma-ref">📚 GUM/JCGM 100:2008 §4.2 (Tipo A) · §4.3.3 (Tipo B normal) · §4.3.7 (Tipo B retangular) · §5.1.2 (u_c) · §G.4 (Welch-Satterthwaite) · §6.2 (k=2) · ILAC-G8:2019 (conformidade)</p>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — Repetibilidade MSA
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("#### Repetibilidade — Estudo MSA (variação do equipamento)")
    st.caption("EV = σ_rep = R̄/d₂ · Razão P/T = 6·EV / 2T · Limite: P/T ≤ 10% ideal, ≤ 30% aceitável — AIAG MSA 4ª ed.")

    fig5 = go.Figure()
    cores_pt = [COR_VERDE if r <= 0.3 else COR_AMARELO if r <= 0.5 else COR_VERMELHO
                for r in df_msa["PT_ratio"]]
    fig5.add_trace(go.Bar(x=df_msa["ID"], y=df_msa["PT_ratio"] * 100,
                          marker_color=cores_pt,
                          text=[f"{v*100:.1f}%" for v in df_msa["PT_ratio"]],
                          textposition="outside", textfont_size=10))
    fig5.add_hline(y=10, line_color=COR_VERDE, line_dash="dash", line_width=1.5,
                   annotation_text="10% (ideal)", annotation_font_size=9)
    fig5.add_hline(y=30, line_color=COR_AMARELO, line_dash="dash", line_width=1.5,
                   annotation_text="30% (limite aceitável)", annotation_font_size=9)
    fig5.update_layout(height=320, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(l=10, r=120, t=20, b=10),
                       yaxis=dict(title="Razão P/T (%)", gridcolor="#F1F5F9"))
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("##### Tabela de repetibilidade")
    tbl_msa = df_msa[["ID","Unid","EV","uA","PT_ratio"]].copy()
    tbl_msa.columns = ["Instrumento","Unid.","EV = σ_rep (R̄/d₂)","u_A combinado","Razão P/T"]
    tbl_msa["EV = σ_rep (R̄/d₂)"]  = tbl_msa["EV = σ_rep (R̄/d₂)"].apply(lambda x: f"{x:.5f}")
    tbl_msa["u_A combinado"] = tbl_msa["u_A combinado"].apply(lambda x: f"{x:.5f}")
    tbl_msa["Razão P/T"] = tbl_msa["Razão P/T"].apply(lambda x: f"{x*100:.1f}%")
    st.dataframe(tbl_msa, use_container_width=True, hide_index=True)

    st.markdown('<div class="alerta-warn">ℹ <strong>Nota sobre P/T elevado:</strong> Valores como PHM-301 (42,4%) e DEN-401 (53,1%) não indicam instrumento ruim — a tolerância ±T é apertada. O instrumento repete bem, mas a tolerância consome boa parte da faixa. Dataset tem apenas repetibilidade (sem múltiplos operadores), portanto não é possível calcular R&R completo. <em>AIAG MSA 4ª ed. §4</em></div>', unsafe_allow_html=True)
    st.markdown('<p class="norma-ref">📚 AIAG MSA 4ª ed. · ISO 5725-2 · GUM/JCGM 100:2008 §4.2 (u_A = Tipo A)</p>', unsafe_allow_html=True)
