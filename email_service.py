import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuração da API Infobip
API_KEY_INFOBIP = os.getenv("API_KEY_INFOBIP")

def enviar_email_com_template_infobip(destinatario, destinatario_cc, assunto, corpo_email_html):
    base_url = 'dm62yg.api.infobip.com'
    url = f'https://{base_url}/email/3/send'
    headers = {
        'Authorization': f'App {API_KEY_INFOBIP}'
    }

    # Estrutura HTML com imagem inline
    with open('images/unnamed.png', 'rb') as img:
        files = {'inlineImage': ('unnamed.png', img)}

        html_content = f"""
        <html>
        <body style="background-color: #f0f0f0; text-align: center; font-family: Arial, sans-serif;">
            <div style="padding: 20px;">
                <div style="display: block; margin: 0 auto;">
                    <img src="cid:unnamed.png" alt="Governança de TI" style="width: 100%; max-width: 640px; height: auto; max-height: 220px; margin-bottom: 20px;"/>
                </div>
                <div style="background-color: white; padding: 20px; border-radius: 10px; display: block; margin: 0 auto; max-width: 600px; text-align: left;">
                    {corpo_email_html}
                </div>
            </div>
        </body>
        </html>
        """

        data = {
            'from': 'Governança de TI <ti-governanca@segurosunimed.com.br>',
            'to': [destinatario],
            'cc': [destinatario_cc],
            'subject': assunto,
            'html': html_content,
        }

        try:
            # Envio do e-mail via Infobip
            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()  # Lança um erro se o status não for 200
            print(f"Email enviado com sucesso para {destinatario} com cópia para {destinatario_cc}.")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar email para {destinatario}: {e}")
