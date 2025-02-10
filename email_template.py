def create_email_content(issue_counts, crisis_data, issues_obh_data, general_observations, text_events):
    """
    Gera o conteúdo HTML do e-mail com base nas contagens de issues, nas informações detalhadas de cada crise,
    nas observações gerais e nos eventos de alerta.
    """
    if issues_obh_data:
        issues_obh_details_section = (
            """
            <tr>
                <th colspan="1">Ticket</th>
                <th colspan="1">Sistema</th>
                <th colspan="5">Resumo</th>
                <th colspan="1">Status</th>
                <th colspan="1">Criado</th>
                <th colspan="1">Equipe Atendente</th>
            </tr>
            """
            + "".join([
                f"""
                <tr>
                    <td colspan="1">{issue["ticket"]}</td>
                    <td colspan="1">{issue["sistema"]}</td>
                    <td colspan="5">{issue["resumo"]}</td>
                    <td colspan="1">{issue["status"]}</td>
                    <td colspan="1">{issue["criado"]}</td>
                    <td colspan="1">{issue["equipe_atendente"]}</td>
                </tr>
                """
                for issue in issues_obh_data
            ])
        )
    else:
        issues_obh_details_section = ""

    if crisis_data:
        crisis_section = (
            """
            <tr>
                <th>Ticket</th>
                <th>Sistema</th>
                <th>Impacto</th>
                <th>Status</th>
                <th>Observações</th>
                <th>Checkpoint</th>
            </tr>
            """
            + "".join([
                f"""
                <tr>
                    <td>{crisis["ticket"]}</td>
                    <td>{crisis["sistema"]}</td>
                    <td>{crisis["impacto"]}</td>
                    <td>{crisis["status"]}</td>
                    <td>{crisis["observacao"]}</td>
                    <td>{crisis["checkpoint"]}</td>
                </tr>
                """
                for crisis in crisis_data
            ])
        )
    else:
        crisis_section = """
            <tr>
                <td colspan="6" style="text-align: center;">Nenhuma crise em andamento!</td>
            </tr>
        """

    if any(issue_counts.get(key, 0) for key in ["Banco de dados", "Cloud", "Servidor", "Redes", "Segurança"]):
        alerts_section_template = """
            <tr>
                <th colspan="1">Banco de Dados</th>
                <th colspan="1">Cloud</th>
                <th colspan="5">Servidor</th>
                <th colspan="1">Rede</th>
                <th colspan="1">Segurança</th>
                <th colspan="1">Sistemas</th>
            </tr>
            <tr>
                <td colspan="1" class="count">{banco_dados}</td>
                <td colspan="1" class="count">{cloud}</td>
                <td colspan="5" class="count">{servidor}</td>
                <td colspan="1" class="count">{rede}</td>
                <td colspan="1" class="count">{seguranca}</td>
                <td colspan="1" class="count">N/A</td>
            </tr>
            {issues_obh_details_section}
        """

        alerts_section = alerts_section_template.format(
            banco_dados=issue_counts.get("Banco de dados", 0),
            cloud=issue_counts.get("Cloud", 0),
            servidor=issue_counts.get("Servidor", 0),
            rede=issue_counts.get("Redes", 0),
            seguranca=issue_counts.get("Segurança", 0),
            issues_obh_details_section=issues_obh_details_section
        )
    else:
        alerts_section = """
            <tr>
                <td colspan="10" style="text-align: center;">Nenhum alerta fora do horário comercial!</td>
            </tr>
        """
    
    html_content = """
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                }}
                .table-container {{
                    width: 100%;
                    max-width: 1000px;
                    margin: 20px auto;
                    background-color: #edf2fb;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    border-radius: 8px;
                    box-sizing: border-box;
                    overflow-x: auto;
                }}
                .table {{
                    width: 100%;
                    margin: 0 auto;
                    table-layout: auto;
                    border-collapse: collapse;
                }}
                .table th, .table td {{
                    border: 1px solid #333;
                    padding: 12px;
                    text-align: center;
                    font-size: 16px;
                    white-space: normal;
                    word-wrap: break-word;
                    max-width: 200px;
                    overflow-wrap: break-word;
                    vertical-align: top;  /* Garante que o conteúdo fique no topo */
                }}
                .table th {{
                    background-color: #006875;
                    font-weight: bold;
                    text-align: center;
                    color: #ffffff;
                }}
                .table td {{
                    background-color: #ffffff;
                }}
                .count {{
                    font-size: 18px;
                    font-weight: bold;
                }}
                .header-title {{
                    font-weight: bold;
                }}
                .spreadsheet-link {{
                    background-color: #00525b;
                    color: #ffffff !important;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                .spreadsheet-link:hover {{
                    background-color: #003c42;
                }}
            </style>
        </head>
        <body>
            <!-- Observações Gerais -->
            <div class="table-container" style="background-color: #F5FAFC">
                <h2 style="font-size: 17px; font-weight: bold;">Observações gerais:</h2>
                <p style="font-size: 14px;">{general_observations}</p>
            </div>

            <!-- Checklist -->
            <div class="table-container">
                <table class="table">
                    <tr>
                        <th colspan="5" class="header-title">Checklist</th>
                    </tr>
                    <tr>
                        <th style="width: 20%;">Tickets Registrados</th>
                        <th style="width: 20%;">Resolvidos</th>
                        <th style="width: 20%;">Resolvidos com SLA Vencido</th>
                        <th style="width: 20%;">Backlog</th>
                        <th style="width: 20%;">Backlog com SLA Vencido</th>
                    </tr>
                    <tr>
                        <td class="count">{tickets_geral}</td>
                        <td class="count">{resolvidos}</td>
                        <td class="count">{resolvidos_sla_vencido}</td>
                        <td class="count">{backlog}</td>
                        <td class="count">{backlog_sla_vencido}</td>
                    </tr>
                </table>
            </div>

            <!-- Alertas -->
            <div class="table-container">
                <table class="table">
                    <tr>
                        <th colspan="10" class="header-title">Alertas Não Resolvidos Fora do Horário Comercial</th>
                    </tr>
                    {alerts_section}
                </table>
            </div>

            <!-- Detalhes das Crises -->
            <div class="table-container">
                <table class="table">
                    <tr>
                        <th colspan="6" class="header-title">Detalhes das Crises</th>
                    </tr>
                    {crisis_section}
                </table>
            </div>

            <!-- Link da planilha estilizado -->
            <p style="text-align: center; margin-top: 20px;">
                <a href="https://docs.google.com/spreadsheets/d/1X_wDbd4xtE597QVw4q-oHfxBZLCH79lguH0X5f7BKsw/edit?gid=0#gid=0" target="_blank" class="spreadsheet-link">
                    Planilha Backlog de eventos
                </a>
            </p>
            <p style="text-align: center;">Este é um e-mail automático gerado pela aplicação de relatórios do Jira.</p>
        </body>
        </html>
    """

    html_content = html_content.format(
        tickets_geral=issue_counts.get("Tickets Registrados", 0),
        resolvidos=issue_counts.get("Tickets Resolvidos", 0),
        resolvidos_sla_vencido=issue_counts.get("Resolvidos com SLA vencido", 0),
        backlog=issue_counts.get("Backlog", 0),
        backlog_sla_vencido=issue_counts.get("Backlog com SLA vencido", 0),
        banco_dados=issue_counts.get("Banco de dados", 0),
        cloud=issue_counts.get("Cloud", 0),
        servidor=issue_counts.get("Servidor", 0),
        rede=issue_counts.get("Redes", 0),
        seguranca=issue_counts.get("Segurança", 0),
        general_observations=general_observations,
        text_events=text_events,
        issues_obh_details_section=issues_obh_details_section,
        crisis_section=crisis_section,
        alerts_section=alerts_section
    )

    return html_content
