import pandas as pd
from datetime import date

# ── Aba: Instrumentos ────────────────────────────────────────────────────────
INSTRUMENTOS = pd.DataFrame([
    {"ID":"BAL-101","Instrumento":"Balança plataforma 500 kg","Etapa":1,"Grandeza":"Massa","Faixa":"0–500 kg","Nominal":250.0,"Criterio_T":0.050,"U_k2":0.005,"Cpk":4.89,"Norma":"ISO 17025 §6.5","Status_achado":"Capaz, mas rastreabilidade inválida (PAD-MASS-01)","Semaforo_Cpk":"VERDE","Alerta_rastr":True},
    {"ID":"TC-201","Instrumento":"Termopar tipo K (mostura)","Etapa":1,"Grandeza":"Temperatura","Faixa":"0–120 °C","Nominal":65.0,"Criterio_T":0.50,"U_k2":0.10,"Cpk":0.68,"Norma":"GUM; ISO 5725; Dec. 6.871","Status_achado":"Deriva crítica de viés (Anomalia 1)","Semaforo_Cpk":"VERMELHO","Alerta_rastr":False},
    {"ID":"PHM-301","Instrumento":"pHmetro de bancada","Etapa":1,"Grandeza":"pH","Faixa":"0–14 pH","Nominal":5.40,"Criterio_T":0.05,"U_k2":0.01,"Cpk":2.38,"Norma":"Dec. 6.871 (PIQ); GUM","Status_achado":"Saudável","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"DEN-401","Instrumento":"Densímetro automático","Etapa":1,"Grandeza":"Densidade (°Plato)","Faixa":"0–30 °P","Nominal":12.0,"Criterio_T":0.020,"U_k2":0.005,"Cpk":2.45,"Norma":"Dec. 6.871; GUM","Status_achado":"Saudável","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"FL-501","Instrumento":"Medidor de vazão volumétrico","Etapa":2,"Grandeza":"Volume","Faixa":"0–600 mL","Nominal":355.0,"Criterio_T":1.00,"U_k2":0.20,"Cpk":2.47,"Norma":"Portaria INMETRO 248/2008","Status_achado":"Saudável (grandeza regulada)","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"TC-202","Instrumento":"Termopar tipo K (envase)","Etapa":2,"Grandeza":"Temperatura","Faixa":"-10 a 30 °C","Nominal":2.0,"Criterio_T":0.30,"U_k2":0.05,"Cpk":2.22,"Norma":"GUM; OIML","Status_achado":"Saudável","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"MAN-601","Instrumento":"Transdutor de pressão CO₂","Etapa":2,"Grandeza":"Pressão","Faixa":"0–10 bar","Nominal":2.700,"Criterio_T":0.020,"U_k2":0.005,"Cpk":2.06,"Norma":"GUM; OIML","Status_achado":"Saudável","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"LVL-701","Instrumento":"Sensor de nível","Etapa":2,"Grandeza":"Nível/altura","Faixa":"0–200 mm","Nominal":125.0,"Criterio_T":0.50,"U_k2":0.10,"Cpk":3.27,"Norma":"GUM","Status_achado":"Saudável","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"TRQ-801","Instrumento":"Torquímetro digital","Etapa":3,"Grandeza":"Torque","Faixa":"0–5 N·m","Nominal":1.600,"Criterio_T":0.050,"U_k2":0.010,"Cpk":2.17,"Norma":"AIAG MSA; ISO 2859","Status_achado":"Deriva leve preventiva (Anomalia 3)","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"DIN-901","Instrumento":"Dinamômetro digital","Etapa":3,"Grandeza":"Força","Faixa":"0–200 N","Nominal":85.0,"Criterio_T":1.00,"U_k2":0.20,"Cpk":1.94,"Norma":"AIAG MSA","Status_achado":"Maior dispersão, dentro do critério","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"CAM-1001","Instrumento":"Sistema de visão computacional","Etapa":3,"Grandeza":"Desvio dimensional","Faixa":"±10 mm","Nominal":0.0,"Criterio_T":0.10,"U_k2":0.02,"Cpk":1.94,"Norma":"ISO 2859; MSA","Status_achado":"Saudável","Semaforo_Cpk":"VERDE","Alerta_rastr":False},
    {"ID":"PAD-MASS-01","Instrumento":"Padrão de massa 1 kg classe F1","Etapa":0,"Grandeza":"Massa (referência)","Faixa":"1 kg","Nominal":1.0,"Criterio_T":None,"U_k2":0.00005,"Cpk":None,"Norma":"ISO 17025 §6.5","Status_achado":"Sem rastreabilidade RBC (Anomalia 2)","Semaforo_Cpk":"—","Alerta_rastr":True},
])

