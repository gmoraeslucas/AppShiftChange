import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, Frame, messagebox
from jira_api import get_issue_counts, fetch_crisis_issues, text_events, fetch_obh_issues
from email_template import create_email_content
from email_service import enviar_email_com_template_infobip
from datetime import datetime

issue_counts = get_issue_counts()

def create_main_interface():
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    root = ttk.Window(themename="darkly")
    root.title("Gerenciamento de Crises e Contagem de Tickets")
    root.geometry("1550x900")

    canvas = Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    canvas.bind_all("<MouseWheel>", on_mouse_wheel) 

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    title_label = ttk.Label(scrollable_frame, text="Checklist", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)

    checklist_frame = ttk.LabelFrame(scrollable_frame, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    checklist_frame.pack(fill="x", padx=10, pady=5)

    headers_checklist = ["Tickets registrados (Geral)", "Resolvidos", "Resolvidos com SLA vencido", "Backlog", "Backlog com SLA vencido"]
    for col, header in enumerate(headers_checklist):
        ttk.Label(checklist_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    checklist_values = [
        issue_counts.get("Tickets Registrados (Geral)", 0),
        issue_counts.get("Tickets Resolvidos", 0),
        issue_counts.get("Resolvidos com SLA vencido", 0),
        issue_counts.get("Backlog", 0),
        issue_counts.get("Backlog com SLA vencido", 0)
    ]
    for col, value in enumerate(checklist_values):
        cell_frame = ttk.Frame(checklist_frame, borderwidth=1, relief="solid")
        cell_frame.grid(row=1, column=col, padx=10, pady=5, sticky="nsew")
        ttk.Label(cell_frame, text=value, anchor="center").pack(fill="both", expand=True)

    for i in range(len(headers_checklist)):
        checklist_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    alerts_title_label = ttk.Label(scrollable_frame, text=text_events, font=("Arial", 14, "bold"))
    alerts_title_label.pack(pady=10)

    alerts_frame = ttk.LabelFrame(scrollable_frame, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    alerts_frame.pack(fill="x", padx=10, pady=5)

    headers_alerts = ["Banco de Dados", "Cloud", "Servidor", "Redes", "Segurança"]
    for col, header in enumerate(headers_alerts):
        ttk.Label(alerts_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    alerts_values = [
        issue_counts.get("Banco de dados", 0),
        issue_counts.get("Cloud", 0),
        issue_counts.get("Servidor", 0),
        issue_counts.get("Redes", 0),
        issue_counts.get("Segurança", 0)
    ]
    for col, value in enumerate(alerts_values):
        cell_frame = ttk.Frame(alerts_frame, borderwidth=1, relief="solid")
        cell_frame.grid(row=1, column=col, padx=10, pady=5, sticky="nsew")
        ttk.Label(cell_frame, text=value, anchor="center").pack(fill="both", expand=True)

    for i in range(len(headers_alerts)):
        alerts_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    headers_crisis = ["Ticket", "Sistema", "Resumo", "Status", "Criado", "Responsável"]
    for col, header in enumerate(headers_crisis):
        ttk.Label(alerts_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    issues_obh_data = fetch_obh_issues()
    issues_obh_entries = []

    for row, issue in enumerate(issues_obh_data, start=1):
        for col, value in enumerate([issue["ticket"], issue["sistema"], issue["resumo"], issue["status"], issue["criado"], issue["responsavel"]]):
            cell_frame = ttk.Frame(alerts_frame, borderwidth=1, relief="solid")
            cell_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            ttk.Label(cell_frame, text=value, wraplength=150, anchor="center").pack(fill="both", expand=True)

        issues_obh_entries.append({
            "ticket": issue["ticket"],
            "resumo": issue["resumo"],
            "sistema": issue["sistema"],
            "status": issue["status"],
            "criado": issue["criado"],
            "responsavel": issue["responsavel"]
        })

    crisis_title_label = ttk.Label(scrollable_frame, text="Crises e Detalhes", font=("Arial", 14, "bold"))
    crisis_title_label.pack(pady=10)

    crisis_frame = ttk.LabelFrame(scrollable_frame, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    crisis_frame.pack(fill="x", padx=10, pady=5)

    headers_crisis = ["Ticket", "Sistema", "Impacto", "Status", "Observações", "Checkpoint"]
    for col, header in enumerate(headers_crisis):
        ttk.Label(crisis_frame, text=header, font=("Arial", 10, "bold"), anchor="center").grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

    for i in range(len(headers_crisis)):
        crisis_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    crisis_data = fetch_crisis_issues()
    crisis_entries = []

    for row, crisis in enumerate(crisis_data, start=1):
        for col, value in enumerate([crisis["ticket"], crisis["sistema"], crisis["impacto"]]):
            cell_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
            cell_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            ttk.Label(cell_frame, text=value, wraplength=150, anchor="center").pack(fill="both", expand=True)
        
        status_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
        status_frame.grid(row=row, column=3, padx=10, pady=5, sticky="nsew")
        status_var = ttk.StringVar()
        status_entry = ttk.Combobox(status_frame, textvariable=status_var, width=20, 
                                    values=["Equipes seguem atuando", "Em validação", "Normalizado"], 
                                    state="readonly")
        status_entry.pack(fill="both", expand=True)

        observation_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
        observation_frame.grid(row=row, column=4, padx=10, pady=5, sticky="nsew")
        observation_entry = ttk.Text(observation_frame, width=25, height=2, wrap="word")
        observation_entry.pack(fill="both", expand=True)

        checkpoint_frame = ttk.Frame(crisis_frame, borderwidth=1, relief="solid")
        checkpoint_frame.grid(row=row, column=5, padx=10, pady=5, sticky="nsew")
        checkpoint_entry = ttk.Entry(checkpoint_frame, width=15)
        checkpoint_entry.pack(fill="both", expand=True)

        crisis_entries.append({
            "ticket": crisis["ticket"],
            "impacto": crisis["impacto"],
            "sistema": crisis["sistema"],
            "status_var": status_var,
            "observation_entry": observation_entry,
            "checkpoint_entry": checkpoint_entry
        })

    general_obs_frame = ttk.LabelFrame(scrollable_frame, text="Observações Gerais", padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
    general_obs_frame.pack(fill="x", padx=10, pady=10)
    general_obs_text = ttk.Text(general_obs_frame, width=100, height=5, wrap="word")
    general_obs_text.pack(fill="both", expand=True, padx=5, pady=5)

    send_button = ttk.Button(scrollable_frame, text="Enviar E-mail", bootstyle="success", command=lambda: submit_data(crisis_entries, issues_obh_entries, general_obs_text.get("1.0", "end-1c")))
    send_button.pack(pady=20)

    root.mainloop()

def submit_data(crisis_entries, issues_obh_entries, general_observations):
    all_data = []
    all_obh_data = []
    for entry in crisis_entries:
        ticket = entry["ticket"]
        impacto = entry["impacto"]
        sistema = entry["sistema"]
        status = entry["status_var"].get()
        observation = entry["observation_entry"].get("1.0", "end-1c")
        checkpoint = entry["checkpoint_entry"].get()

        all_data.append({
            "ticket": ticket,
            "impacto": impacto,
            "sistema": sistema,
            "status": status,
            "observacao": observation,
            "checkpoint": checkpoint
        })

    for entry in issues_obh_entries:
        ticket = entry["ticket"]
        resumo = entry["resumo"]
        sistema = entry["sistema"]
        status = entry["status"]
        criado = entry["criado"]
        responsavel = entry["responsavel"]

        all_obh_data.append({
                "ticket": ticket,
                "resumo": resumo,
                "sistema": sistema,
                "status": status,
                "criado": criado,
                "responsavel": responsavel
        })

    formatted_observations = general_observations.replace("\n", "<br>")

    email_content = create_email_content(issue_counts, all_data, all_obh_data, formatted_observations, text_events)

    destinatario = "gabriel.oliveira@segurosunimed.com.br"
    destinatario_cc = ""
    today = datetime.today().strftime("%d/%m")

    try:
        enviar_email_com_template_infobip(destinatario, destinatario_cc, f"Passagem de turno - {today}", email_content)
        messagebox.showinfo("Envio de E-mail", "E-mail enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar o e-mail: {e}")



