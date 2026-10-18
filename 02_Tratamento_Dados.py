# Databricks notebook source
# MAGIC %md
# MAGIC # Projeto Caixa Pix
# MAGIC
# MAGIC ## Fase 2 - Tratamento dos Dados
# MAGIC
# MAGIC ### Fonte
# MAGIC
# MAGIC Tabela RAW persistida:
# MAGIC
# MAGIC default.pix_caixa_raw
# MAGIC
# MAGIC ### Objetivos
# MAGIC
# MAGIC - Ler a camada RAW.
# MAGIC - Analisar o schema.
# MAGIC - Expandir estruturas aninhadas.
# MAGIC - Criar a camada tratada.
# MAGIC - Persistir a tabela tratada.

# COMMAND ----------

# Ler a tabela RAW persistida

df_raw = spark.table("default.pix_caixa_raw")

# Exibir o schema completo

df_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Planejamento da Camada Tratada
# MAGIC
# MAGIC A camada tratada terá como objetivo disponibilizar os dados em formato analítico.
# MAGIC
# MAGIC ### Colunas Selecionadas
# MAGIC
# MAGIC - cnpj_agente_saque
# MAGIC - nome_agente_saque
# MAGIC - bairro
# MAGIC - cep
# MAGIC - cidade
# MAGIC - estado
# MAGIC - logradouro
# MAGIC - latitude
# MAGIC - longitude
# MAGIC - pix_saque
# MAGIC - pix_troco
# MAGIC
# MAGIC ### Colunas Excluídas nesta Versão
# MAGIC
# MAGIC - horarios_funcionamento
# MAGIC - observacoes
# MAGIC
# MAGIC As colunas excluídas poderão ser avaliadas em versões futuras do projeto.

# COMMAND ----------

from pyspark.sql.functions import explode

# Explodir a estrutura de pontos de atendimento

df_explodido = df_raw.withColumn(
    "ponto",
    explode("pontos_atendimento")
)

# Verificar o schema após a expansão

df_explodido.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Criação da Camada Tratada
# MAGIC
# MAGIC Após a expansão da estrutura `pontos_atendimento`, será criada a primeira versão da camada tratada.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Disponibilizar os dados em formato tabular para análises e dashboards.
# MAGIC
# MAGIC ### Colunas Selecionadas
# MAGIC
# MAGIC - cnpj_agente_saque
# MAGIC - nome_agente_saque
# MAGIC - bairro
# MAGIC - cep
# MAGIC - cidade
# MAGIC - estado
# MAGIC - logradouro
# MAGIC - latitude
# MAGIC - longitude
# MAGIC - pix_saque
# MAGIC - pix_troco
# MAGIC ``

# COMMAND ----------

from pyspark.sql.functions import col

# Selecionar apenas os campos necessários
# para a primeira versão da camada tratada

df_tratado = df_explodido.select(
    col("cnpj_agente_saque"),
    col("nome_agente_saque"),
    col("ponto.bairro").alias("bairro"),
    col("ponto.cep").alias("cep"),
    col("ponto.cidade").alias("cidade"),
    col("ponto.estado").alias("estado"),
    col("ponto.logradouro").alias("logradouro"),
    col("ponto.latitude").alias("latitude"),
    col("ponto.longitude").alias("longitude"),
    col("ponto.produtos.`Pix-saque`").alias("pix_saque"),
    col("ponto.produtos.`Pix-troco`").alias("pix_troco")
)

# Exibir schema da camada tratada

df_tratado.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validação da Camada Tratada
# MAGIC
# MAGIC Após a normalização dos dados, será realizada uma validação da estrutura resultante.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Confirmar que os campos foram extraídos corretamente da estrutura aninhada e estão disponíveis para análise.
# MAGIC
# MAGIC ### Critérios
# MAGIC
# MAGIC - Ausência de estruturas complexas;
# MAGIC - Colunas analíticas disponíveis;
# MAGIC - Dados legíveis e utilizáveis em SQL e dashboards.

# COMMAND ----------

# Visualizar os primeiros registros
# da camada tratada

