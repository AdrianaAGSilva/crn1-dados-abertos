# Automação de Dados Abertos — CRN-1 / TCU

Projeto desenvolvido durante estágio para automatizar a extração, tratamento
e padronização dos dados abertos do **Conselho Regional de Nutrição 1ª
Região (CRN-1)**, em atendimento ao **Acórdão nº 1648/2024 do TCU**, que
exige que conselhos de fiscalização profissional publiquem dados abertos de
forma integrada e conforme a Lei de Acesso à Informação (Lei 12.527/2011).

## O problema

O TCU determinou que os conselhos profissionais publicassem, de forma
estruturada e auditável, um conjunto de informações (atas, quadro de
pessoal, execução financeira, balancetes, contratos, entre outros). Esses
dados estavam espalhados entre uma API de terceiros (portal Implanta) e
planilhas Excel publicadas no site do próprio conselho — formatos
diferentes, sem padronização.

## A solução

Dois módulos reutilizáveis em Python:

- **`src/implanta_client.py`** — cliente HTTP para a API de transparência
  do portal Implanta, com autenticação via variáveis de ambiente.
- **`src/excel_extractor.py`** — baixa planilhas `.xlsx` publicadas
  publicamente, converte cada linha em um dicionário e trata a
  serialização de campos de data/hora.

Ambos os módulos convertem os dados para **JSON padronizado**, pronto para
auditoria, versionamento ou publicação.

## Por que isso importa

- Substitui um processo manual e propenso a erro por um pipeline
  repetível.
- Centraliza duas fontes de dados heterogêneas (API + planilhas) em um
  formato único.
- Trata casos reais de dados "sujos" (datas em `datetime`, campos
  ausentes) de forma explícita.

## Estrutura

```
crn1-dados-abertos/
├── src/
│   ├── implanta_client.py   # cliente da API Implanta
│   └── excel_extractor.py   # extrator de planilhas Excel
├── main.py                  # exemplo de uso ponta a ponta
├── requirements.txt
├── .env.example
└── .gitignore
```

## Como rodar

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# preencha IMPLANTA_CHAVE e IMPLANTA_SENHA no .env

python main.py
```

## Nota sobre segurança

As credenciais de acesso à API **nunca** ficam no código-fonte — são lidas
de variáveis de ambiente via [`python-dotenv`](https://pypi.org/project/python-dotenv/).
O arquivo `.env` está no `.gitignore` e não deve ser versionado.

## Stack

`Python` · `requests` · `openpyxl` · `http.client` · `json`

## Relatório completo

Para quem for dar continuidade a este projeto, deixei um relatório
detalhado explicando o contexto (Acórdão TCU 1648/2024), a metodologia
e o passo a passo de como rodar cada script, questão por questão:

📄 [Relatorio_Dados_Abertos_CRN1_TCU.pdf](./Relatorio_Dados_Abertos_CRN1_TCU.pdf)
