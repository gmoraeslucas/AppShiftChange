import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from datetime import datetime
import pytz
import json

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

brazil_timezone = pytz.timezone('America/Sao_Paulo')

current_time_in_brazil = datetime.now(brazil_timezone)

if current_time_in_brazil.weekday() == 0:
    from_time = 'startOfWeek("-26h")'
    to_time = 'startOfWeek("\u002b32h")'
    text_events = "Alertas não resolvidos fora do horário comercial (Fim de semana)"
    
else:
    from_time = 'startOfDay("-2h")'
    to_time = 'startOfDay("\u002b8h")' 
    text_events = "Alertas não resolvidos fora do horário comercial"

JQL_QUERIES_CHECKLIST = {
    "Tickets Registrados": "project = Governança AND issuetype = Evento AND created >= startOfDay()",
    "Tickets Resolvidos": "project = Governança AND issuetype = Evento AND status = Resolvido AND resolved >= startOfDay()",
    "Resolvidos com SLA vencido": "project = Governança AND issuetype = Evento AND status = Resolvido AND resolved >= startOfDay() AND \"SLA Evento\" = breached()",
    "Backlog": "project = Governança AND issuetype = Evento AND Status not in (Resolvido, Encerrado, Cancelado)",
    "Backlog com SLA vencido": "project = Governança AND issuetype = Evento AND Status not in (Resolvido, Encerrado, Cancelado) AND \"SLA Evento\" = breached()",
    "Banco de dados": f"project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (\"Banco de Dados\") AND created >= {from_time} AND created <= {to_time}",
    "Servidor": f"project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (Servidor) AND created >= {from_time} AND created <= {to_time}",
    "Cloud": f"project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (Cloud) AND created >= {from_time} AND created <= {to_time}",
    "Redes": f"project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (Telecom) AND created >= {from_time} AND created <= {to_time}",
    "Segurança": f"project = Governança AND status != Resolvido AND type = Evento AND \"Equipe Atendente[Dropdown]\" in (\"Equipe - Cyber Security\") AND created >= {from_time} AND created <= {to_time}"
}

def fetch_count_for_filter(name, jql):
    """
    Realiza uma consulta ao Jira para um filtro específico e retorna a contagem de issues.
    """
    url = f"{JIRA_URL}/rest/api/3/search"
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_API_TOKEN)
    params = {"jql": jql, "maxResults": 0}

    response = requests.get(url, headers=headers, params=params, auth=auth)
    if response.status_code == 200:
        data = response.json()
        count = data["total"]
        if count > 0:
            print(f"Consulta realizada com sucesso para '{name}': {count} issues encontradas.")
        else:
            print(f"Consulta realizada com sucesso para '{name}', mas nenhuma issue foi encontrada.")
        return name, count
    else:
        print(f"Erro ao buscar '{name}': {response.status_code} - {response.text}")
        return name, "Erro"

def get_issue_counts():
    """
    Retorna a contagem de issues para cada filtro JQL no dicionário JQL_QUERIES.
    Usa multithreading para executar as consultas simultaneamente.
    """
    counts = {}
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_count_for_filter, name, jql) for name, jql in JQL_QUERIES_CHECKLIST.items()]
        
        for future in as_completed(futures):
            name, count = future.result()
            counts[name] = count

    return counts

def extract_text_from_Impacto(Impacto):
    text = ""
    if isinstance(Impacto, dict):
        content = Impacto.get('content', [])
        for item in content:
            if isinstance(item, dict):
                paragraph_content = item.get('content', [])
                for paragraph in paragraph_content:
                    if isinstance(paragraph, dict):
                        text += paragraph.get('text', '') + " "
    return text.strip()