df_tratado.show(5, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação das Coordenadas Geográficas
# MAGIC
# MAGIC Durante a exploração da camada tratada foram identificadas coordenadas geográficas válidas.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Verificar a qualidade e completude dos dados de latitude e longitude.
# MAGIC
# MAGIC ### Importância
# MAGIC
# MAGIC As coordenadas possibilitam análises geoespaciais e construção de mapas de cobertura dos pontos de atendimento.

# COMMAND ----------

# Verificar quantos registros possuem
# latitude ou longitude zeradas

df_tratado.filter(
    (df_tratado.latitude == "0.00000") |
    (df_tratado.longitude == "0.00000")
).count()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação das Coordenadas Geográficas
# MAGIC
# MAGIC Foi identificada uma inconsistência relevante nos dados geográficos.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC - Registros totais: 25.942
# MAGIC - Registros com coordenadas zeradas: 13.052
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A base possui coordenadas geográficas parcialmente preenchidas.
# MAGIC
# MAGIC ### Impacto
# MAGIC
# MAGIC Análises geoespaciais deverão considerar a existência de registros sem localização válida.

# COMMAND ----------

# Verificar a distribuição dos serviços

df_tratado.groupBy(
    "pix_saque",
    "pix_troco"
).count().show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação de Duplicidades
# MAGIC
# MAGIC Antes da persistência da camada tratada será realizada uma verificação de possíveis registros duplicados.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Garantir a qualidade e a integridade da base analítica.
# MAGIC
# MAGIC ### Chave Avaliada
# MAGIC
# MAGIC - cnpj_agente_saque

# COMMAND ----------

from pyspark.sql.functions import count

duplicados = (
    df_tratado
    .groupBy("cnpj_agente_saque")
    .agg(count("*").alias("quantidade"))
    .filter("quantidade > 1")
)

duplicados.count()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Investigação de Duplicidades
# MAGIC
# MAGIC Foi identificado que 363 CNPJs aparecem mais de uma vez na camada tratada.
# MAGIC
# MAGIC ### Hipóteses
# MAGIC
# MAGIC - Um mesmo agente pode possuir mais de um ponto de atendimento.
# MAGIC - Um mesmo CNPJ pode estar presente em diferentes endereços.
# MAGIC - As duplicidades podem representar comportamento válido do negócio.
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Analisar exemplos de CNPJs repetidos antes de aplicar qualquer regra de deduplicação.
# MAGIC ``

# COMMAND ----------

# Exibir alguns CNPJs que aparecem mais de uma vez

duplicados.orderBy(
    "quantidade",
    ascending=False
).show(20, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação de Qualidade dos CNPJs
# MAGIC
# MAGIC Durante a análise da camada tratada foram identificados CNPJs com múltiplas ocorrências.
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC Foram encontrados valores que aparentam representar placeholders ou identificadores genéricos.
# MAGIC
# MAGIC Exemplos:
# MAGIC
# MAGIC - 00000000000000
# MAGIC - 00011111111111
# MAGIC
# MAGIC ### Próximos Passos
# MAGIC
# MAGIC Avaliar a quantidade de registros associados a esses valores e definir uma estratégia de tratamento.

# COMMAND ----------

# Quantidade de registros com CNPJ zerado

df_tratado.filter(
    df_tratado.cnpj_agente_saque == "00000000000000"
).count()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência da Camada Tratada
# MAGIC
# MAGIC Após a normalização da estrutura aninhada, será criada a primeira versão da camada tratada.
# MAGIC
# MAGIC ### Características
# MAGIC
# MAGIC - Estrutura tabular.
# MAGIC - Sem arrays.
# MAGIC - Sem structs.
# MAGIC - Compatível com SQL e Power BI.
# MAGIC
# MAGIC ### Tabela
# MAGIC
# MAGIC default.pix_caixa_tratado
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC A camada tratada preserva os registros originais e mantém eventuais inconsistências identificadas para futuras análises de qualidade.

# COMMAND ----------

from pyspark.sql.functions import length

# Verificar os tamanhos existentes
# do campo cnpj_agente_saque

df_tratado.groupBy(
    length("cnpj_agente_saque").alias("tamanho")
).count().orderBy("tamanho").show()

# COMMAND ----------

# Ver exemplos dos registros associados
# ao possível CPF identificado

df_tratado.filter(
    df_tratado.cnpj_agente_saque == "00005939500110"
).show(
    truncate=False
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência da Camada Tratada
# MAGIC
# MAGIC Após a normalização dos dados, a primeira versão da camada tratada será persistida.
# MAGIC
# MAGIC ### Características
# MAGIC
# MAGIC - Estrutura tabular.
# MAGIC - Compatível com SQL.
# MAGIC - Compatível com Power BI.
# MAGIC - Sem estruturas aninhadas.
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC Durante a análise foram identificados possíveis identificadores institucionais e padrões de preenchimento diferenciados.
# MAGIC
# MAGIC Nenhuma regra de exclusão foi aplicada nesta versão para preservar a integridade da fonte original.
# MAGIC
# MAGIC ### Tabela
# MAGIC
# MAGIC default.pix_caixa_tratado%md
# MAGIC

# COMMAND ----------

# Persistir a primeira versão da camada tratada

df_tratado.write \
    .mode("overwrite") \
    .saveAsTable("default.pix_caixa_tratado")

print("Camada tratada criada com sucesso!")

# COMMAND ----------

spark.sql("""
SHOW TABLES IN default
""").show(truncate=False)