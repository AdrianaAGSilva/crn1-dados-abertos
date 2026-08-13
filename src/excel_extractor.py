"""
Extrator de dados abertos publicados em planilhas Excel (.xlsx) pelo CRN-1.

Baixa um arquivo .xlsx a partir de uma URL pública, converte a primeira
planilha em uma lista de dicionários (uma linha = um dicionário) e
serializa o resultado em JSON, tratando corretamente valores do tipo
`datetime`.

Uso básico:
    from excel_extractor import extrair_planilha_como_json

    dados = extrair_planilha_como_json(
        "https://novoportal.crn1.org.br/formularios/dados_abertos_crn1/"
        "relacao_de_alienacoes_bens_imoveis_veiculos.xlsx"
    )
"""

from __future__ import annotations

import datetime
import json
from io import BytesIO
from typing import Any

import openpyxl
import requests


class ExcelExtractionError(Exception):
    """Erro ao baixar ou processar a planilha."""


def _datetime_converter(obj: Any) -> str:
    """Converte objetos datetime para string no formato YYYY-MM-DD HH:MM:SS."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError(f"Tipo não serializável: {type(obj)!r}")


def baixar_planilha(url: str, timeout: int = 30) -> openpyxl.Workbook:
    """Baixa um arquivo .xlsx a partir de uma URL e o carrega em memória."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExcelExtractionError(f"Falha ao baixar planilha em {url}: {exc}") from exc

    try:
        return openpyxl.load_workbook(filename=BytesIO(response.content))
    except Exception as exc:  # openpyxl levanta exceções variadas
        raise ExcelExtractionError(f"Falha ao abrir planilha baixada de {url}: {exc}") from exc


def planilha_para_lista_de_dicts(wb: openpyxl.Workbook) -> list[dict[str, Any]]:
    """Converte a planilha ativa de um Workbook em uma lista de dicionários."""
    sheet = wb.active
    linhas = list(sheet.iter_rows(values_only=True))

    if not linhas:
        return []

    cabecalhos, *dados = linhas
    return [dict(zip(cabecalhos, linha)) for linha in dados]


def normalizar_datas(registros: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converte valores datetime/date em strings, para permitir serialização JSON."""
    for registro in registros:
        for chave, valor in registro.items():
            if isinstance(valor, (datetime.datetime, datetime.date)):
                registro[chave] = valor.strftime("%Y-%m-%d %H:%M:%S")
    return registros


def extrair_planilha_como_json(url: str, indent: int = 4) -> str:
    """
    Fluxo completo: baixa a planilha, converte para lista de dicionários,
    normaliza datas e retorna uma string JSON formatada.
    """
    wb = baixar_planilha(url)
    registros = planilha_para_lista_de_dicts(wb)
    registros = normalizar_datas(registros)
    return json.dumps(registros, indent=indent, ensure_ascii=False)


if __name__ == "__main__":
    # Exemplo de uso (Questão 6 do relatório original: Alienações de Bens)
    URL_EXEMPLO = (
        "https://novoportal.crn1.org.br/formularios/dados_abertos_crn1/"
        "relacao_de_alienacoes_bens_imoveis_veiculos.xlsx"
    )
    print(extrair_planilha_como_json(URL_EXEMPLO))
