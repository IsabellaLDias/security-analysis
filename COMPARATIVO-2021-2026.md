# Quedas públicas e evidência de ataques com IA, 2021–2026

## Frequência observada em três plataformas

Os históricos públicos de GitHub, Discord e Jira Software expuseram os 71 meses de janeiro de 2021 a novembro de 2026. A coleta registrou 1.836 URLs únicas, incluindo avisos menores e manutenções. A tabela seleciona os avisos classificados pela própria plataforma como de impacto maior ou crítico. O período de referência vai de 1º de janeiro de 2021 a 18 de novembro de 2023 (1.052 dias). O recente vai de 1º de janeiro de 2024 a 18 de novembro de 2026 (1.053 dias).

| Provedor | Avisos no período de referência | Avisos no período recente | Taxa de referência por 100 dias | Taxa recente por 100 dias |
|---|---:|---:|---:|---:|
| [GitHub](https://www.githubstatus.com/history) | 55 | 149 | 5,23 | 14,15 |
| [Discord](https://discordstatus.com/history) | 47 | 70 | 4,47 | 6,65 |
| [Jira Software](https://jira-software.status.atlassian.com/history) | 73 | 103 | 6,94 | 9,78 |
| **Total dos três provedores** | **175** | **322** | **16,63** | **30,58** |

A taxa agregada de avisos por 100 dias de calendário cresceu cerca de **84%**. O acumulado dos três provedores foi de **61 em 2021, 56 em 2022, 58 até 18/11/2023, 83 em 2024, 91 em 2025 e 148 até 18/11/2026**, usando as mesmas janelas da tabela. A unidade é o aviso público, com uma URL por linha. Alterações de cobertura, critérios de gravidade, volume e serviços monitorados podem afetar o comparativo. Com os três anos completos de referência, seriam 179 avisos em 1.095 dias, ou 16,35 por 100 dias.

A busca inicial por termos de ataque nos títulos e resumos históricos sinalizou três registros, dos quais um era maior ou crítico. Para esse caso, em 17/08/2026, o relatório detalhado do GitHub atribui a indisponibilidade à saturação de balanceadores num centro de dados durante um pico de tráfego, agravada por novas tentativas automáticas de acesso. A triagem por termos é insuficiente para classificar a causa do conjunto. A taxa de quedas por ataque e a taxa de quedas por ataques assistidos por IA continuam indeterminadas nesse grupo. [Relatório de disponibilidade do GitHub](https://github.blog/news-insights/company-news/github-availability-report-august-2026/)

## Casos que testam a atribuição

| Data | Episódio | O que a evidência sustenta |
|---|---|---|
| 07/12/2021 | AWS, Virgínia do Norte | Falha operacional associada ao congestionamento em rede interna. [AWS](https://aws.amazon.com/message/12721/) |
| Junho de 2023 | Serviços Microsoft | A Microsoft atribuiu interrupções temporárias a uma campanha de DDoS. A publicação deixa em aberto o uso de IA pelo atacante. [Microsoft](https://www.microsoft.com/en-us/msrc/blog/2023/06/microsoft-response-to-layer-7-distributed-denial-of-service-ddos-attacks/) |
| 08–09/11/2023 | ChatGPT e API | A OpenAI informou que as quedas intermitentes tinham padrão compatível com DDoS. Classificação da causa como suspeita. A empresa publicou separadamente outra ocorrência de 08/11 atribuída a limites de memória no roteamento, que deve ter seu próprio registro. [Quedas intermitentes](https://status.openai.com/incidents/21vl32gvx3hb) · [Outro incidente em 8 de novembro](https://status.openai.com/incidents/01JMYB63BJ47J3SXV6KSCT4D2A) |
| 30/07/2024 | Azure Front Door e CDN | O ataque de DDoS teve impacto inicial mínimo. Uma configuração de rede incorreta após a mitigação provocou o impacto maior. Uso ofensivo de IA sem informação suficiente. [Microsoft Azure](https://azure.status.microsoft/status/history/?trackingId=KTY1-HW8) |
| Setembro de 2025 | Campanha investigada pela Anthropic | A Anthropic documentou uso ofensivo de IA numa campanha de espionagem. A fonte sustenta o uso de IA em ataques reais. Falta a ligação com indisponibilidade de uma plataforma da série para entrar na taxa de quedas. [Anthropic](https://www.anthropic.com/news/disrupting-AI-espionage) |
| 18/11/2025 | Cloudflare | A suspeita inicial de DDoS foi descartada. A causa descrita foi uma mudança de permissões que afetou o arquivo consumido pelo sistema de detecção de bots. [Cloudflare](https://blog.cloudflare.com/18-november-2025-outage/) |
| Abril de 2026 | Bluesky | A empresa atribuiu interrupções intermitentes em feeds, notificações, conversas e busca a um DDoS. O comunicado deixa o uso de IA pelo atacante sem informação suficiente. [Bluesky](https://bsky.social/about/blog/04-16-2026-bluesky-service-interruption) |
| Abril de 2026 | GitHub, relato de capacidade | A empresa vincula o crescimento de fluxos de desenvolvimento com agentes a maior pressão de capacidade. Trata-se de evidência de demanda legítima de IA, registrada à parte da hipótese de uso por atacantes. [GitHub](https://github.blog/news-insights/company-news/an-update-on-github-availability/) |

## O que é possível concluir

Os avisos de impacto maior ou crítico aumentaram no grupo analisado. Os relatos documentam tanto ataques que interromperam serviços quanto criminosos usando IA em operações reais. Os casos revisados até aqui ainda carecem de uma ligação documentada entre uso ofensivo de IA e uma queda da série histórica. A hipótese permanece em aberto.

A Cloudflare informou 47,1 milhões de ataques DDoS mitigados em 2025, 121% acima de 2024. O indicador mede atividade detectada pela Cloudflare na sua rede. Para o GQM, ele ajuda a descrever o contexto de ameaças. A taxa de quedas precisa de episódios com impacto confirmado e a atribuição de IA exige evidência própria. Os dados do primeiro semestre de 2026 incluem contagens de ataques de camada de rede e contagens de requisições HTTP, com unidades distintas. [Relatório Cloudflare 2025](https://blog.cloudflare.com/ddos-threat-report-2025-q4/) · [Relatório Cloudflare do primeiro semestre de 2026](https://blog.cloudflare.com/ddos-threat-report-2026-h1/)

## Dados usados no cálculo

A [série histórica](series-historicas.json) guarda mês e URL consultada por provedor, erros de coleta e uma linha por registro. Os campos de cada linha são provedor, data exibida, impacto declarado, título, URL do incidente e sinalizador de termos de ataque.
