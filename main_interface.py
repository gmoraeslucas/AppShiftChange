import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, Frame, messagebox
from jira_api import get_issue_counts, fetch_crisis_issues, text_events
from email_template import create_email_content
from email_service import enviar_email_com_template_infobip
from datetime import datetime


def create_main_interface():
    # --- Carrega DADOS ANTES da UI (síncrono) ---
    issue_counts = get_issue_counts()
    crisis_data = fetch_crisis_issues()

    # -------------------- UI base --------------------
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    root = ttk.Window(themename="simplex")
    root.title("Gerenciamento de Crises e Contagem de Tickets")
    root.geometry("1475x800")

    # -------------------- Estilos (paleta suave) --------------------
    style = ttk.Style()

    PALETTE = {
        "app_bg": "#F3F4F6",
        "card_bg": "#F3F4F6",
        "section_bg": "#F3F4F6",
        "border": "#F3F4F6",
        "header_bg": "#475569",
        "header_fg": "#F3F4F6",
        "text": "#111827",
        "muted": "#6B7280",
        "accent": "#2563EB",
        "select_bg": "#BFDBFE",
        "select_fg": "#111827",
    }

    # Frames gerais
    style.configure("App.TFrame", background=PALETTE["app_bg"])
    style.configure("Viewport.TFrame", background=PALETTE["app_bg"])

    # LabelFrame externo (card)
    style.configure("Outer.TLabelframe",
                    background=PALETTE["card_bg"],
                    borderwidth=1)
    style.configure("Outer.TLabelframe.Label",
                    background=PALETTE["card_bg"],
                    foreground=PALETTE["muted"])

    # Seção de Crises (fundo bem claro)
    style.configure("Section.TLabelframe",
                    background=PALETTE["section_bg"],
                    borderwidth=1)
    style.configure("Section.TLabelframe.Label",
                    background=PALETTE["section_bg"],
                    foreground=PALETTE["muted"])

    # Cabeçalho das colunas
    style.configure("Header.TLabel",
                    background=PALETTE["header_bg"],
                    foreground=PALETTE["header_fg"],
                    font=("Arial", 10, "bold"),
                    padding=(8, 6))

    # Células
    style.configure("Cell.TFrame", background=PALETTE["card_bg"])
    style.configure("Cell.TLabel",
                    background=PALETTE["card_bg"],
                    foreground=PALETTE["text"])

    # Entradas (Entry/Combobox) – tons claros
    style.configure("Cell.TEntry",
                    fieldbackground=PALETTE["card_bg"],
                    foreground=PALETTE["text"])
    style.configure("Cell.TCombobox",
                    fieldbackground=PALETTE["card_bg"],
                    foreground=PALETTE["text"],
                    background=PALETTE["card_bg"])

    # Botão principal (accent indigo)
    style.configure("Accent.TButton",
                    background=PALETTE["accent"],
                    foreground="#FFFFFF",
                    font=("Arial", 10, "bold"),
                    padding=(12, 6))
    style.map("Accent.TButton",
              background=[("active", "#1D4ED8")],  # indigo-700
              foreground=[("disabled", "#E5E7EB")])

    # Labels de título
    style.configure("Title.TLabel",
                    background=PALETTE["card_bg"],
                    foreground=PALETTE["text"],
                    font=("Arial", 16, "bold"))

    # -------------------- Layout base (canvas + viewport) --------------------
    canvas = Canvas(root, highlightthickness=0, bg=PALETTE["app_bg"])
    scrollbar = ttk.Scrollbar(
        root,
        orient="vertical",
        command=canvas.yview,
        bootstyle="dark-round"  # mais suave que dark
    )
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    viewport = ttk.Frame(canvas, style="Viewport.TFrame")
    win_id = canvas.create_window((0, 0), window=viewport, anchor="nw")

    # Grid 3x3 para centralizar
    for r in (0, 2):
        viewport.grid_rowconfigure(r, weight=1)
    for c in (0, 2):
        viewport.grid_columnconfigure(c, weight=1)

    MAX_WIDTH = 1100
    center = ttk.Frame(viewport, style="App.TFrame")
    center.grid(row=1, column=1)

    # -------------------- Moldura externa (engloba tudo) --------------------
    outer = ttk.LabelFrame(
        center,
        text="",                       # defina um título geral caso queira
        padding=12,
        style="Outer.TLabelframe",
        borderwidth=1,
        relief="solid",
    )
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------- Cabeçalho --------------------
    title_lbl = ttk.Label(outer, text="Crises e Detalhes", style="Title.TLabel")
    title_lbl.pack(pady=(0, 12))

    # -------------------- Bloco de Crises --------------------
    crisis_frame = ttk.LabelFrame(
        outer,
        text="",  # sem título na borda
        padding=10,
        style="Section.TLabelframe",
        borderwidth=1,
        relief="solid",
    )
    crisis_frame.pack(fill="x", padx=10, pady=(5, 32))

    headers_crisis = ["Ticket", "Sistema", "Impacto", "Status", "Observações", "Checkpoint"]
    for col, header in enumerate(headers_crisis):
        # Cabeçalho com cor sólida e texto branco
        hdr = ttk.Label(crisis_frame, text=header, style="Header.TLabel", anchor="center")
        hdr.grid(row=0, column=col, padx=6, pady=(0, 8), sticky="nsew")

    for i in range(len(headers_crisis)):
        crisis_frame.grid_columnconfigure(i, weight=1, uniform="uniform")

    crisis_entries = []
    for row, crisis in enumerate(crisis_data, start=1):
        # Ticket, Sistema, Impacto (cards claros)
        for col, value in enumerate([crisis["ticket"], crisis["sistema"], crisis["impacto"]]):
            cell_frame = ttk.Frame(crisis_frame, style="Cell.TFrame", borderwidth=1, relief="solid")
            cell_frame.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            ttk.Label(cell_frame, text=value, style="Cell.TLabel", wraplength=170, anchor="center")\
                .pack(fill="both", expand=True, padx=8, pady=8)

        # Status (Combobox)
        status_frame = ttk.Frame(crisis_frame, style="Cell.TFrame", borderwidth=1, relief="solid")
        status_frame.grid(row=row, column=3, padx=6, pady=6, sticky="nsew")
        status_var = ttk.StringVar()
        status_entry = ttk.Combobox(
            status_frame, textvariable=status_var, width=20,
            values=["Equipes seguem atuando", "Em validação", "Normalizado"],
            state="readonly", style="Cell.TCombobox"
        )
        status_entry.pack(fill="both", expand=True, padx=8, pady=8)

        # Observações (Entry curto)
        observation_frame = ttk.Frame(crisis_frame, style="Cell.TFrame", borderwidth=1, relief="solid")
        observation_frame.grid(row=row, column=4, padx=6, pady=6, sticky="nsew")
        observation_entry = ttk.Entry(observation_frame, width=15, style="Cell.TEntry")
        observation_entry.pack(fill="both", expand=True, padx=8, pady=8)

        # Checkpoint
        checkpoint_frame = ttk.Frame(crisis_frame, style="Cell.TFrame", borderwidth=1, relief="solid")
        checkpoint_frame.grid(row=row, column=5, padx=6, pady=6, sticky="nsew")
        checkpoint_entry = ttk.Entry(checkpoint_frame, width=15, style="Cell.TEntry")
        checkpoint_entry.pack(fill="both", expand=True, padx=8, pady=8)

        crisis_entries.append({
            "ticket": crisis["ticket"],
            "impacto": crisis["impacto"],
            "sistema": crisis["sistema"],
            "status_var": status_var,
            "observation_entry": observation_entry,
            "checkpoint_entry": checkpoint_entry
        })

    # -------------------- Observações Gerais (claro) --------------------
    general_obs_frame = ttk.LabelFrame(
        outer,
        text="Observações Gerais",
        padding=10,
        style="Outer.TLabelframe",
        borderwidth=1,
        relief="solid",
    )
    general_obs_frame.pack(fill="x", padx=10, pady=(0, 12))

    general_obs_text = ttk.Text(general_obs_frame, width=100, height=5, wrap="word")
    general_obs_text.configure(
        background=PALETTE["card_bg"],
        foreground=PALETTE["text"],
        insertbackground=PALETTE["text"],
        selectbackground=PALETTE["select_bg"],
        selectforeground=PALETTE["select_fg"],
        borderwidth=0
    )
    general_obs_text.pack(fill="both", expand=True, padx=5, pady=5)

    # -------------------- Botão enviar (accent) --------------------
    buttons_bar = ttk.Frame(outer, style="App.TFrame")
    buttons_bar.pack(fill="x", padx=10, pady=(0, 10))

    send_button = ttk.Button(
        buttons_bar,
        text="Enviar E-mail",
        bootstyle="primary",
        command=lambda: submit_data(crisis_entries, general_obs_text.get("1.0", "end-1c"), issue_counts)
    )
    send_button.pack(pady=6)

    # -------------------- Layout responsivo/centralização --------------------
    relayout_scheduled = False

    def schedule_relayout(_evt=None):
        nonlocal relayout_scheduled
        if not relayout_scheduled:
            relayout_scheduled = True
            root.after_idle(relayout)

    def relayout():
        nonlocal relayout_scheduled
        target_w = min(MAX_WIDTH, max(600, canvas.winfo_width() - 40))

        center.update_idletasks()
        # força o bloco a ter ao menos target_w
        req_w = max(center.winfo_reqwidth(), target_w)
        req_h = center.winfo_reqheight()

        vp_w = max(canvas.winfo_width(), req_w + 40)   # margens
        vp_h = max(canvas.winfo_height(), req_h + 40)

        viewport.configure(width=vp_w, height=vp_h)
        canvas.itemconfig(win_id, width=vp_w, height=vp_h)
        canvas.configure(scrollregion=(0, 0, vp_w, vp_h))

        relayout_scheduled = False

    canvas.bind("<Configure>", schedule_relayout)
    center.bind("<Configure>", schedule_relayout)
    schedule_relayout()

    root.mainloop()


def submit_data(crisis_entries, general_observations, issue_counts):
    crisis_data = []
    for entry in crisis_entries:
        ticket = entry["ticket"]
        impacto = entry["impacto"]
        sistema = entry["sistema"]
        status = entry["status_var"].get()
        observation = entry["observation_entry"].get()
        checkpoint = entry["checkpoint_entry"].get()

        crisis_data.append({
            "ticket": ticket,
            "impacto": impacto,
            "sistema": sistema,
            "status": status,
            "observacao": observation,
            "checkpoint": checkpoint
        })

    formatted_observations = (general_observations or "").replace("\n", "<br>")
    email_content = create_email_content(issue_counts, crisis_data, formatted_observations, text_events)

    destinatario = "ti-commandcenter@segurosunimed.com.br"
    destinatario_cc = "thiago.maia@segurosunimed.com.br"
    today = datetime.today().strftime("%d/%m")

    try:
        enviar_email_com_template_infobip(destinatario, destinatario_cc, f"Passagem de turno - {today}", email_content)
        messagebox.showinfo("Envio de E-mail", "E-mail enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar o e-mail: {e}")