# ── Aba: Capacidade (Cp/Cpk/Pp/Ppk) ────────────────────────────────────────
CAPACIDADE = pd.DataFrame([
    {"ID":"BAL-101","Unid":"kg","T":0.05,"Erro_medio":-0.00114,"Sigma_dentro":0.00382,"Sigma_global":0.00369,"Cp":4.36,"Cpk":4.26,"Pp":4.52,"Ppk":4.41,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"TC-201","Unid":"°C","T":0.5,"Erro_medio":0.15317,"Sigma_dentro":0.05417,"Sigma_global":0.12636,"Cp":3.08,"Cpk":2.13,"Pp":1.32,"Ppk":0.91,"Sem_Cpk":"VERDE","Sem_Ppk":"VERMELHO"},
    {"ID":"PHM-301","Unid":"pH","T":0.05,"Erro_medio":-0.00035,"Sigma_dentro":0.00707,"Sigma_global":0.00648,"Cp":2.36,"Cpk":2.34,"Pp":2.57,"Ppk":2.55,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"DEN-401","Unid":"°P","T":0.02,"Erro_medio":-0.00027,"Sigma_dentro":0.00354,"Sigma_global":0.00342,"Cp":1.88,"Cpk":1.86,"Pp":1.95,"Ppk":1.92,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"FL-501","Unid":"mL","T":1.0,"Erro_medio":-0.00784,"Sigma_dentro":0.12042,"Sigma_global":0.11532,"Cp":2.77,"Cpk":2.75,"Pp":2.89,"Ppk":2.87,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"TC-202","Unid":"°C","T":0.3,"Erro_medio":0.0041,"Sigma_dentro":0.03758,"Sigma_global":0.03636,"Cp":2.66,"Cpk":2.62,"Pp":2.75,"Ppk":2.71,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"MAN-601","Unid":"bar","T":0.02,"Erro_medio":-0.00012,"Sigma_dentro":0.00312,"Sigma_global":0.0031,"Cp":2.14,"Cpk":2.13,"Pp":2.15,"Ppk":2.14,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"LVL-701","Unid":"mm","T":0.5,"Erro_medio":-0.00993,"Sigma_dentro":0.0661,"Sigma_global":0.06357,"Cp":2.52,"Cpk":2.47,"Pp":2.62,"Ppk":2.57,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"TRQ-801","Unid":"N·m","T":0.05,"Erro_medio":0.00136,"Sigma_dentro":0.00672,"Sigma_global":0.00733,"Cp":2.48,"Cpk":2.41,"Pp":2.27,"Ppk":2.21,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"DIN-901","Unid":"N","T":1.0,"Erro_medio":-0.00551,"Sigma_dentro":0.15118,"Sigma_global":0.15143,"Cp":2.20,"Cpk":2.19,"Pp":2.20,"Ppk":2.19,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
    {"ID":"CAM-1001","Unid":"mm","T":0.1,"Erro_medio":0.00136,"Sigma_dentro":0.01324,"Sigma_global":0.01275,"Cp":2.52,"Cpk":2.48,"Pp":2.61,"Ppk":2.58,"Sem_Cpk":"VERDE","Sem_Ppk":"VERDE"},
])

# ── Aba: Deriva (Cpk por calibração) ────────────────────────────────────────
DERIVA = pd.DataFrame([
    {"ID":"BAL-101","Cal":1,"Data":date(2025,2,2),"Erro_medio":0.0007,"Sigma":0.0031,"Cp":5.31,"Cpk":5.23,"Semaforo":"VERDE"},
    {"ID":"BAL-101","Cal":2,"Data":date(2025,5,6),"Erro_medio":-0.0018,"Sigma":0.0035,"Cp":4.70,"Cpk":4.53,"Semaforo":"VERDE"},
    {"ID":"BAL-101","Cal":3,"Data":date(2025,8,13),"Erro_medio":-0.0012,"Sigma":0.0048,"Cp":3.48,"Cpk":3.39,"Semaforo":"VERDE"},
    {"ID":"BAL-101","Cal":4,"Data":date(2025,11,28),"Erro_medio":-0.0014,"Sigma":0.0036,"Cp":4.67,"Cpk":4.54,"Semaforo":"VERDE"},
    {"ID":"BAL-101","Cal":5,"Data":date(2026,3,8),"Erro_medio":-0.002,"Sigma":0.0033,"Cp":5.10,"Cpk":4.89,"Semaforo":"VERDE"},
    {"ID":"TC-201","Cal":1,"Data":date(2025,2,20),"Erro_medio":-0.0007,"Sigma":0.0484,"Cp":3.44,"Cpk":3.44,"Semaforo":"VERDE"},
    {"ID":"TC-201","Cal":2,"Data":date(2025,5,26),"Erro_medio":0.0669,"Sigma":0.0292,"Cp":5.71,"Cpk":4.94,"Semaforo":"VERDE"},
    {"ID":"TC-201","Cal":3,"Data":date(2025,9,6),"Erro_medio":0.1675,"Sigma":0.0604,"Cp":2.76,"Cpk":1.84,"Semaforo":"VERDE"},
    {"ID":"TC-201","Cal":4,"Data":date(2025,12,1),"Erro_medio":0.2228,"Sigma":0.0632,"Cp":2.64,"Cpk":1.46,"Semaforo":"VERDE"},
    {"ID":"TC-201","Cal":5,"Data":date(2026,3,12),"Erro_medio":0.3094,"Sigma":0.0939,"Cp":1.77,"Cpk":0.68,"Semaforo":"VERMELHO"},
    {"ID":"PHM-301","Cal":1,"Data":date(2025,2,23),"Erro_medio":-0.0012,"Sigma":0.0057,"Cp":2.91,"Cpk":2.84,"Semaforo":"VERDE"},
    {"ID":"PHM-301","Cal":2,"Data":date(2025,5,30),"Erro_medio":-0.0001,"Sigma":0.0057,"Cp":2.91,"Cpk":2.90,"Semaforo":"VERDE"},
    {"ID":"PHM-301","Cal":3,"Data":date(2025,8,17),"Erro_medio":0.0015,"Sigma":0.0069,"Cp":2.43,"Cpk":2.35,"Semaforo":"VERDE"},
    {"ID":"PHM-301","Cal":4,"Data":date(2025,11,21),"Erro_medio":-0.0013,"Sigma":0.0079,"Cp":2.11,"Cpk":2.05,"Semaforo":"VERDE"},
    {"ID":"PHM-301","Cal":5,"Data":date(2026,3,31),"Erro_medio":-0.0006,"Sigma":0.0069,"Cp":2.41,"Cpk":2.38,"Semaforo":"VERDE"},
    {"ID":"DEN-401","Cal":1,"Data":date(2025,2,1),"Erro_medio":0.001,"Sigma":0.0043,"Cp":1.57,"Cpk":1.49,"Semaforo":"VERDE"},
    {"ID":"DEN-401","Cal":2,"Data":date(2025,5,19),"Erro_medio":-0.001,"Sigma":0.0022,"Cp":2.98,"Cpk":2.83,"Semaforo":"VERDE"},
    {"ID":"DEN-401","Cal":3,"Data":date(2025,9,3),"Erro_medio":0.0002,"Sigma":0.0043,"Cp":1.54,"Cpk":1.52,"Semaforo":"VERDE"},
    {"ID":"DEN-401","Cal":4,"Data":date(2025,11,26),"Erro_medio":-0.0005,"Sigma":0.0034,"Cp":1.94,"Cpk":1.89,"Semaforo":"VERDE"},
    {"ID":"DEN-401","Cal":5,"Data":date(2026,3,17),"Erro_medio":-0.001,"Sigma":0.0026,"Cp":2.58,"Cpk":2.45,"Semaforo":"VERDE"},
    {"ID":"FL-501","Cal":1,"Data":date(2025,2,1),"Erro_medio":0.0496,"Sigma":0.1351,"Cp":2.47,"Cpk":2.34,"Semaforo":"VERDE"},
    {"ID":"FL-501","Cal":2,"Data":date(2025,6,1),"Erro_medio":-0.0107,"Sigma":0.0847,"Cp":3.94,"Cpk":3.89,"Semaforo":"VERDE"},
    {"ID":"FL-501","Cal":3,"Data":date(2025,9,6),"Erro_medio":0.0012,"Sigma":0.1194,"Cp":2.79,"Cpk":2.79,"Semaforo":"VERDE"},
    {"ID":"FL-501","Cal":4,"Data":date(2025,12,2),"Erro_medio":-0.0515,"Sigma":0.0956,"Cp":3.49,"Cpk":3.31,"Semaforo":"VERDE"},
    {"ID":"FL-501","Cal":5,"Data":date(2026,3,9),"Erro_medio":-0.0279,"Sigma":0.1314,"Cp":2.54,"Cpk":2.47,"Semaforo":"VERDE"},
    {"ID":"TC-202","Cal":1,"Data":date(2025,2,20),"Erro_medio":-0.0051,"Sigma":0.0406,"Cp":2.46,"Cpk":2.42,"Semaforo":"VERDE"},
    {"ID":"TC-202","Cal":2,"Data":date(2025,6,3),"Erro_medio":0.008,"Sigma":0.0331,"Cp":3.02,"Cpk":2.94,"Semaforo":"VERDE"},
    {"ID":"TC-202","Cal":3,"Data":date(2025,8,21),"Erro_medio":0.0161,"Sigma":0.0326,"Cp":3.07,"Cpk":2.91,"Semaforo":"VERDE"},
    {"ID":"TC-202","Cal":4,"Data":date(2025,11,21),"Erro_medio":-0.0089,"Sigma":0.0317,"Cp":3.15,"Cpk":3.06,"Semaforo":"VERDE"},
    {"ID":"TC-202","Cal":5,"Data":date(2026,3,1),"Erro_medio":0.0104,"Sigma":0.0434,"Cp":2.30,"Cpk":2.22,"Semaforo":"VERDE"},
    {"ID":"MAN-601","Cal":1,"Data":date(2025,1,25),"Erro_medio":-0.0009,"Sigma":0.0028,"Cp":2.40,"Cpk":2.29,"Semaforo":"VERDE"},
    {"ID":"MAN-601","Cal":2,"Data":date(2025,5,5),"Erro_medio":0.0014,"Sigma":0.0022,"Cp":3.03,"Cpk":2.82,"Semaforo":"VERDE"},
    {"ID":"MAN-601","Cal":3,"Data":date(2025,9,11),"Erro_medio":-0.0004,"Sigma":0.0037,"Cp":1.79,"Cpk":1.75,"Semaforo":"VERDE"},
    {"ID":"MAN-601","Cal":4,"Data":date(2025,12,2),"Erro_medio":-0.0018,"Sigma":0.0028,"Cp":2.35,"Cpk":2.13,"Semaforo":"VERDE"},
    {"ID":"MAN-601","Cal":5,"Data":date(2026,3,31),"Erro_medio":0.0012,"Sigma":0.003,"Cp":2.19,"Cpk":2.06,"Semaforo":"VERDE"},
    {"ID":"LVL-701","Cal":1,"Data":date(2025,2,4),"Erro_medio":0.0093,"Sigma":0.0511,"Cp":3.26,"Cpk":3.20,"Semaforo":"VERDE"},
    {"ID":"LVL-701","Cal":2,"Data":date(2025,5,15),"Erro_medio":0.018,"Sigma":0.0744,"Cp":2.24,"Cpk":2.16,"Semaforo":"VERDE"},
    {"ID":"LVL-701","Cal":3,"Data":date(2025,8,30),"Erro_medio":-0.0169,"Sigma":0.0705,"Cp":2.37,"Cpk":2.29,"Semaforo":"VERDE"},
    {"ID":"LVL-701","Cal":4,"Data":date(2025,12,18),"Erro_medio":-0.0138,"Sigma":0.0627,"Cp":2.66,"Cpk":2.59,"Semaforo":"VERDE"},
    {"ID":"LVL-701","Cal":5,"Data":date(2026,3,23),"Erro_medio":-0.0463,"Sigma":0.0462,"Cp":3.60,"Cpk":3.27,"Semaforo":"VERDE"},
    {"ID":"TRQ-801","Cal":1,"Data":date(2025,2,16),"Erro_medio":-0.0035,"Sigma":0.0052,"Cp":3.23,"Cpk":3.01,"Semaforo":"VERDE"},
    {"ID":"TRQ-801","Cal":2,"Data":date(2025,5,6),"Erro_medio":-0.0003,"Sigma":0.0079,"Cp":2.10,"Cpk":2.09,"Semaforo":"VERDE"},
    {"ID":"TRQ-801","Cal":3,"Data":date(2025,8,13),"Erro_medio":0.0027,"Sigma":0.0081,"Cp":2.05,"Cpk":1.94,"Semaforo":"VERDE"},
    {"ID":"TRQ-801","Cal":4,"Data":date(2025,12,18),"Erro_medio":0.0038,"Sigma":0.0065,"Cp":2.57,"Cpk":2.38,"Semaforo":"VERDE"},
    {"ID":"TRQ-801","Cal":5,"Data":date(2026,3,7),"Erro_medio":0.004,"Sigma":0.007,"Cp":2.37,"Cpk":2.17,"Semaforo":"VERDE"},
    {"ID":"DIN-901","Cal":1,"Data":date(2025,2,9),"Erro_medio":-0.0386,"Sigma":0.1456,"Cp":2.29,"Cpk":2.20,"Semaforo":"VERDE"},
    {"ID":"DIN-901","Cal":2,"Data":date(2025,5,29),"Erro_medio":0.0726,"Sigma":0.1473,"Cp":2.26,"Cpk":2.10,"Semaforo":"VERDE"},
    {"ID":"DIN-901","Cal":3,"Data":date(2025,8,25),"Erro_medio":0.0171,"Sigma":0.118,"Cp":2.82,"Cpk":2.78,"Semaforo":"VERDE"},
    {"ID":"DIN-901","Cal":4,"Data":date(2025,12,13),"Erro_medio":0.0387,"Sigma":0.1431,"Cp":2.33,"Cpk":2.24,"Semaforo":"VERDE"},
    {"ID":"DIN-901","Cal":5,"Data":date(2026,3,16),"Erro_medio":-0.1173,"Sigma":0.1514,"Cp":2.20,"Cpk":1.94,"Semaforo":"VERDE"},
    {"ID":"CAM-1001","Cal":1,"Data":date(2025,1,27),"Erro_medio":0.0047,"Sigma":0.012,"Cp":2.77,"Cpk":2.64,"Semaforo":"VERDE"},
    {"ID":"CAM-1001","Cal":2,"Data":date(2025,5,6),"Erro_medio":0.0013,"Sigma":0.0159,"Cp":2.09,"Cpk":2.07,"Semaforo":"VERDE"},
    {"ID":"CAM-1001","Cal":3,"Data":date(2025,9,4),"Erro_medio":0.0017,"Sigma":0.0112,"Cp":2.97,"Cpk":2.91,"Semaforo":"VERDE"},
    {"ID":"CAM-1001","Cal":4,"Data":date(2025,12,19),"Erro_medio":-0.0014,"Sigma":0.0068,"Cp":4.90,"Cpk":4.83,"Semaforo":"VERDE"},
    {"ID":"CAM-1001","Cal":5,"Data":date(2026,3,12),"Erro_medio":0.0005,"Sigma":0.0171,"Cp":1.95,"Cpk":1.94,"Semaforo":"VERDE"},
])

# ── Aba: Cartas de controle ──────────────────────────────────────────────────
CARTAS = pd.DataFrame([
    {"ID":"BAL-101","Cal":1,"xbar":0.0007,"R":0.0093,"S":0.0031,"LC":-0.0011,"LSC":0.0025,"LIC":-0.0048,"Rbar":0.0118,"LSC_R":0.0209,"LIC_R":0.0026},
    {"ID":"BAL-101","Cal":2,"xbar":-0.0018,"R":0.012,"S":0.0035,"LC":-0.0011,"LSC":0.0025,"LIC":-0.0048,"Rbar":0.0118,"LSC_R":0.0209,"LIC_R":0.0026},
    {"ID":"BAL-101","Cal":3,"xbar":-0.0012,"R":0.0152,"S":0.0048,"LC":-0.0011,"LSC":0.0025,"LIC":-0.0048,"Rbar":0.0118,"LSC_R":0.0209,"LIC_R":0.0026},
    {"ID":"BAL-101","Cal":4,"xbar":-0.0014,"R":0.0118,"S":0.0036,"LC":-0.0011,"LSC":0.0025,"LIC":-0.0048,"Rbar":0.0118,"LSC_R":0.0209,"LIC_R":0.0026},
    {"ID":"BAL-101","Cal":5,"xbar":-0.002,"R":0.0106,"S":0.0033,"LC":-0.0011,"LSC":0.0025,"LIC":-0.0048,"Rbar":0.0118,"LSC_R":0.0209,"LIC_R":0.0026},
    {"ID":"TC-201","Cal":1,"xbar":-0.0007,"R":0.1474,"S":0.0484,"LC":0.1532,"LSC":0.2045,"LIC":0.1018,"Rbar":0.1667,"LSC_R":0.2963,"LIC_R":0.0372},
    {"ID":"TC-201","Cal":2,"xbar":0.0669,"R":0.0823,"S":0.0292,"LC":0.1532,"LSC":0.2045,"LIC":0.1018,"Rbar":0.1667,"LSC_R":0.2963,"LIC_R":0.0372},
    {"ID":"TC-201","Cal":3,"xbar":0.1675,"R":0.1822,"S":0.0604,"LC":0.1532,"LSC":0.2045,"LIC":0.1018,"Rbar":0.1667,"LSC_R":0.2963,"LIC_R":0.0372},
    {"ID":"TC-201","Cal":4,"xbar":0.2228,"R":0.1545,"S":0.0632,"LC":0.1532,"LSC":0.2045,"LIC":0.1018,"Rbar":0.1667,"LSC_R":0.2963,"LIC_R":0.0372},
    {"ID":"TC-201","Cal":5,"xbar":0.3094,"R":0.2672,"S":0.0939,"LC":0.1532,"LSC":0.2045,"LIC":0.1018,"Rbar":0.1667,"LSC_R":0.2963,"LIC_R":0.0372},
    {"ID":"PHM-301","Cal":1,"xbar":-0.0012,"R":0.0192,"S":0.0057,"LC":-0.0004,"LSC":0.0064,"LIC":-0.0071,"Rbar":0.0218,"LSC_R":0.0387,"LIC_R":0.0049},
    {"ID":"PHM-301","Cal":2,"xbar":-0.0001,"R":0.0182,"S":0.0057,"LC":-0.0004,"LSC":0.0064,"LIC":-0.0071,"Rbar":0.0218,"LSC_R":0.0387,"LIC_R":0.0049},
    {"ID":"PHM-301","Cal":3,"xbar":0.0015,"R":0.0179,"S":0.0069,"LC":-0.0004,"LSC":0.0064,"LIC":-0.0071,"Rbar":0.0218,"LSC_R":0.0387,"LIC_R":0.0049},
    {"ID":"PHM-301","Cal":4,"xbar":-0.0013,"R":0.0285,"S":0.0079,"LC":-0.0004,"LSC":0.0064,"LIC":-0.0071,"Rbar":0.0218,"LSC_R":0.0387,"LIC_R":0.0049},
    {"ID":"PHM-301","Cal":5,"xbar":-0.0006,"R":0.0251,"S":0.0069,"LC":-0.0004,"LSC":0.0064,"LIC":-0.0071,"Rbar":0.0218,"LSC_R":0.0387,"LIC_R":0.0049},
    {"ID":"FL-501","Cal":1,"xbar":0.0496,"R":0.4191,"S":0.1351,"LC":-0.0078,"LSC":0.1063,"LIC":-0.122,"Rbar":0.3707,"LSC_R":0.6587,"LIC_R":0.0827},
    {"ID":"FL-501","Cal":2,"xbar":-0.0107,"R":0.2724,"S":0.0847,"LC":-0.0078,"LSC":0.1063,"LIC":-0.122,"Rbar":0.3707,"LSC_R":0.6587,"LIC_R":0.0827},
    {"ID":"FL-501","Cal":3,"xbar":0.0012,"R":0.3837,"S":0.1194,"LC":-0.0078,"LSC":0.1063,"LIC":-0.122,"Rbar":0.3707,"LSC_R":0.6587,"LIC_R":0.0827},
    {"ID":"FL-501","Cal":4,"xbar":-0.0515,"R":0.3396,"S":0.0956,"LC":-0.0078,"LSC":0.1063,"LIC":-0.122,"Rbar":0.3707,"LSC_R":0.6587,"LIC_R":0.0827},
    {"ID":"FL-501","Cal":5,"xbar":-0.0279,"R":0.4385,"S":0.1314,"LC":-0.0078,"LSC":0.1063,"LIC":-0.122,"Rbar":0.3707,"LSC_R":0.6587,"LIC_R":0.0827},
    {"ID":"TRQ-801","Cal":1,"xbar":-0.0035,"R":0.016,"S":0.0052,"LC":0.0014,"LSC":0.0077,"LIC":-0.005,"Rbar":0.0207,"LSC_R":0.0368,"LIC_R":0.0046},
    {"ID":"TRQ-801","Cal":2,"xbar":-0.0003,"R":0.0227,"S":0.0079,"LC":0.0014,"LSC":0.0077,"LIC":-0.005,"Rbar":0.0207,"LSC_R":0.0368,"LIC_R":0.0046},
    {"ID":"TRQ-801","Cal":3,"xbar":0.0027,"R":0.0217,"S":0.0081,"LC":0.0014,"LSC":0.0077,"LIC":-0.005,"Rbar":0.0207,"LSC_R":0.0368,"LIC_R":0.0046},
    {"ID":"TRQ-801","Cal":4,"xbar":0.0038,"R":0.0177,"S":0.0065,"LC":0.0014,"LSC":0.0077,"LIC":-0.005,"Rbar":0.0207,"LSC_R":0.0368,"LIC_R":0.0046},
    {"ID":"TRQ-801","Cal":5,"xbar":0.004,"R":0.0254,"S":0.007,"LC":0.0014,"LSC":0.0077,"LIC":-0.005,"Rbar":0.0207,"LSC_R":0.0368,"LIC_R":0.0046},
])

# ── Aba: Repetibilidade (MSA) ────────────────────────────────────────────────
MSA = pd.DataFrame([
    {"ID":"BAL-101","Unid":"kg","EV":0.00382,"uA":0.00371,"PT_ratio":0.229},
    {"ID":"TC-201","Unid":"°C","EV":0.05417,"uA":0.06270,"PT_ratio":0.325},
    {"ID":"PHM-301","Unid":"pH","EV":0.00707,"uA":0.00668,"PT_ratio":0.424},
    {"ID":"DEN-401","Unid":"°P","EV":0.00354,"uA":0.00347,"PT_ratio":0.531},
    {"ID":"FL-501","Unid":"mL","EV":0.12042,"uA":0.11496,"PT_ratio":0.361},
    {"ID":"TC-202","Unid":"°C","EV":0.03758,"uA":0.03660,"PT_ratio":0.376},
    {"ID":"MAN-601","Unid":"bar","EV":0.00312,"uA":0.00296,"PT_ratio":0.468},
    {"ID":"LVL-701","Unid":"mm","EV":0.06610,"uA":0.06194,"PT_ratio":0.397},
    {"ID":"TRQ-801","Unid":"N·m","EV":0.00672,"uA":0.00703,"PT_ratio":0.403},
    {"ID":"DIN-901","Unid":"N","EV":0.15118,"uA":0.14158,"PT_ratio":0.454},
    {"ID":"CAM-1001","Unid":"mm","EV":0.01324,"uA":0.01314,"PT_ratio":0.397},
])

# ── Balanço de Incerteza (12 instrumentos) ───────────────────────────────────
INCERTEZA = pd.DataFrame([
    {"ID":"BAL-101","Unid":"kg","s_cal5":0.0033,"Erro_med":-0.002,"U_pad":0.005,"Resolucao":0.02,"T":0.05,"uc":0.00638,"U_k2":0.01275,"nu_eff":12554,"Situacao":"CONFORME","Obs":"Rastreabilidade inválida (PAD-MASS-01)"},
    {"ID":"TC-201","Unid":"°C","s_cal5":0.0939,"Erro_med":0.3094,"U_pad":0.1,"Resolucao":0.1,"T":0.5,"uc":0.06492,"U_k2":0.12985,"nu_eff":206,"Situacao":"CONFORME","Obs":"Deriva crítica — projeção ultrapassa ±T na Cal.6"},
    {"ID":"PHM-301","Unid":"pH","s_cal5":0.0069,"Erro_med":-0.0006,"U_pad":0.01,"Resolucao":0.01,"T":0.05,"uc":0.00617,"U_k2":0.01234,"nu_eff":576,"Situacao":"CONFORME","Obs":""},
    {"ID":"DEN-401","Unid":"°P","s_cal5":0.0026,"Erro_med":-0.001,"U_pad":0.005,"Resolucao":0.001,"T":0.02,"uc":0.00265,"U_k2":0.00530,"nu_eff":968,"Situacao":"CONFORME","Obs":""},
    {"ID":"FL-501","Unid":"mL","s_cal5":0.1314,"Erro_med":-0.0279,"U_pad":0.2,"Resolucao":0.1,"T":1.0,"uc":0.11207,"U_k2":0.22414,"nu_eff":476,"Situacao":"CONFORME","Obs":"Grandeza regulada — Portaria INMETRO 248/2008"},
    {"ID":"TC-202","Unid":"°C","s_cal5":0.0434,"Erro_med":0.0104,"U_pad":0.05,"Resolucao":0.1,"T":0.3,"uc":0.04058,"U_k2":0.08116,"nu_eff":688,"Situacao":"CONFORME","Obs":""},
    {"ID":"MAN-601","Unid":"bar","s_cal5":0.003,"Erro_med":0.0012,"U_pad":0.005,"Resolucao":0.001,"T":0.02,"uc":0.00269,"U_k2":0.00538,"nu_eff":581,"Situacao":"CONFORME","Obs":""},
    {"ID":"LVL-701","Unid":"mm","s_cal5":0.0462,"Erro_med":-0.0463,"U_pad":0.1,"Resolucao":0.1,"T":0.5,"uc":0.05955,"U_k2":0.11911,"nu_eff":2485,"Situacao":"CONFORME","Obs":""},
    {"ID":"TRQ-801","Unid":"N·m","s_cal5":0.007,"Erro_med":0.004,"U_pad":0.01,"Resolucao":0.01,"T":0.05,"uc":0.00618,"U_k2":0.01237,"nu_eff":548,"Situacao":"CONFORME","Obs":"Deriva leve monitorada"},
    {"ID":"DIN-901","Unid":"N","s_cal5":0.1514,"Erro_med":-0.1173,"U_pad":0.2,"Resolucao":0.1,"T":1.0,"uc":0.11457,"U_k2":0.22913,"nu_eff":295,"Situacao":"CONFORME","Obs":"Maior dispersão relativa"},
    {"ID":"CAM-1001","Unid":"mm","s_cal5":0.0171,"Erro_med":0.0005,"U_pad":0.02,"Resolucao":0.01,"T":0.1,"uc":0.01173,"U_k2":0.02346,"nu_eff":199,"Situacao":"CONFORME","Obs":""},
])

# ── Validade de calibração ───────────────────────────────────────────────────
from dateutil.relativedelta import relativedelta

VALIDADE_RAW = [
    {"ID":"BAL-101",     "prazo":12,"ultima_cal":date(2026,3,8),  "norma":"ISO 17025 §6.4.7; ILAC-G24"},
    {"ID":"TC-201",      "prazo": 6,"ultima_cal":date(2026,3,12), "norma":"GUM; ILAC-G24 (6 m — deriva crítica)"},
    {"ID":"PHM-301",     "prazo":12,"ultima_cal":date(2026,3,31), "norma":"Dec. 6.871/PIQ; ILAC-G24"},
    {"ID":"DEN-401",     "prazo":12,"ultima_cal":date(2026,3,17), "norma":"Dec. 6.871; ILAC-G24"},
    {"ID":"FL-501",      "prazo":12,"ultima_cal":date(2026,3,9),  "norma":"Portaria INMETRO 248/2008; ILAC-G24"},
    {"ID":"TC-202",      "prazo":12,"ultima_cal":date(2026,3,1),  "norma":"GUM; OIML D10; ILAC-G24"},
    {"ID":"MAN-601",     "prazo":12,"ultima_cal":date(2026,3,31), "norma":"GUM; OIML D10; ILAC-G24"},
    {"ID":"LVL-701",     "prazo":12,"ultima_cal":date(2026,3,23), "norma":"GUM; ILAC-G24"},
    {"ID":"TRQ-801",     "prazo":12,"ultima_cal":date(2026,3,7),  "norma":"AIAG MSA 4ª ed.; ILAC-G24"},
    {"ID":"DIN-901",     "prazo":12,"ultima_cal":date(2026,3,16), "norma":"AIAG MSA; ISO 2859; ILAC-G24"},
    {"ID":"CAM-1001",    "prazo":12,"ultima_cal":date(2026,3,12), "norma":"ISO 2859; MSA; ILAC-G24"},
    {"ID":"PAD-MASS-01", "prazo":12,"ultima_cal":date(2026,3,24), "norma":"ISO 17025 §6.5; OIML R111 — SEM RBC"},
]

TODAY = date(2026, 6, 26)

rows = []
for r in VALIDADE_RAW:
    prox = r["ultima_cal"] + relativedelta(months=r["prazo"])
    dias = (prox - TODAY).days
    inst = INSTRUMENTOS[INSTRUMENTOS["ID"] == r["ID"]]
    alerta_rastr = bool(inst["Alerta_rastr"].values[0]) if len(inst) else False
    if r["ID"] == "PAD-MASS-01" or alerta_rastr:
        status = "SEM RASTREABILIDADE"
    elif r["ID"] == "TC-201":
        status = "RECALIBRAR URGENTE"
    elif dias < 0:
        status = "VENCIDO"
    elif dias <= 60:
        status = "VENCE EM BREVE"
    else:
        status = "VÁLIDO"
    rows.append({**r, "proxima_cal": prox, "dias_restantes": dias, "status": status})

VALIDADE = pd.DataFrame(rows)
