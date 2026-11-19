# GQM — Ataques com IA e quedas de plataformas digitais

## Objetivo de medição

Investigar se aumentou a frequência de indisponibilidades públicas provocadas por ataques contra plataformas digitais entre 2021–2023 e 2024–2026, e quantificar em quais ataques que derrubaram ou degradaram serviços houve uso de IA atribuível ao atacante.

**Hipótese.** O uso de IA generativa por atacantes pode ter aumentado as interrupções por ataque no período recente. Para testá-la, cada episódio positivo precisa ligar três fatos à mesma ocorrência: o impacto no serviço, o ataque que contribuiu para esse impacto e o uso de IA pelo atacante.

## Recorte e regras

- **Janelas principais.** 01/01/2021 a 18/11/2023 (1.052 dias) e 01/01/2024 a 18/11/2026 (1.053 dias). A análise usa o mesmo dia de corte nos dois períodos, pois a coleta ocorreu em 19/11/2026. Dezembro de 2023 continua na série bruta. A análise de sensibilidade pode comparar os três anos completos de referência com 2024–2026 até a extração, ajustando a exposição pelo número de dias.
- **Contexto de adoção.** O primeiro período é uma referência histórica. Inclui o lançamento público do ChatGPT em novembro de 2022 e a adoção inicial em 2023. O segundo representa um período posterior de difusão. A data serve como aproximação temporal. A evidência do uso de IA deve vir do episódio. Como análise complementar, apresentar a série anual e tratar 2023 como transição. [Lançamento público do ChatGPT](https://openai.com/index/chatgpt/)
- **Provedores.** GitHub, Discord e Jira Software são o grupo inicial com histórico consultável nas duas janelas. Microsoft/Azure, Bluesky, AWS, OpenAI, Cloudflare e outros provedores podem contribuir com estudos de caso. Incluir outros nas taxas quando tiverem cobertura pública comparável nos dois períodos.
- **Unidade.** Um episódio por provedor, com indisponibilidade ou degradação percebida por usuários, contado pela data de início em UTC. Agrupar atualizações do mesmo episódio. Para a comparação preliminar, usar a data exibida no índice e uma linha por URL, com os níveis de impacto maior ou crítico definidos pelo provedor.
- **Causa.** Classificar como ataque confirmado com impacto, ataque suspeito, causa operacional documentada ou causa indeterminada. Se houve ataque e uma falha de mitigação ampliou seus efeitos, registrar ambos e identificar qual parte do impacto o relatório atribui a cada fator.
- **Atribuição de IA.** Por ataque confirmado, registrar IA usada pelo atacante com ligação ao episódio, uso suspeito ou ausência de informação suficiente. Se a fonte documentar o estágio, indicar planejamento, preparação ou execução. Registrar em campos próprios qualquer uso defensivo, produto de IA atingido ou pressão de demanda. Esses casos entram na contagem específica de IA ofensiva apenas se também houver evidência de uso pelo atacante naquele episódio.

## Perguntas e métricas

| Pergunta | Métrica |
|---|---|
| Q1. As plataformas divulgaram mais quedas de impacto alto? | Avisos de impacto maior ou crítico por 100 dias observados, por provedor. Na base revisada, deduplicar por episódio e apresentar contagem e taxa. |
| Q2. Aumentaram as quedas provocadas ou agravadas por ataques? | Episódios com ataque confirmado e impacto atribuído a ele por 100 dias observados. Apresentar também a fração entre os episódios de causa conhecida e quantos têm causa indeterminada. Mostrar ataques diretos e impacto ampliado pela mitigação em linhas distintas. |
| Q3. Em quantas quedas por ataque o atacante usou IA naquele episódio? | Episódios que satisfazem as três evidências por 100 dias observados. Exibir também o número confirmado, suspeito e sem informação em relação ao total de quedas por ataques confirmados. Se o denominador for zero, registrar “não calculável”. |
| Q4. Ataques com IA tiveram maior chance de causar queda? | Quando houver telemetria comparável, dividir ataques com impacto confirmado pelo total de tentativas, separando uso de IA confirmado e tentativas cujo método foi documentado sem IA. Comparar dentro do mesmo provedor e tipo de ataque. A métrica fica indeterminada sem os totais das tentativas e seus desfechos. |

## Coleta e interpretação

1. Percorrer os históricos por mês, registrando o intervalo observado e versões revisadas. Selecionar eventos de impacto maior ou crítico para o recorte inicial. Usar os mesmos tipos de serviço e regras nos dois períodos sempre que a fonte permitir. Conservar dias sem eventos em meses observados.
2. Abrir o comunicado do incidente e procurar o relatório pós-incidente e comunicações do provedor, de autoridades ou de pesquisadores com evidência direta. Guardar fonte, data, serviço, início, fim, categoria de causa, evidência de ataque, evidência de IA pelo atacante e elo com a indisponibilidade. Marcar quando o portal só informa sintomas. Uma busca por termos ajuda a localizar casos para revisão.
3. Comparar a taxa geral, a taxa de quedas por ataques e a taxa documentada de quedas por ataques com IA para o mesmo conjunto de provedores. Usar as falhas operacionais como referência para interpretar mudanças em divulgação, escala e infraestrutura. Um aumento também pode refletir mais tentativas, mudanças de tráfego, qualidade das defesas ou cobertura dos registros.
4. Para sustentar que a IA aumentou a taxa de sucesso dos atacantes, seriam necessárias séries comparáveis de tentativas com e sem uso de IA, impacto e fatores como tipo de ataque e defesas. A comparação histórica pública mede associações e casos documentados. Informação insuficiente deve aparecer na tabela.

[Comparação histórica preliminar e casos de atribuição](COMPARATIVO-2021-2026.md) · [Relação de incidentes de 2025–2026](RELACAO-2025-2026.md)
