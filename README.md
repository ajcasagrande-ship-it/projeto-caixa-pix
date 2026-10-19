📍 Análise da Rede de Atendimento Pix da Caixa Econômica Federal

Este repositório faz parte do meu portfólio de projetos em Análise de Dados.

O objetivo é demonstrar minha capacidade de:

- consumir dados por meio de APIs REST;
- construir pipelines de dados em Databricks;
- trabalhar com PySpark e Spark SQL;
- realizar análises exploratórias;
- construir KPIs executivos;
- desenvolver dashboards utilizando Databricks Lakeview;
- documentar projetos de forma clara e organizada.

Este é um projeto de estudo, desenvolvido para fins de aprendizado e demonstração técnica.

🎯 Objetivo do Projeto

Analisar a distribuição da rede de atendimento dos serviços Pix Saque e Pix Troco disponibilizados pela Caixa Econômica Federal.

A análise busca responder questões como:

- Quantos pontos de atendimento existem?
- Quantos municípios são atendidos?
- Como a rede está distribuída pelos estados brasileiros?
- Quais localidades possuem maior concentração de pontos?
- Qual a qualidade das informações geográficas disponíveis?

🗂️ Estrutura do Projeto

projeto-caixa-pix/
│
├── notebooks/
│   ├── 01_Coleta_RAW.py
│   ├── 02_Tratamento_Dados.py
│   ├── 03_Analise_Exploratoria.py
│   ├── 04_SQL_KPIs.py
│   └── 05_Dashboard.py
│
├── imagens/
│
└── README.md

📥 Origem dos Dados

Os dados utilizados neste projeto foram obtidos a partir da API pública da Caixa Econômica Federal contendo informações sobre os pontos de atendimento dos serviços Pix Saque e Pix Troco.

Fonte:

- Caixa Econômica Federal: API pública de pontos de atendimento Pix

🔍 Metodologia

1. Coleta dos Dados
- Consumo da API.
- Paginação dos resultados.
- Armazenamento da camada RAW.

2. Tratamento dos Dados
- Limpeza e padronização.
- Tratamento de inconsistências.
- Persistência em Delta Lake.

3. Análise Exploratória
- Avaliação da cobertura nacional.
- Distribuição por estados e municípios.
- Análise da qualidade geográfica dos dados.

4. Construção de KPIs
- Total de pontos.
- Total de agentes.
- Municípios atendidos.
- Estados atendidos.
- Ranking de estados.
- Ranking de municípios.

5. Dashboard Executivo

Construção de painel utilizando Databricks Lakeview.

📊 Principais Resultados
- Cobertura Nacional
- 25.942 pontos de atendimento.
- 25.003 agentes distintos.
- 5.281 municípios atendidos.
- 27 unidades federativas atendidas.
- Concentração

Estados com maior quantidade de pontos:

- São Paulo
- Minas Gerais
- Rio Grande do Sul
- Rio de Janeiro
- Paraná

Municípios com maior quantidade de pontos:

- São Paulo
- Rio de Janeiro
- Belo Horizonte
- Brasília
- Porto Alegre
- Qualidade dos Dados
- 12.890 registros com coordenadas válidas.
- 13.052 registros com coordenadas zeradas.

📈 Dashboard

O projeto inclui um dashboard desenvolvido com Databricks Lakeview.

O painel apresenta:

- indicadores executivos;
- distribuição dos pontos por estado;
- ranking dos principais municípios;
- heatmap de distribuição;
- indicadores de qualidade geográfica.

🧠 Aprendizados

Durante o desenvolvimento deste projeto foram praticados conceitos relacionados a:

- Consumo de APIs REST.
- Engenharia de Dados.
- Databricks.
- PySpark.
- Spark SQL.
- Delta Lake.
- Construção de KPIs.
- Dashboards executivos.
- Organização de projetos analíticos.

🧪 Tecnologias Utilizadas
Python
- Databricks
- Apache Spark
- PySpark
- Spark SQL
- Delta Lake
- Databricks Lakeview
  
🚀 Evoluções Futuras

Como próximos passos, pretende-se enriquecer a análise utilizando dados externos como:

população;
PIB;
renda;
indicadores socioeconômicos;
cobertura por habitante.
📚 Status do Projeto

✔ Concluído como projeto de estudo

✔ Publicado no GitHub para compor meu portfólio de Data Science

✔ Aberto para melhorias e novas versões

📬 Contato

