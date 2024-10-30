from jira_api import get_issue_counts
from email_template import create_email_content
from email_service import enviar_email_com_template_infobip

if __name__ == "__main__":
    # Obter as contagens de issues
    issue_counts = get_issue_counts()

    # Gerar o conteúdo HTML do e-mail usando o template
    corpo_email_html = create_email_content(issue_counts)

    # Destinatários
    destinatario = "lucas.moraes.stefanini@segurosunimed.com.br"        # Destinatário principal
    destinatario_cc = "gabriel.coelho@segurosunimed.com.br"             # Destinatário em cópia

    # Assunto do e-mail
    assunto = "Relatório de Issues do Jira"

    # Enviar o e-mail
    enviar_email_com_template_infobip(destinatario, destinatario_cc, assunto, corpo_email_html)
