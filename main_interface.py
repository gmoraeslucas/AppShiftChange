import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from jira_api import get_issue_counts, fetch_crisis_issues
from email_template import create_email_content
from email_service import enviar_email_com_template_infobip

issue_counts = get_issue_counts()

def create_main_interface():
    root = ttk.Window(themename="darkly")
    root.title("Gerenciamento de Crises e Contagem de Tickets")
    root.geometry("1500x900")
    root.state("zoomed")

    # Título da seção de contagem de tickets
    title_label = ttk.Label(root, text="Checklist", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)

    # Frame para a tabela de contagem de tickets (Checklist Geral) com bordas arredondadas e finas
    checklist_frame = ttk.LabelFrame(root, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    checklist_frame.pack(fill="x", padx=10, pady=5)

    # Cabeçalhos da tabela de contagem de tickets
    headers_checklist = ["Tickets registrados (Geral)", "Resolvidos", "Resolvidos com SLA vencido", "Backlog", "Backlog com SLA vencido"]
    for col, header in enumerate(headers_checklist):
        ttk.Label(checklist_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    # Valores da contagem de tickets do Checklist Geral
    checklist_values = [
        issue_counts.get("Tickets Registrados (Geral)", 0),
        issue_counts.get("Tickets Resolvidos", 0),
        issue_counts.get("Resolvidos com SLA vencido", 0),
        issue_counts.get("Backlog", 0),
        issue_counts.get("Backlog com SLA vencido", 0)
    ]
    # Exibindo valores no checklist com bordas entre células
    for col, value in enumerate(checklist_values):
        cell_frame = ttk.Frame(checklist_frame, borderwidth=1, relief="solid")
        cell_frame.grid(row=1, column=col, padx=10, pady=5, sticky="nsew")
        ttk.Label(cell_frame, text=value, anchor="center").pack(fill="both", expand=True)

    # Configura as colunas para uniformidade
    for i in range(len(headers_checklist)):
        checklist_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    # Título da seção de alertas fora do horário comercial
    alerts_title_label = ttk.Label(root, text="Alertas não resolvidos fora do horário comercial", font=("Arial", 14, "bold"))
    alerts_title_label.pack(pady=10)

    # Frame para a tabela de alertas com bordas arredondadas e finas
    alerts_frame = ttk.LabelFrame(root, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    alerts_frame.pack(fill="x", padx=10, pady=5)

    # Cabeçalhos para a tabela de alertas
    headers_alerts = ["Banco de Dados", "Cloud", "Servidor", "Redes", "Segurança"]
    for col, header in enumerate(headers_alerts):
        ttk.Label(alerts_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    # Valores dos alertas
    alerts_values = [
        issue_counts.get("Banco de dados", 0),
        issue_counts.get("Cloud", 0),
        issue_counts.get("Servidor", 0),
        issue_counts.get("Redes", 0),
        issue_counts.get("Segurança", 0)
    ]
    # Exibindo valores nos alertas com bordas entre células
    for col, value in enumerate(alerts_values):
        cell_frame = ttk.Frame(alerts_frame, borderwidth=1, relief="solid")
        cell_frame.grid(row=1, column=col, padx=10, pady=5, sticky="nsew")
        ttk.Label(cell_frame, text=value, anchor="center").pack(fill="both", expand=True)

    # Configura as colunas para uniformidade na tabela de alertas
    for i in range(len(headers_alerts)):
        alerts_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    # Título da seção de detalhes das crises
    crisis_title_label = ttk.Label(root, text="Crises e Detalhes", font=("Arial", 14, "bold"))
    crisis_title_label.pack(pady=10)

    # Frame para a tabela de crises com bordas arredondadas e finas
    crisis_frame = ttk.LabelFrame(root, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    crisis_frame.pack(fill="x", padx=10, pady=5)

    # Cabeçalhos para a tabela de crises
    headers_crisis = ["Ticket", "Sistema", "Impacto", "Status", "Observações", "Checkpoint"]
    for col, header in enumerate(headers_crisis):
        ttk.Label(crisis_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    # Configura as colunas para uniformidade na tabela de crises
    for i in range(len(headers_crisis)):
        crisis_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    # Dados das crises com campos de entrada e linhas de separação
    crisis_data = fetch_crisis_issues()
    crisis_entries = []

    for row, crisis in enumerate(crisis_data, start=1):
        # Dados da crise do Jira
        for col, value in enumerate([crisis["ticket"], crisis["sistema"], crisis["impacto"]]):
            cell_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
            cell_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            ttk.Label(cell_frame, text=value, wraplength=150, anchor="center").pack(fill="both", expand=True)
        
        # Campo de seleção de status com borda
        status_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
        status_frame.grid(row=row, column=3, padx=10, pady=5, sticky="nsew")
        status_var = ttk.StringVar()
        status_entry = ttk.Combobox(status_frame, textvariable=status_var, width=20, 
                                    values=["Equipes seguem atuando", "Em validação", "Normalizado"], 
                                    state="readonly")
        status_entry.pack(fill="both", expand=True)

        # Campo de entrada de observação com borda
        observation_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
        observation_frame.grid(row=row, column=4, padx=10, pady=5, sticky="nsew")
        observation_entry = ttk.Text(observation_frame, width=25, height=2, wrap="word")
        observation_entry.pack(fill="both", expand=True)

        # Campo de entrada para checkpoint com borda
        checkpoint_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
        checkpoint_frame.grid(row=row, column=5, padx=10, pady=5, sticky="nsew")
        checkpoint_entry = ttk.Entry(checkpoint_frame, width=15)
        checkpoint_entry.pack(fill="both", expand=True)

        # Armazena referências para coleta posterior
        crisis_entries.append({
            "ticket": crisis["ticket"],
            "impacto": crisis["impacto"],
            "sistema": crisis["sistema"],
            "status_var": status_var,
            "observation_entry": observation_entry,
            "checkpoint_entry": checkpoint_entry
        })

    # Botão de envio
    send_button = ttk.Button(root, text="Enviar E-mail", bootstyle="success", command=lambda: submit_data(crisis_entries))
    send_button.pack(pady=20)

    root.mainloop()

def submit_data(crisis_entries):
    # Processa e valida os dados inseridos pelo usuário
    all_data = []
    for entry in crisis_entries:
        ticket = entry["ticket"]
        impacto = entry["impacto"]
        sistema = entry["sistema"]
        status = entry["status_var"].get()
        observation = entry["observation_entry"].get("1.0", "end-1c")
        checkpoint = entry["checkpoint_entry"].get()

        # Armazena os dados completos da crise atual
        all_data.append({
            "ticket": ticket,
            "impacto": impacto,
            "sistema": sistema,
            "status": status,
            "observacao": observation,
            "checkpoint": checkpoint
        })

    # Gera o conteúdo HTML do e-mail usando os dados
    email_content = create_email_content(issue_counts, all_data)  # Gera o HTML do e-mail

    # Define o destinatário e o destinatário em cópia
    destinatario = "lucas.moraes.stefanini@segurosunimed.com.br"  # Defina o destinatário principal
    destinatario_cc = "ruan.santos.stefanini@segurosunimed.com.br"  # Defina o destinatário em cópia

    # Envia o e-mail
    try:
        enviar_email_com_template_infobip(destinatario, destinatario_cc, "Relatório de Crises e Contagem de Tickets", email_content)
        messagebox.showinfo("Envio de E-mail", "E-mail enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar o e-mail: {e}")


