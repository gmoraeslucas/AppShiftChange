def create_email_content(issue_counts, crisis_data, issues_obh_data, general_observations, text_events):
    """
    Gera o conteúdo HTML do e-mail com base nas contagens de issues, nas informações detalhadas de cada crise
    e nas observações gerais.
    
    Args:
        issue_counts (dict): Dicionário com o nome do filtro e a contagem de issues.
        crisis_data (list of dict): Lista com dados das crises, cada item sendo um dicionário com as chaves 'ticket',
                                    'sistema', 'impacto', 'status', 'observacao', 'checkpoint'.
        general_observations (str): Texto das observações gerais a serem incluídas no e-mail.

    Returns:
        str: Conteúdo do e-mail em HTML.
    """

    # Tabela HTML estilizada com as duas seções
    html_content = """
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0; 
                    padding: 0;
                    display: flex;
                    justify-content: center; /* Centraliza horizontalmente */
                    background-color: #f0f0f0;
                }}

                /* Container principal */
                .table-container {{
                    width: 100%;
                    max-width: 1000px; /* Aumenta o tamanho da caixa branca */
                    margin: 20px auto; /* Centraliza vertical e horizontalmente */
                    background-color: #ffffff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    border-radius: 8px;
                    box-sizing: border-box;
                    overflow-x: auto; /* Evita rolagem horizontal */
                }}

                /* Tabelas - Ajustáveis */
                .table {{
                    width: 100%; /* Ajusta a tabela para ocupar todo o container */
                    margin: 0 auto; /* Centraliza dentro do container */
                    table-layout: auto; /* Ajusta colunas dinamicamente ao conteúdo */
                    border-collapse: collapse;
                }}

                /* Células das tabelas */
                .table th, .table td {{
                    border: 1px solid #333;
                    padding: 12px;
                    text-align: center;
                    font-size: 16px;
                    white-space: normal; /* Permite a quebra de linha */
                    word-wrap: break-word; /* Quebra palavras muito longas */
                    max-width: 200px; /* Limita a largura das células */
                    overflow-wrap: break-word;
                }}

                /* Cabeçalhos da tabela */
                .table th {{
                    background-color: #d3d3d3;
                    font-weight: bold;
                    text-align: center;
                }}

                /* Texto destacado */
                .count {{
                    font-size: 18px;
                    font-weight: bold;
                }}

                /* Título principal da tabela */
                .header-title {{
                    background-color: #5a336b;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <!-- Observações Gerais -->
            <div class="table-container">
                <h2 style="font-size: 22px;">Observações Gerais</h2>
                <p style="font-size: 16px;">{general_observations}</p>
            </div>

            <!-- Checklist -->
            <div class="table-container">
                <table class="table">
                    <tr>
                        <th colspan="5" class="header-title">Checklist</th>
                    </tr>
                    <tr>
                        <th style="width: 20%;">Tickets Registrados (Geral)</th>
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
                    <tr>
                        <th colspan="1">Ticket</th>
                        <th colspan="1">Sistema</th>
                        <th colspan="5">Resumo</th>
                        <th colspan="1">Status</th>
                        <th colspan="1">Criado</th>
                        <th colspan="1">Equipe Atendente</th>
                    </tr>
                    {issues_obh_rows}
                </table>
            </div>

            <!-- Detalhes das Crises -->
            <div class="table-container">
                <table class="table">
                    <tr>
                        <th colspan="6" class="header-title">Detalhes das Crises</th>
                    </tr>
                    <tr>
                        <th>Ticket</th>
                        <th>Sistema</th>
                        <th>Impacto</th>
                        <th>Status</th>
                        <th>Observações</th>
                        <th>Checkpoint</th>
                    </tr>
                    {crisis_rows}
                </table>
            </div>

            <p style="text-align: center;">Este é um e-mail automático gerado pela aplicação de relatórios do Jira.</p>
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
        seguranca=issue_counts.get("Segurança", 0),
        general_observations=general_observations,
        text_events=text_events,
        crisis_rows="".join([
            f"""
            <tr>
                <td>{crisis["ticket"]}</td>
                <td>{crisis["sistema"]}</td>
                <td>{crisis["impacto"]}</td>
                <td>{crisis["status"]}</td>
                <td>{crisis["observacao"]}</td>
                <td>{crisis["checkpoint"]}</td>
            </tr>
            """ for crisis in crisis_data
        ]),
        issues_obh_rows="".join([
            f"""
            <tr>
                <td colspan="1">{issue["ticket"]}</td>
                <td colspan="1">{issue["sistema"]}</td>
                <td colspan="5">{issue["resumo"]}</td>
                <td colspan="1">{issue["status"]}</td>
                <td colspan="1">{issue["criado"]}</td>
                <td colspan="1">{issue["equipe_atendente"]}</td>
            </tr>
            """ for issue in issues_obh_data
        ])
    )

    return html_content
