# Integração IA ↔ Dashboard — Equipe 4 (CamaBier)

A IA foi integrada ao dashboard **sem reescrever o trabalho da Integrante 3**.
Foram tocados 3 pontos no `Aplicativostreamlit.py` e adicionados 3 arquivos.

## Princípio
A IA consome os **mesmos dados do dashboard** (o `dados.py`), por meio de um
adaptador (`data_contract.py`). Assim, quando a IA cita um número, ele é
idêntico ao que o dashboard mostra — nada de divergência no demo.

## O que mudou no Aplicativostreamlit.py (3 adições mínimas)
1. `import painel_ia` (após `import dados as d`).
2. Uma 6ª aba: `🤖 Assistente IA` na linha do `st.tabs([...])`.
3. O bloco `with tab6:` no fim do arquivo (chat + painel de foco que reage).
Nada do que ela já tinha foi alterado.

## Arquivos novos
| Arquivo | Papel |
|---|---|
| `data_contract.py` | Adaptador: expõe os dados do `dados.py` para a IA |
| `sistema_ia.py` | As 4 funções de IA (classificar, prever_deriva, laudo, interpretar) |
| `painel_ia.py` | O chat plugável + estado compartilhado |
| `system_prompt.txt` | System prompt v1 (base normativa controlada) |

## Como rodar
```
pip install -r requirements.txt
streamlit run Aplicativostreamlit.py
```
Abra a aba **🤖 Assistente IA** e digite, por exemplo:
"mostre a deriva do TC-201" · "capacidade do BAL-101" · "incerteza do FL-501".
O painel de foco à direita muda conforme o comando.

Modo padrão = MOCK (sem chave, sem custo). Para IA real:
`export ANTHROPIC_API_KEY="sk-ant-..."` antes de rodar.

## Limitação honesta
A troca automática de **aba** não é usada (o `st.tabs` do Streamlit não permite
trocar de aba por código); em vez disso, a IA foca o instrumento e atualiza um
painel dentro da própria aba do Assistente. Isso é robusto e não mexe nas abas dela.