def fetch_crisis_issue_details(issue_id):
    """
    Faz uma consulta detalhada de uma crise específica pelo issue_id.
    """
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_id}"
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_API_TOKEN)

    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        issue_data = response.json()
        
        issue_ticket = issue_data['key']
        Impacto = issue_data['fields'].get('customfield_11335', {})
        issue_impacto = extract_text_from_Impacto(Impacto)

        Sistema = issue_data['fields'].get('customfield_10273', {})
        issue_sistema = Sistema.get('value', 'Não especificado')

        print(f"Processamento concluído para o ticket: {issue_ticket}")
        return {
            "ticket": issue_ticket,
            "impacto": issue_impacto,
            "sistema": issue_sistema
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes do ticket {issue_id}: {e}")
        return None

def fetch_crisis_issues():
    """
    Obtém issues de crises e faz consultas detalhadas para cada uma usando multithreading.
    """
    jql = "project = Governança AND type = Crise AND (resolved >= startOfDay() OR status IN ('Em análise', 'Em validação'))"
    url = f"{JIRA_URL}/rest/api/3/search"
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_API_TOKEN)
    params = {"jql": jql, "fields": "key", "maxResults": 50}

    response = requests.get(url, headers=headers, params=params, auth=auth)
    
    if response.status_code == 200:
        issues_data = response.json().get("issues", [])
        if not issues_data:
            print("Consulta realizada com sucesso, mas nenhuma issue foi encontrada.")
            return []

        issue_ids = [issue["key"] for issue in issues_data]

        crisis_issues = []
        with ThreadPoolExecutor(max_workers=5) as executor: 
            futures = [executor.submit(fetch_crisis_issue_details, issue_id) for issue_id in issue_ids]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    crisis_issues.append(result)

        print(f"Consulta realizada com sucesso. {len(crisis_issues)} issues de crise processadas.")
        return crisis_issues
    else:
        print(f"Erro ao buscar issues de crises: {response.status_code} - {response.text}")
        return []
    
def fetch_obh_issue_details(issue_id):
    """
    Faz uma consulta detalhada de uma crise específica pelo issue_id.
    """
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_id}"
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_API_TOKEN)

    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()

        issue_data = response.json()
        
        issue_ticket = issue_data['key']

        issue_resumo = issue_data['fields'].get('summary', {})

        Sistema = issue_data['fields'].get('customfield_10273', {})
        issue_sistema = Sistema.get('value', 'Não especificado')

        Status = issue_data['fields'].get('status', {})
        issue_status = Status.get('name', 'Não especificado')

        Criado = issue_data['fields'].get('created', {})
        Criado = Criado[:-5] + " " + Criado[-5:]
        dt_object = datetime.strptime(Criado, "%Y-%m-%dT%H:%M:%S.%f %z")
        issue_criado = dt_object.strftime("%d/%m/%Y - %H:%M")

        Equipe_atendente = issue_data['fields'].get('customfield_10275', {})
        issue_equipe_atendente = Equipe_atendente.get('value', 'Não especificado')
        print(f"Processamento concluído para o ticket: {issue_ticket}")
        return {
            "ticket": issue_ticket,
            "resumo": issue_resumo,
            "sistema": issue_sistema,
            "status": issue_status,
            "criado": issue_criado,
            "equipe_atendente": issue_equipe_atendente
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes do ticket {issue_id}: {e}")
        return None

def fetch_obh_issues():
    """
    Obtém issues fora do horário comercial e faz consultas detalhadas para cada uma usando multithreading.
    """
    jql_query_obh = f'project = Governança AND status NOT IN (Resolvido, Cancelado) AND type = Evento AND "Equipe Atendente[Dropdown]" IN ("Banco de Dados", Servidor, Cloud, Telecom, "Equipe - Cyber Security") AND created >= {from_time} AND created <= {to_time}'
    url = f"{JIRA_URL}/rest/api/3/search"
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_API_TOKEN)
    params = {"jql": jql_query_obh, "fields": "key", "maxResults": 50}

    response = requests.get(url, headers=headers, params=params, auth=auth)
    
    if response.status_code == 200:
        issues_data = response.json().get("issues", [])
        if not issues_data:
            print("Consulta realizada com sucesso, mas nenhuma issue foi encontrada.")
            return []

        issue_ids = [issue["key"] for issue in issues_data]

        obh_issues = []
        with ThreadPoolExecutor(max_workers=5) as executor: 
            futures = [executor.submit(fetch_obh_issue_details, issue_id) for issue_id in issue_ids]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    obh_issues.append(result)

        print(f"Consulta realizada com sucesso. {len(obh_issues)} issues fora do horário comercial processadas.")
        return obh_issues
    else:
        print(f"Erro ao buscar issues de crises: {response.status_code} - {response.text}")
        return []

