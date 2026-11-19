<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/header/graph.svg?title=Security+Analysis&subtitle=Estudo+GQM+sobre+quedas+de+plataformas+e+ataques+com+IA&align=left&mode=dark" /><img alt="Security Analysis" src="https://shieldcn.dev/header/graph.svg?title=Security+Analysis&subtitle=Estudo+GQM+sobre+quedas+de+plataformas+e+ataques+com+IA&align=left&mode=light" /></picture>
</p>

<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/stars/IsabellaLDias/security-analysis.svg?variant=secondary&size=sm&mode=dark" /><img alt="GitHub Stars" src="https://shieldcn.dev/github/stars/IsabellaLDias/security-analysis.svg?variant=secondary&size=sm&mode=light" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/forks/IsabellaLDias/security-analysis.svg?variant=secondary&size=sm&mode=dark" /><img alt="GitHub Forks" src="https://shieldcn.dev/github/forks/IsabellaLDias/security-analysis.svg?variant=secondary&size=sm&mode=light" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/watchers/IsabellaLDias/security-analysis.svg?variant=secondary&size=sm&mode=dark" /><img alt="Watchers" src="https://shieldcn.dev/github/watchers/IsabellaLDias/security-analysis.svg?variant=secondary&size=sm&mode=light" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/contributors/IsabellaLDias/security-analysis.svg?theme=emerald&size=sm&mode=dark" /><img alt="Contributors" src="https://shieldcn.dev/github/contributors/IsabellaLDias/security-analysis.svg?theme=emerald&size=sm&mode=light" /></picture>
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/license/IsabellaLDias/security-analysis.svg?variant=ghost&size=sm&mode=dark" /><img alt="License" src="https://shieldcn.dev/github/license/IsabellaLDias/security-analysis.svg?variant=ghost&size=sm&mode=light" /></picture>
</p>

<p align="center">
  <img alt="Python" src="https://shieldcn.dev/badge/Language-Python-3776AB.svg?logo=python&variant=branded&size=sm" />
  <img alt="Markdown" src="https://shieldcn.dev/badge/Language-Markdown-000000.svg?logo=markdown&variant=branded&size=sm" />
  <img alt="JSON" src="https://shieldcn.dev/badge/Tool-JSON-000000.svg?logo=json&variant=branded&size=sm" />
</p>

# 📖 Sobre

O **Security Analysis** reúne um estudo empírico baseado no método **GQM (Goal-Question-Metric)** para investigar se houve aumento na frequência de indisponibilidades públicas provocadas por ataques contra plataformas digitais entre 2021–2023 e 2024–2026, além de levantar evidências de uso ofensivo de IA nos incidentes analisados.

O repositório concentra o plano de medição ([PLANO-GQM.md](PLANO-GQM.md)), os relatórios comparativos ([COMPARATIVO-2021-2026.md](COMPARATIVO-2021-2026.md) e [RELACAO-2025-2026.md](RELACAO-2025-2026.md)), os conjuntos de dados coletados em 19/11/2026 ([series-historicas.json](series-historicas.json), [indice-publico.csv](indice-publico.csv) e [cobertura.csv](cobertura.csv)) e scripts em **Python** ([statuspage.py](statuspage.py), [coletar_historicos.py](coletar_historicos.py) e [coletar_indices.py](coletar_indices.py)) que consultam históricos públicos no padrão Statuspage utilizando apenas a biblioteca padrão.

# 📋 Motivo

Trabalho do laboratório de medição.

# 💻 Como iniciar

### Requisitos

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/IsabellaLDias/security-analysis.git
   ```

2. Entre no diretório do projeto:

   ```sh
   cd security-analysis
   ```

3. Execute os scripts de coleta (não há dependências externas além da biblioteca padrão do Python; a execução atualiza `series-historicas.json`, `indice-publico.csv` e `cobertura.csv`):

   ```sh
   python3 coletar_historicos.py
   python3 coletar_indices.py
   ```

# 🤝 Contribuidores

<a href="https://github.com/IsabellaLDias/security-analysis/graphs/contributors">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/contributors/IsabellaLDias/security-analysis.svg?title=false&preset=transparent&border=false&mode=dark" /><img alt="Contribuidores" src="https://shieldcn.dev/contributors/IsabellaLDias/security-analysis.svg?title=false&preset=transparent&border=false&mode=light" /></picture>
</a>

# 📄 Licença

Distribuído sob a licença [MIT](LICENSE).
