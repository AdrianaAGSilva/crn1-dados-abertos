"""
Exemplo de execução: carrega variáveis do .env e roda uma extração de cada tipo
(API Implanta e planilha Excel), salvando os resultados em ./output/.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.excel_extractor import extrair_planilha_como_json
from src.implanta_client import ImplantaClient

load_dotenv()  # lê o arquivo .env, se existir, e popula os.environ

OUTPUT_DIR = Path("output")


def rodar_exemplo_api() -> None:
    """Exemplo baseado na Questão 1 do relatório: Atas de Colegiados."""
    client = ImplantaClient()
    dados = client.get(
        "AtasColegiados",
        params={"dataInicio": "01/01/2022", "dataTermino": "31/12/2023"},
    )
    _salvar(dados, "atas_colegiados.json")


def rodar_exemplo_excel() -> None:
    """Exemplo baseado na Questão 6 do relatório: Alienações de Bens."""
    url = (
        "https://novoportal.crn1.org.br/formularios/dados_abertos_crn1/"
        "relacao_de_alienacoes_bens_imoveis_veiculos.xlsx"
    )
    json_string = extrair_planilha_como_json(url)
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "alienacoes_bens.json").write_text(json_string, encoding="utf-8")
    print("Salvo em output/alienacoes_bens.json")


def _salvar(dados, nome_arquivo: str) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    caminho = OUTPUT_DIR / nome_arquivo
    caminho.write_text(json.dumps(dados, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"Salvo em {caminho}")


if __name__ == "__main__":
    rodar_exemplo_api()
    rodar_exemplo_excel()
