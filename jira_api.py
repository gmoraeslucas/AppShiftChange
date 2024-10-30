import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configurações do Jira
JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Filtros JQL para contagens específicas
JQL_QUERIES = {
    "Tickets Registrados (Geral)": "project = Governança AND issuetype = Evento AND created >= startOfDay()",
    "Tickets Resolvidos": "project = Governança AND issuetype = Evento AND status = Resolvido AND resolved >= startOfDay()",
    "Resolvidos com SLA vencido": "project = Governança AND issuetype = Evento AND status = Resolvido AND resolved >= startOfDay() AND \"SLA Evento\" = breached()",
    "Backlog": "project = Governança AND issuetype = Evento AND Status not in (Resolvido, Encerrado, Cancelado)",
    "Backlog com SLA vencido": "project = Governança AND issuetype = Evento AND Status not in (Resolvido, Encerrado, Cancelado) AND \"SLA Evento\" = breached()",
    "Banco de dados": "project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (\"Banco de Dados\") AND created >= startOfDay(-2h) AND created <= startOfDay(\"+8h\")",
    "Servidor": "project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (Servidor) AND created >= startOfDay(-2h) AND created <= startOfDay(\"+8h\")",
    "Cloud": "project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (Cloud) AND created >= startOfDay(-2h) AND created <= startOfDay(\"+8h\")",
    "Redes": "project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (Telecom) AND created >= startOfDay(-2h) AND created <= startOfDay(\"+8h\")",
    "Segurança": "project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (\"Equipe - Cyber Security\") AND created >= startOfDay(-2h) AND created <= startOfDay(\"+8h\")"
}

def get_issue_counts():
    """
    Retorna a contagem de issues para cada filtro JQL no dicionário JQL_QUERIES.
    """
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_API_TOKEN)
    counts = {}

    for name, jql in JQL_QUERIES.items():
        url = f"{JIRA_URL}/rest/api/3/search"
        params = {"jql": jql, "maxResults": 0}  # maxResults=0 para apenas a contagem
        response = requests.get(url, headers=headers, params=params, auth=auth)
        
        if response.status_code == 200:
            data = response.json()
            counts[name] = data["total"]  # O campo 'total' contém a contagem de resultados
        else:
            print(f"Erro ao buscar {name}: {response.status_code} - {response.text}")
            counts[name] = "Erro"

    return counts
