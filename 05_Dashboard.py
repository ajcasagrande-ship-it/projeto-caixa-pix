# Databricks notebook source
# MAGIC %md
# MAGIC # Projeto Caixa Pix
# MAGIC
# MAGIC ## Fase 5 - Dashboard Executivo
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Disponibilizar visualmente os principais indicadores identificados durante as etapas de análise exploratória e construção dos KPIs.
# MAGIC
# MAGIC ### Fonte dos Dados
# MAGIC
# MAGIC default.pix_caixa_tratado
# MAGIC
# MAGIC ### Indicadores Selecionados
# MAGIC
# MAGIC - Total de pontos de atendimento.
# MAGIC - Total de agentes distintos.
# MAGIC - Municípios atendidos.
# MAGIC - Estados atendidos.
# MAGIC - Top 10 estados.
# MAGIC - Top 10 municípios.
# MAGIC - Qualidade geográfica dos registros.
# MAGIC
# MAGIC ### Público-Alvo
# MAGIC
# MAGIC Gestores, analistas e tomadores de decisão interessados na distribuição da rede de atendimento Pix.

# COMMAND ----------

# MAGIC %md
# MAGIC # Planejamento do Dashboard
# MAGIC
# MAGIC O dashboard executivo será composto pelos principais indicadores identificados durante a análise exploratória e consolidados na etapa de construção dos KPIs.
# MAGIC
# MAGIC ## Estrutura Proposta
# MAGIC
# MAGIC ### Visão Geral
# MAGIC
# MAGIC Cards:
# MAGIC
# MAGIC - Total de pontos de atendimento.
# MAGIC - Total de agentes distintos.
# MAGIC - Municípios atendidos.
# MAGIC - Estados atendidos.
# MAGIC
# MAGIC ### Distribuição Geográfica
# MAGIC
# MAGIC Gráficos:
# MAGIC
# MAGIC - Top 10 estados por quantidade de pontos.
# MAGIC - Top 10 municípios por quantidade de pontos.
# MAGIC - Estados com menor quantidade de pontos.
# MAGIC
# MAGIC ### Qualidade dos Dados
# MAGIC
# MAGIC Indicadores:
# MAGIC
# MAGIC - Coordenadas válidas.
# MAGIC - Coordenadas zeradas.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Disponibilizar uma visão executiva da rede de atendimento Pix a partir dos dados disponibilizados pela Caixa Econômica Federal.

# COMMAND ----------

# MAGIC %md
# MAGIC # Estrutura do Dashboard
# MAGIC
# MAGIC O dashboard executivo será composto por indicadores resumidos e gráficos de distribuição geográfica.
# MAGIC
# MAGIC ## Cards
# MAGIC
# MAGIC ### Total de Pontos de Atendimento
# MAGIC
# MAGIC 25.942
# MAGIC
# MAGIC ### Agentes Distintos
# MAGIC
# MAGIC 25.003
# MAGIC
# MAGIC ### Municípios Atendidos
# MAGIC
# MAGIC 5.281
# MAGIC
# MAGIC ### Estados Atendidos
# MAGIC
# MAGIC 27
# MAGIC
# MAGIC ## Gráficos
# MAGIC
# MAGIC ### Distribuição por Estado
# MAGIC
# MAGIC Top 10 estados com maior quantidade de pontos.
# MAGIC
# MAGIC ### Distribuição por Município
# MAGIC
# MAGIC Top 10 municípios com maior quantidade de pontos.
# MAGIC
# MAGIC ### Menor Cobertura Estadual
# MAGIC
# MAGIC Estados com menor quantidade de pontos.
# MAGIC
# MAGIC ### Qualidade Geográfica
# MAGIC
# MAGIC Comparação entre coordenadas válidas e coordenadas zeradas.

# COMMAND ----------

# MAGIC %md
# MAGIC # Principais Insights
# MAGIC
# MAGIC ## Cobertura Nacional
# MAGIC
# MAGIC A rede está presente em todas as unidades federativas brasileiras.
# MAGIC
# MAGIC ## Capilaridade
# MAGIC
# MAGIC A base contempla 5.281 municípios.
# MAGIC
# MAGIC ## Concentração
# MAGIC
# MAGIC Os dez estados com maior quantidade de pontos concentram aproximadamente três quartos da rede analisada.
# MAGIC
# MAGIC ## Qualidade dos Dados
# MAGIC
# MAGIC Aproximadamente metade dos registros possui coordenadas geográficas válidas.
# MAGIC
# MAGIC ## Agentes
# MAGIC
# MAGIC A quantidade de agentes distintos é muito próxima da quantidade de pontos de atendimento, indicando baixa concentração de múltiplos pontos por agente.

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado Final
# MAGIC
# MAGIC O dashboard executivo foi implementado utilizando Lakeview Dashboards do Databricks.
# MAGIC
# MAGIC ## Dashboard
# MAGIC
# MAGIC Dashboard Executivo - Rede Pix Caixa
# MAGIC
# MAGIC ## Indicadores Disponíveis
# MAGIC
# MAGIC - Total de pontos de atendimento.
# MAGIC - Total de agentes distintos.
# MAGIC - Municípios atendidos.
# MAGIC - Estados atendidos.
# MAGIC - Top 10 estados.
# MAGIC - Top 10 municípios.
# MAGIC - Distribuição geográfica da rede.
# MAGIC - Indicadores de qualidade geográfica.
# MAGIC
# MAGIC ## Observação
# MAGIC
# MAGIC O dashboard constitui o produto final deste projeto e consolida os resultados produzidos nas etapas anteriores.
# MAGIC