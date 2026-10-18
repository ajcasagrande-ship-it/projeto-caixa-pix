# Databricks notebook source
# MAGIC %md
# MAGIC # Projeto Caixa Pix
# MAGIC
# MAGIC ## Fase 4 - Construção de KPIs com SQL
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Construir indicadores analíticos utilizando SQL sobre a camada tratada dos dados.
# MAGIC
# MAGIC ### Fonte dos Dados
# MAGIC
# MAGIC Tabela:
# MAGIC
# MAGIC default.pix_caixa_tratado
# MAGIC
# MAGIC ### Objetivos da Etapa
# MAGIC
# MAGIC - Construir indicadores de negócio.
# MAGIC - Aplicar consultas SQL no Databricks.
# MAGIC - Produzir informações para utilização em dashboards.
# MAGIC - Consolidar os principais resultados identificados na análise exploratória.
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC Os KPIs desta etapa serão utilizados na construção do dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC # Validação do Ambiente
# MAGIC
# MAGIC Antes do início da construção dos KPIs em SQL será realizada a validação do ambiente de execução.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Confirmar o acesso à camada tratada persistida.
# MAGIC
# MAGIC ## Fonte
# MAGIC
# MAGIC default.pix_caixa_tratado

# COMMAND ----------

spark.sql("""
SHOW TABLES IN default
""").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 1 - Total de Pontos de Atendimento
# MAGIC
# MAGIC Será calculada a quantidade total de pontos de atendimento disponíveis na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Mensurar o volume total de pontos cadastrados.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Este indicador representa a dimensão da rede de atendimento analisada.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_pontos_atendimento
# MAGIC FROM default.pix_caixa_tratado;

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 1 - Resultado
# MAGIC
# MAGIC Foi calculada a quantidade total de pontos de atendimento presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Total de pontos de atendimento:
# MAGIC
# MAGIC - 25.942
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A rede analisada possui cobertura nacional e representa um conjunto expressivo de pontos cadastrados para oferta dos serviços Pix Saque e Pix Troco.
# MAGIC
# MAGIC ## Utilização
# MAGIC
# MAGIC Este indicador será utilizado como um dos principais cards do dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 2 - Total de Agentes Distintos
# MAGIC
# MAGIC Será calculada a quantidade de agentes distintos presentes na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Mensurar a diversidade de participantes da rede de atendimento.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Este indicador permite avaliar quantas entidades diferentes operam os pontos de atendimento cadastrados.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT cnpj_agente_saque) AS total_agentes_distintos
# MAGIC FROM default.pix_caixa_tratado;

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 2 - Resultado
# MAGIC
# MAGIC Foi calculada a quantidade de agentes distintos presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Total de agentes distintos:
# MAGIC
# MAGIC - 25.003
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A quantidade de agentes distintos é muito próxima da quantidade total de pontos de atendimento.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC A maior parte dos agentes aparece associada a apenas um ponto de atendimento, indicando elevada dispersão da rede e baixa concentração de múltiplos pontos sob um mesmo identificador.
# MAGIC
# MAGIC ## Utilização
# MAGIC
# MAGIC Este indicador será utilizado como um dos principais cards do dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 3 - Municípios Atendidos
# MAGIC
# MAGIC Será calculada a quantidade de municípios distintos presentes na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Mensurar a abrangência territorial da rede de atendimento.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Este indicador permite avaliar a capilaridade dos serviços em âmbito municipal.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT cidade) AS municipios_atendidos
# MAGIC FROM default.pix_caixa_tratado;

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 3 - Resultado
# MAGIC
# MAGIC Foi calculada a quantidade de municípios distintos atendidos pela rede.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Municípios atendidos:
# MAGIC
# MAGIC - 5.281
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A rede apresenta ampla cobertura territorial, alcançando milhares de municípios em todas as regiões do país.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC O indicador reforça a elevada capilaridade da rede de atendimento Pix analisada.
# MAGIC
# MAGIC ## Utilização
# MAGIC
# MAGIC Este indicador será utilizado como um dos principais cards do dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 4 - Unidades Federativas Atendidas
# MAGIC
# MAGIC Será calculada a quantidade de unidades federativas presentes na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Mensurar a abrangência estadual da rede de atendimento.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Este indicador permite verificar se existe cobertura nacional dos serviços.
# MAGIC ``

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT estado) AS estados_atendidos
# MAGIC FROM default.pix_caixa_tratado;

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 4 - Resultado
# MAGIC
# MAGIC Foi calculada a quantidade de unidades federativas presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Unidades federativas atendidas:
# MAGIC
# MAGIC - 27
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A rede de atendimento possui cobertura em todos os estados brasileiros, incluindo o Distrito Federal.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC Os dados demonstram abrangência nacional dos serviços analisados.
# MAGIC
# MAGIC ## Utilização
# MAGIC
# MAGIC Este indicador será utilizado como um dos principais cards do dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 5 - Ranking dos Estados
# MAGIC
# MAGIC Será gerado o ranking dos estados com maior quantidade de pontos de atendimento.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar as unidades federativas com maior presença da rede de atendimento Pix.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT estado, COUNT(estado) AS quantidade_pontos
# MAGIC FROM default.pix_caixa_tratado
# MAGIC GROUP BY estado
# MAGIC ORDER BY quantidade_pontos DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 6 - Ranking dos Municípios
# MAGIC
# MAGIC Será gerado o ranking dos municípios com maior quantidade de pontos de atendimento.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar os principais centros urbanos da rede de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Este indicador permitirá a construção de um gráfico de distribuição municipal da rede.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     cidade,
# MAGIC     COUNT(cidade) AS quantidade_pontos
# MAGIC FROM default.pix_caixa_tratado
# MAGIC GROUP BY cidade
# MAGIC ORDER BY quantidade_pontos DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 7 - Qualidade Geográfica
# MAGIC
# MAGIC Será avaliada a disponibilidade das coordenadas geográficas presentes nos registros.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Mensurar a qualidade das informações de localização disponíveis para análises espaciais.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC A disponibilidade das coordenadas impacta diretamente a construção de mapas e visualizações geográficas no dashboard final.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   latitude,
# MAGIC   COUNT(latitude) AS quantidade
# MAGIC FROM default.pix_caixa_tratado
# MAGIC WHERE latitude = '0.00000'
# MAGIC GROUP BY latitude

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultado
# MAGIC
# MAGIC Registros com coordenadas zeradas:
# MAGIC
# MAGIC - 13.052
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC Estes registros não poderão ser utilizados em análises geográficas baseadas em latitude e longitude.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(latitude) AS coordenadas_validas
# MAGIC FROM default.pix_caixa_tratado
# MAGIC WHERE latitude <> '0.00000'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conclusão
# MAGIC
# MAGIC A base apresenta disponibilidade parcial de coordenadas geográficas.
# MAGIC
# MAGIC ### Resultado Consolidado
# MAGIC
# MAGIC - Coordenadas válidas: 12.890
# MAGIC - Coordenadas zeradas: 13.052
# MAGIC
# MAGIC ### Percentuais
# MAGIC
# MAGIC - Coordenadas válidas: 49,7%
# MAGIC - Coordenadas zeradas: 50,3%
# MAGIC
# MAGIC ### Impacto
# MAGIC
# MAGIC Aproximadamente metade dos registros pode ser utilizada em mapas e análises geográficas.

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 8 - Estados com Menor Quantidade de Pontos
# MAGIC
# MAGIC Será gerado o ranking das unidades federativas com menor quantidade de pontos de atendimento.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar regiões do país com menor cobertura da rede analisada.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC O indicador complementa a análise de concentração dos pontos de atendimento.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     estado,
# MAGIC     COUNT(estado) AS quantidade_pontos
# MAGIC FROM default.pix_caixa_tratado
# MAGIC GROUP BY estado
# MAGIC ORDER BY quantidade_pontos ASC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC # KPI 8 - Estados com Menor Quantidade de Pontos
# MAGIC
# MAGIC Foi gerado o ranking das unidades federativas com menor quantidade de pontos de atendimento.
# MAGIC
# MAGIC ## Principais Resultados
# MAGIC
# MAGIC 1. AP - 46
# MAGIC 2. RR - 52
# MAGIC 3. AC - 77
# MAGIC 4. RO - 172
# MAGIC 5. TO - 257
# MAGIC 6. SE - 292
# MAGIC 7. MS - 325
# MAGIC 8. AM - 344
# MAGIC 9. AL - 357
# MAGIC 10. MT - 427
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC Os estados com menor quantidade de pontos concentram-se principalmente na região Norte do país.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC Apesar da cobertura nacional, a distribuição da rede apresenta diferenças significativas entre as regiões brasileiras.

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusão da Construção dos KPIs
# MAGIC
# MAGIC Foram construídos indicadores analíticos baseados na camada tratada dos dados.
# MAGIC
# MAGIC ## Principais Indicadores
# MAGIC
# MAGIC ### Rede de Atendimento
# MAGIC
# MAGIC - Total de pontos de atendimento.
# MAGIC - Total de agentes distintos.
# MAGIC - Municípios atendidos.
# MAGIC - Estados atendidos.
# MAGIC
# MAGIC ### Distribuição Geográfica
# MAGIC
# MAGIC - Ranking dos estados com maior quantidade de pontos.
# MAGIC - Ranking dos estados com menor quantidade de pontos.
# MAGIC - Ranking dos municípios com maior quantidade de pontos.
# MAGIC
# MAGIC ### Qualidade dos Dados
# MAGIC
# MAGIC - Quantidade de coordenadas válidas.
# MAGIC - Quantidade de coordenadas zeradas.
# MAGIC
# MAGIC ## Próxima Etapa
# MAGIC
# MAGIC Construção do dashboard final para disponibilização visual dos indicadores produzidos.