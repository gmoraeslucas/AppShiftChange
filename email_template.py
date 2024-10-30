def create_email_content(issue_counts):
    """
    Gera o conteúdo HTML do e-mail com base nas contagens de issues, com o estilo semelhante ao exemplo.
    Args:
        issue_counts (dict): Dicionário com o nome do filtro e a contagem de issues.
    Returns:
        str: Conteúdo do e-mail em HTML.
    """

    # Tabela HTML estilizada com as duas seções
    html_content = """
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h2 {{ color: #333; }}
                .table-container {{ width: 100%; max-width: 600px; margin: auto; }}
                .table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .table, .table th, .table td {{ border: 1px solid #333; }}
                .table th, .table td {{ padding: 8px; text-align: center; }}
                .table th {{ background-color: #d3d3d3; font-weight: bold; }}
                .checklist-title {{ background-color: #d3d3d3; font-weight: bold; font-size: 16px; }}
                .alerts-title {{ color: #5a336b; font-weight: bold; font-size: 14px; }}
                .section-header {{ text-align: center; padding: 8px; }}
                .count {{ font-size: 18px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="table-container">
                <table class="table">
                    <tr>
                        <th colspan="5" class="checklist-title">Checklist</th>
                    </tr>
                    <tr>
                        <th>Tickets registrados<br>(Geral)</th>
                        <th>Resolvidos</th>
                        <th>Resolvidos com SLA vencido</th>
                        <th>Backlog</th>
                        <th>Backlog com SLA vencido</th>
                    </tr>
                    <tr>
                        <td class="count">{tickets_geral}</td>
                        <td class="count">{resolvidos}</td>
                        <td class="count">{resolvidos_sla_vencido}</td>
                        <td class="count">{backlog}</td>
                        <td class="count">{backlog_sla_vencido}</td>
                    </tr>
                </table>

                <table class="table">
                    <tr>
                        <th colspan="5" class="alerts-title">Alertas não resolvidos fora do horário comercial</th>
                    </tr>
                    <tr>
                        <th>Banco de Dados</th>
                        <th>Cloud</th>
                        <th>Servidor</th>
                        <th>Rede</th>
                        <th>Segurança</th>
                    </tr>
                    <tr>
                        <td class="count">{banco_dados}</td>
                        <td class="count">{cloud}</td>
                        <td class="count">{servidor}</td>
                        <td class="count">{rede}</td>
                        <td class="count">{seguranca}</td>
                    </tr>
                </table>
            </div>
            <p>Este é um e-mail automático gerado pela aplicação de relatórios do Jira.</p>
        </body>
    </html>
    """

    # Mapeando as contagens para variáveis
    html_content = html_content.format(
        tickets_geral=issue_counts.get("Tickets Registrados (Geral)", 0),
        resolvidos=issue_counts.get("Tickets Resolvidos", 0),
        resolvidos_sla_vencido=issue_counts.get("Resolvidos com SLA vencido", 0),
        backlog=issue_counts.get("Backlog", 0),
        backlog_sla_vencido=issue_counts.get("Backlog com SLA vencido", 0),
        banco_dados=issue_counts.get("Banco de dados", 0),
        cloud=issue_counts.get("Cloud", 0),
        servidor=issue_counts.get("Servidor", 0),
        rede=issue_counts.get("Redes", 0),
        seguranca=issue_counts.get("Segurança", 0)
    )

    return html_content
