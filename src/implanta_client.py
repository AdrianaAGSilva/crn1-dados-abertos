"""
Cliente para a API de transparência do portal Implanta (CRN-DF).

As credenciais (chave e senha) NUNCA devem ficar escritas no código-fonte.
Elas são lidas de variáveis de ambiente, definidas em um arquivo `.env`
local (que não deve ser versionado) ou diretamente no ambiente do sistema.

Uso básico:
    from implanta_client import ImplantaClient

    client = ImplantaClient()
    dados = client.get("AtasColegiados", params={
        "dataInicio": "01/01/2022",
        "dataTermino": "31/12/2023",
    })
"""

from __future__ import annotations

import json
import os
import urllib.parse
from typing import Any

import http.client


class ImplantaClientError(Exception):
    """Erro genérico ao consultar a API do Implanta."""


class ImplantaClient:
    """Pequeno cliente HTTP para a API do portal de transparência Implanta."""

    def __init__(
        self,
        host: str = "crn-df.implanta.net.br",
        chave: str | None = None,
        senha: str | None = None,
    ) -> None:
        self.host = host
        # Prioriza valores passados explicitamente; caso contrário, busca
        # nas variáveis de ambiente IMPLANTA_CHAVE / IMPLANTA_SENHA.
        self.chave = chave or os.environ.get("IMPLANTA_CHAVE")
        self.senha = senha or os.environ.get("IMPLANTA_SENHA")

        if not self.chave or not self.senha:
            raise ImplantaClientError(
                "Credenciais não encontradas. Defina IMPLANTA_CHAVE e "
                "IMPLANTA_SENHA como variáveis de ambiente (ex.: em um "
                "arquivo .env) antes de instanciar o cliente."
            )

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """
        Faz uma requisição GET autenticada à API do Implanta.

        Args:
            endpoint: caminho do recurso, ex. "AtasColegiados".
            params: parâmetros de query string, ex. {"dataInicio": "01/01/2022"}.

        Returns:
            O corpo da resposta já desserializado (dict ou list), quando
            possível; caso contrário, a string bruta retornada pela API.
        """
        query = f"?{urllib.parse.urlencode(params)}" if params else ""
        path = f"/portaltransparencia/servico/api/{endpoint}{query}"

        headers = {
            "Chave": self.chave,
            "Senha": self.senha,
            "Accept": "application/json, text/json",
        }

        conn = http.client.HTTPSConnection(self.host)
        try:
            conn.request("GET", path, headers=headers)
            res = conn.getresponse()
            raw = res.read().decode("utf-8")

            if res.status >= 400:
                raise ImplantaClientError(
                    f"Erro {res.status} ao acessar {endpoint}: {raw}"
                )
        finally:
            conn.close()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Alguns endpoints podem retornar corpo vazio ou não-JSON.
            return raw


if __name__ == "__main__":
    # Exemplo de uso (Questão 1 do relatório original: Atas de Colegiados)
    client = ImplantaClient()
    resultado = client.get(
        "AtasColegiados",
        params={"dataInicio": "01/01/2022", "dataTermino": "31/12/2023"},
    )
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
