# Databricks notebook source
# MAGIC %md
# MAGIC # Projeto Caixa Pix
# MAGIC
# MAGIC ## Fase 3 - Análise Exploratória dos Dados
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Realizar análises exploratórias sobre os dados tratados dos pontos de atendimento Pix disponibilizados pela Caixa Econômica Federal.
# MAGIC
# MAGIC ### Fonte dos Dados
# MAGIC
# MAGIC Tabela tratada:
# MAGIC
# MAGIC default.pix_caixa_tratado
# MAGIC
# MAGIC ### Objetivos da Análise
# MAGIC
# MAGIC - Avaliar a distribuição dos pontos por estado;
# MAGIC - Avaliar a distribuição dos pontos por município;
# MAGIC - Investigar a qualidade dos dados;
# MAGIC - Identificar padrões geográficos;
# MAGIC - Produzir insumos para construção de indicadores e dashboards.
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC Os dados utilizados nesta fase já passaram pelo processo de normalização realizado na camada tratada.
# MAGIC
# MAGIC Nenhuma transformação adicional será realizada nesta etapa.

# COMMAND ----------

df_tratado = spark.table("default.pix_caixa_tratado")

# COMMAND ----------

# MAGIC %md
# MAGIC # Validação da Camada Tratada
# MAGIC
# MAGIC Antes do início das análises exploratórias será realizada a validação da quantidade de registros presentes na camada tratada.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Confirmar que nenhum registro foi perdido durante o processo de transformação.
# MAGIC
# MAGIC ## Critério
# MAGIC
# MAGIC A quantidade de registros da camada tratada deve ser igual à quantidade de registros da camada RAW.

# COMMAND ----------

# Ler a tabela tratada persistida

df_tratado = spark.table(
    "default.pix_caixa_tratado"
)

# Contar a quantidade de registros
# disponíveis para análise

df_tratado.count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Achado de Qualidade dos Dados
# MAGIC
# MAGIC Durante a análise da camada tratada foram identificados registros com o identificador:
# MAGIC
# MAGIC 00000000000000
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Quantidade de registros: 339
# MAGIC
# MAGIC ## Observação
# MAGIC
# MAGIC Também foram identificados outros registros iniciados por zeros que aparentam representar entidades válidas.
# MAGIC
# MAGIC Por esse motivo, nenhuma exclusão ou tratamento corretivo foi aplicado nesta etapa.
# MAGIC
# MAGIC Os dados foram mantidos para preservar a fidelidade da fonte original.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 1 - Distribuição por Estado
# MAGIC
# MAGIC A distribuição geográfica dos pontos de atendimento será analisada por unidade federativa.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar os estados com maior e menor quantidade de pontos de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Essa análise permite avaliar a concentração geográfica dos serviços e identificar padrões de cobertura nacional.

# COMMAND ----------

# Quantidade de pontos de atendimento por estado

df_tratado.groupBy(
    "estado"
).count().orderBy(
    "count",
    ascending=False
).show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Análise por Estado
# MAGIC
# MAGIC A distribuição dos pontos de atendimento Pix apresenta forte concentração em alguns estados brasileiros.
# MAGIC
# MAGIC ## Principais Resultados
# MAGIC
# MAGIC Top 5 estados por quantidade de pontos:
# MAGIC
# MAGIC 1. São Paulo (SP): 6.234
# MAGIC 2. Minas Gerais (MG): 3.135
# MAGIC 3. Rio Grande do Sul (RS): 2.073
# MAGIC 4. Rio de Janeiro (RJ): 1.709
# MAGIC 5. Paraná (PR): 1.682
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC - São Paulo concentra aproximadamente um quarto de todos os pontos identificados na base.
# MAGIC - A região Sudeste domina a distribuição nacional.
# MAGIC - Minas Gerais aparece como o segundo estado com maior quantidade de pontos.
# MAGIC - Rio Grande do Sul apresenta destaque mesmo possuindo população inferior a outros grandes estados.
# MAGIC
# MAGIC ## Próximos Passos
# MAGIC
# MAGIC Avaliar a distribuição dos pontos por município para identificar os principais centros de atendimento.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 2 - Distribuição por Município
# MAGIC
# MAGIC Após a análise por estado, será avaliada a distribuição dos pontos de atendimento por município.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar os municípios com maior quantidade de pontos de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Esta análise permite identificar polos regionais de atendimento e avaliar a concentração da rede em grandes centros urbanos.

# COMMAND ----------

# Top 20 municípios por quantidade
# de pontos de atendimento

df_tratado.groupBy(
    "cidade"
).count().orderBy(
    "count",
    ascending=False
).show(20, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Análise por Município
# MAGIC
# MAGIC A distribuição dos pontos de atendimento por município apresenta forte concentração nas capitais e grandes centros urbanos.
# MAGIC
# MAGIC ## Principais Resultados
# MAGIC
# MAGIC Top 10 municípios por quantidade de pontos:
# MAGIC
# MAGIC 1. São Paulo (SP): 1.848
# MAGIC 2. Rio de Janeiro (RJ): 844
# MAGIC 3. Belo Horizonte (MG): 548
# MAGIC 4. Brasília (DF): 512
# MAGIC 5. Porto Alegre (RS): 404
# MAGIC 6. Salvador (BA): 374
# MAGIC 7. Curitiba (PR): 340
# MAGIC 8. Fortaleza (CE): 283
# MAGIC 9. Goiânia (GO): 250
# MAGIC 10. Recife (PE): 228
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC - A cidade de São Paulo lidera com ampla vantagem.
# MAGIC - As capitais dominam a distribuição dos pontos.
# MAGIC - Brasília aparece em quarto lugar mesmo sem ser um estado.
# MAGIC - Existe forte concentração da rede em grandes centros urbanos.
# MAGIC
# MAGIC ## Próximos Passos
# MAGIC
# MAGIC Avaliar a qualidade das coordenadas geográficas presentes na base de dados.

# COMMAND ----------

# Avaliar a qualidade das coordenadas geográficas

df_tratado.groupBy(
    (df_tratado.latitude == "0.00000").alias("coordenada_zerada")
).count().show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Avaliação das Coordenadas Geográficas
# MAGIC
# MAGIC Foi realizada uma análise da disponibilidade das coordenadas geográficas presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Registros com coordenadas zeradas:
# MAGIC - 13.052
# MAGIC
# MAGIC Registros com coordenadas válidas:
# MAGIC - 12.890
# MAGIC
# MAGIC ## Percentuais
# MAGIC
# MAGIC - Coordenadas zeradas: 50,3%
# MAGIC - Coordenadas válidas: 49,7%
# MAGIC
# MAGIC ## Impacto
# MAGIC
# MAGIC A base permite análises geográficas e construção de mapas, porém aproximadamente metade dos registros apresenta coordenadas indisponíveis.
# MAGIC
# MAGIC ## Observação
# MAGIC
# MAGIC As coordenadas inválidas foram preservadas para manter a fidelidade dos dados disponibilizados pela fonte oficial.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 3 - Cobertura Municipal
# MAGIC
# MAGIC Será avaliada a quantidade de municípios distintos presentes na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar a abrangência territorial dos pontos de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC A quantidade de municípios atendidos permite mensurar a capilaridade da rede em âmbito nacional.

# COMMAND ----------

# Quantidade de municípios distintos

df_tratado.select(
    "cidade"
).distinct().count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Cobertura Municipal
# MAGIC
# MAGIC Foi realizada a contagem de municípios distintos presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Municípios distintos identificados:
# MAGIC
# MAGIC - 5.281
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A rede de pontos de atendimento Pix apresenta ampla capilaridade territorial, estando presente em milhares de municípios brasileiros.
# MAGIC
# MAGIC ## Observação
# MAGIC
# MAGIC O resultado sugere cobertura nacional significativa dos serviços de Pix Saque e Pix Troco disponibilizados na base analisada.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 4 - Cobertura por Unidade Federativa
# MAGIC
# MAGIC Será avaliada a quantidade de unidades federativas presentes na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Verificar a abrangência estadual da rede de pontos de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Confirmar se os serviços estão distribuídos nacionalmente ou concentrados em determinadas regiões.

# COMMAND ----------

# Quantidade de estados distintos

df_tratado.select(
    "estado"
).distinct().count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Cobertura Estadual
# MAGIC
# MAGIC Foi realizada a contagem das unidades federativas presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Unidades federativas identificadas:
# MAGIC
# MAGIC - 27
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A base contempla todas as unidades federativas brasileiras, incluindo o Distrito Federal.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC Os pontos de atendimento Pix analisados apresentam cobertura nacional, estando distribuídos em todos os estados brasileiros.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 5 - Municípios com Apenas um Ponto de Atendimento
# MAGIC
# MAGIC Será avaliada a quantidade de municípios que possuem apenas um ponto de atendimento cadastrado.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar o nível de dispersão da rede de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Permite compreender se a cobertura está concentrada em grandes centros ou distribuída em municípios de menor porte.

# COMMAND ----------

# Quantidade de municípios que possuem
# apenas um ponto de atendimento

df_tratado.groupBy(
    "cidade"
).count().filter(
    "count = 1"
).count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Análise de Dispersão da Rede
# MAGIC
# MAGIC Foi avaliada a quantidade de municípios que possuem apenas um ponto de atendimento cadastrado.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Municípios com apenas um ponto de atendimento:
# MAGIC
# MAGIC - 2.295
# MAGIC
# MAGIC Municípios identificados na base:
# MAGIC
# MAGIC - 5.281
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC Aproximadamente 43,5% dos municípios presentes na base possuem apenas um ponto de atendimento cadastrado.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC A rede apresenta elevada capilaridade territorial, alcançando um grande número de municípios com baixa concentração de pontos.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 6 - Município com Maior Quantidade de Pontos
# MAGIC
# MAGIC Será identificado o município com a maior quantidade de pontos de atendimento cadastrados.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar o principal polo de concentração dos serviços na base analisada.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Permite avaliar o grau de concentração dos pontos em grandes centros urbanos.

# COMMAND ----------

# Município com maior quantidade
# de pontos de atendimento

df_tratado.groupBy

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 6 - Município com Maior Quantidade de Pontos
# MAGIC
# MAGIC Será identificado o município com maior quantidade de pontos de atendimento cadastrados.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar o principal polo de concentração da rede de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Permite avaliar o grau de concentração da rede em grandes centros urbanos.

# COMMAND ----------

# Município com maior quantidade
# de pontos de atendimento

df_tratado.groupBy(
    "cidade"
).count().orderBy(
    "count",
    ascending=False
).limit(1).show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Análise de Concentração Municipal
# MAGIC
# MAGIC Foi identificado o município com maior quantidade de pontos de atendimento cadastrados.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Município líder:
# MAGIC
# MAGIC - São Paulo (SP): 1.848 pontos
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A cidade de São Paulo concentra a maior quantidade de pontos de atendimento da base analisada.
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC O resultado é compatível com a posição da cidade como maior centro econômico e populacional do país.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC A rede de atendimento apresenta forte presença na capital paulista, que se destaca como principal polo de concentração dos serviços.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 7 - Percentual de Coordenadas Válidas
# MAGIC
# MAGIC Será calculado o percentual de registros que possuem coordenadas geográficas válidas.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Mensurar a qualidade da informação geográfica disponível na base.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Este indicador permite avaliar o potencial de utilização dos dados para análises espaciais e visualizações em mapas.

# COMMAND ----------

# Quantidade total de registros

total_registros = df_tratado.count()

# Quantidade de registros com coordenadas válidas

coordenadas_validas = df_tratado.filter(
    (df_tratado.latitude != "0.00000") &
    (df_tratado.longitude != "0.00000")
).count()

# Percentual

round(
    (coordenadas_validas / total_registros) * 100,
    2
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 7 - Distribuição por Região
# MAGIC
# MAGIC Será realizada uma análise da distribuição dos pontos de atendimento por região do Brasil.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar quais regiões concentram a maior quantidade de pontos de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC A análise regional permite avaliar o equilíbrio da cobertura nacional e identificar concentrações geográficas.

# COMMAND ----------

# Distribuição dos pontos por estado
# para posterior agrupamento regional

df_tratado.groupBy(
    "estado"
).count().orderBy(
    "count",
    ascending=False
).show(30)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Distribuição por Estado
# MAGIC
# MAGIC A análise evidenciou forte concentração dos pontos de atendimento em estados das regiões Sudeste e Sul.
# MAGIC
# MAGIC ## Estados com Maior Quantidade de Pontos
# MAGIC
# MAGIC - São Paulo (SP): 6.234
# MAGIC - Minas Gerais (MG): 3.135
# MAGIC - Rio Grande do Sul (RS): 2.073
# MAGIC - Rio de Janeiro (RJ): 1.709
# MAGIC - Paraná (PR): 1.682
# MAGIC
# MAGIC ## Estados com Menor Quantidade de Pontos
# MAGIC
# MAGIC - Amapá (AP): 46
# MAGIC - Roraima (RR): 52
# MAGIC - Acre (AC): 77
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC Embora a cobertura seja nacional, existe uma concentração significativa de pontos de atendimento em estados mais populosos e economicamente relevantes.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 8 - Média de Pontos por Município
# MAGIC
# MAGIC Será calculada a média de pontos de atendimento por município.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Avaliar o nível médio de cobertura da rede nos municípios presentes na base.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC O indicador permite compreender o grau de concentração dos pontos de atendimento.

# COMMAND ----------

# Média de pontos por município

round(
    25942 / 5281,
    2
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Média de Pontos por Município
# MAGIC
# MAGIC Foi calculada a média de pontos de atendimento por município.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Média de pontos por município:
# MAGIC
# MAGIC - 4,91
# MAGIC
# MAGIC ## Observação
# MAGIC
# MAGIC A média deve ser interpretada com cautela, pois existem municípios com apenas um ponto de atendimento e grandes centros urbanos com quantidade significativamente superior à média.
# MAGIC
# MAGIC ## Evidências
# MAGIC
# MAGIC - 2.295 municípios possuem apenas um ponto de atendimento.
# MAGIC - São Paulo possui 1.848 pontos de atendimento.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 9 - Municípios com Alta Concentração de Pontos
# MAGIC
# MAGIC Será avaliada a quantidade de municípios que possuem dez ou mais pontos de atendimento.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar a presença de municípios com elevada concentração de pontos.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Permite avaliar o grau de concentração da rede em centros urbanos de maior porte.

# COMMAND ----------

# Quantidade de municípios com
# 10 ou mais pontos de atendimento

df_tratado.groupBy(
    "cidade"
).count().filter(
    "count >= 10"
).count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Concentração de Pontos por Município
# MAGIC
# MAGIC Foi analisada a quantidade de municípios que possuem dez ou mais pontos de atendimento.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Municípios com 10 ou mais pontos:
# MAGIC
# MAGIC - 355
# MAGIC
# MAGIC Municípios identificados na base:
# MAGIC
# MAGIC - 5.281
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC Apenas uma pequena parcela dos municípios possui alta concentração de pontos de atendimento.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC A rede apresenta elevado grau de dispersão territorial, com a maior parte dos municípios operando com poucos pontos de atendimento.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 10 - Cobertura por Agente
# MAGIC
# MAGIC Será avaliada a quantidade de agentes distintos presentes na base.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar quantas entidades diferentes operam os pontos de atendimento cadastrados.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC Permite avaliar a diversidade de participantes da rede de atendimento Pix.

# COMMAND ----------

# Quantidade de agentes distintos

df_tratado.select(
    "cnpj_agente_saque"
).distinct().count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Análise de Agentes
# MAGIC
# MAGIC Foi avaliada a quantidade de agentes distintos presentes na base.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC Agentes distintos identificados:
# MAGIC
# MAGIC - 25.003
# MAGIC
# MAGIC Pontos de atendimento identificados:
# MAGIC
# MAGIC - 25.942
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC A diferença entre a quantidade de agentes e a quantidade de pontos de atendimento é reduzida.
# MAGIC
# MAGIC ## Evidências
# MAGIC
# MAGIC - Foram identificados apenas 363 identificadores associados a mais de um ponto.
# MAGIC - A maior parte dos agentes aparece uma única vez na base.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC A rede apresenta elevada diversidade de participantes, com baixa concentração de múltiplos pontos sob o mesmo identificador.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Resumo dos Principais Achados
# MAGIC
# MAGIC Até o momento foram identificados os seguintes resultados:
# MAGIC
# MAGIC ## Cobertura Nacional
# MAGIC
# MAGIC - 27 unidades federativas.
# MAGIC - 5.281 municípios.
# MAGIC
# MAGIC ## Rede de Atendimento
# MAGIC
# MAGIC - 25.942 pontos de atendimento.
# MAGIC - 25.003 agentes distintos.
# MAGIC
# MAGIC ## Concentração
# MAGIC
# MAGIC - São Paulo possui 6.234 pontos.
# MAGIC - A cidade de São Paulo possui 1.848 pontos.
# MAGIC
# MAGIC ## Capilaridade
# MAGIC
# MAGIC - 2.295 municípios possuem apenas um ponto.
# MAGIC - 355 municípios possuem dez ou mais pontos.
# MAGIC
# MAGIC ## Qualidade dos Dados
# MAGIC
# MAGIC - 49,7% dos registros possuem coordenadas válidas.
# MAGIC - 50,3% possuem coordenadas zeradas.
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC Foram identificados registros com identificadores especiais ou não convencionais, mantidos para preservar a fidelidade da fonte original.

# COMMAND ----------

# MAGIC %md
# MAGIC # Preparação do Ambiente
# MAGIC
# MAGIC Como as análises exploratórias utilizam a camada tratada persistida, será realizada a leitura da tabela para disponibilização dos dados na sessão atual.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Recuperar a camada tratada previamente persistida para continuidade das análises.
# MAGIC
# MAGIC ## Fonte
# MAGIC
# MAGIC default.pix_caixa_tratado

# COMMAND ----------

# Ler novamente a camada tratada

df_tratado = spark.table(
    "default.pix_caixa_tratado"
)

print("Tabela carregada com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 11 - Municípios com Maior Concentração de Pontos
# MAGIC
# MAGIC Será realizada a identificação dos municípios com maior quantidade de pontos de atendimento.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar os principais polos de concentração da rede de atendimento Pix.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC A análise permite compreender quais municípios exercem maior relevância na distribuição dos pontos de atendimento.

# COMMAND ----------

# Top 10 municípios com maior quantidade
# de pontos de atendimento

df_tratado.groupBy(
    "cidade"
).count().orderBy(
    "count",
    ascending=False
).show(10, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado dos Municípios com Maior Concentração de Pontos
# MAGIC
# MAGIC Foi identificada a concentração dos pontos de atendimento nos principais centros urbanos do país.
# MAGIC
# MAGIC ## Top 10 Municípios
# MAGIC
# MAGIC 1. São Paulo (SP): 1.848
# MAGIC 2. Rio de Janeiro (RJ): 844
# MAGIC 3. Belo Horizonte (MG): 548
# MAGIC 4. Brasília (DF): 512
# MAGIC 5. Porto Alegre (RS): 404
# MAGIC 6. Salvador (BA): 374
# MAGIC 7. Curitiba (PR): 340
# MAGIC 8. Fortaleza (CE): 283
# MAGIC 9. Goiânia (GO): 250
# MAGIC 10. Recife (PE): 228
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC - A cidade de São Paulo apresenta mais que o dobro da quantidade de pontos observada na cidade do Rio de Janeiro.
# MAGIC - Todas as cidades do Top 10 são capitais estaduais.
# MAGIC - A distribuição reforça a concentração da rede em grandes centros urbanos.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 12 - Cobertura Média por Município
# MAGIC
# MAGIC Será avaliada a quantidade média de agentes por município em cada estado.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar estados que apresentam maior densidade de atendimento.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC A análise possibilita comparar a intensidade da cobertura entre estados, independentemente do seu tamanho territorial.

# COMMAND ----------

# Quantidade de municípios e agentes por estado

from pyspark.sql.functions import countDistinct

df_tratado.groupBy("estado").agg(
    countDistinct("cidade").alias("municipios"),
    countDistinct("cnpj_agente_saque").alias("agentes")
).show(30)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado Parcial da Cobertura Estadual
# MAGIC
# MAGIC Foi realizado o levantamento da quantidade de municípios e agentes por unidade federativa.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Preparar os dados para cálculo da densidade média de agentes por município em cada estado.
# MAGIC
# MAGIC ## Observação
# MAGIC
# MAGIC Estados com menor quantidade de municípios podem apresentar maior densidade de atendimento quando comparados aos estados mais extensos.

# COMMAND ----------

# Criar a métrica de agentes por município

from pyspark.sql.functions import col, round

cobertura_estado = df_tratado.groupBy(
    "estado"
).agg(
    countDistinct("cidade").alias("municipios"),
    countDistinct("cnpj_agente_saque").alias("agentes")
)

cobertura_estado.withColumn(
    "agentes_por_municipio",
    round(
        col("agentes") / col("municipios"),
        2
    )
).orderBy(
    "agentes_por_municipio",
    ascending=False
).show(10)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Densidade de Atendimento por Estado
# MAGIC
# MAGIC Foi calculada a quantidade média de agentes por município em cada unidade federativa.
# MAGIC
# MAGIC ## Principais Resultados
# MAGIC
# MAGIC Desconsiderando a particularidade do Distrito Federal, os estados com maior densidade de agentes por município foram:
# MAGIC
# MAGIC 1. Rio de Janeiro (RJ): 18,10
# MAGIC 2. São Paulo (SP): 9,36
# MAGIC 3. Espírito Santo (ES): 5,91
# MAGIC 4. Amazonas (AM): 5,35
# MAGIC 5. Pernambuco (PE): 4,64
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC - O Distrito Federal foi desconsiderado da comparação por apresentar apenas uma cidade registrada na base, o que distorce a métrica de agentes por município.
# MAGIC - O Rio de Janeiro destaca-se pela elevada concentração de agentes em relação à quantidade de municípios.
# MAGIC - São Paulo combina alta quantidade absoluta de agentes com elevada densidade municipal.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC Os dados indicam que estados mais urbanizados apresentam maior concentração de pontos de atendimento por município.

# COMMAND ----------

# MAGIC %md
# MAGIC # Análise 13 - Estados com Maior Participação na Rede
# MAGIC
# MAGIC Será avaliada a concentração dos pontos de atendimento nos principais estados da federação.
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Identificar o nível de concentração da rede de atendimento Pix no território nacional.
# MAGIC
# MAGIC ## Importância
# MAGIC
# MAGIC A análise permite verificar se a cobertura está distribuída de forma homogênea ou concentrada em poucos estados.

# COMMAND ----------

# Top 10 estados com mais pontos

df_tratado.groupBy(
    "estado"
).count().orderBy(
    "count",
    ascending=False
).show(10)

# COMMAND ----------

# MAGIC %md
# MAGIC # Resultado da Concentração por Estado
# MAGIC
# MAGIC Foi analisada a participação dos estados com maior quantidade de pontos de atendimento.
# MAGIC
# MAGIC ## Principais Resultados
# MAGIC
# MAGIC Top 10 estados:
# MAGIC
# MAGIC 1. SP - 6.234
# MAGIC 2. MG - 3.135
# MAGIC 3. RS - 2.073
# MAGIC 4. RJ - 1.709
# MAGIC 5. PR - 1.682
# MAGIC 6. BA - 1.476
# MAGIC 7. SC - 1.044
# MAGIC 8. GO - 906
# MAGIC 9. PE - 880
# MAGIC 10. CE - 707
# MAGIC
# MAGIC ## Interpretação
# MAGIC
# MAGIC Os dez estados com maior quantidade de pontos concentram aproximadamente três quartos de toda a rede analisada.
# MAGIC
# MAGIC ## Conclusão
# MAGIC
# MAGIC Apesar da cobertura nacional, a distribuição dos pontos apresenta forte concentração em um grupo reduzido de estados.

# COMMAND ----------

# MAGIC %md
# MAGIC # Inventário de Indicadores e Estruturas Utilizadas
# MAGIC
# MAGIC Este resumo consolida os principais campos analisados, métricas calculadas e indicadores produzidos durante a fase de análise exploratória.
# MAGIC
# MAGIC ## Estrutura Utilizada
# MAGIC
# MAGIC Tabela analisada:
# MAGIC
# MAGIC default.pix_caixa_tratado
# MAGIC
# MAGIC ### Colunas Disponíveis
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
# MAGIC ## Indicadores Produzidos
# MAGIC
# MAGIC ### Cobertura Nacional
# MAGIC
# MAGIC - 27 unidades federativas.
# MAGIC - 5.281 municípios distintos.
# MAGIC
# MAGIC ### Rede de Atendimento
# MAGIC
# MAGIC - 25.942 pontos de atendimento.
# MAGIC - 25.003 agentes distintos.
# MAGIC
# MAGIC ### Concentração Estadual
# MAGIC
# MAGIC Top estados por quantidade de pontos:
# MAGIC
# MAGIC - SP: 6.234
# MAGIC - MG: 3.135
# MAGIC - RS: 2.073
# MAGIC - RJ: 1.709
# MAGIC - PR: 1.682
# MAGIC
# MAGIC ### Concentração Municipal
# MAGIC
# MAGIC Top municípios por quantidade de pontos:
# MAGIC
# MAGIC - São Paulo: 1.848
# MAGIC - Rio de Janeiro: 844
# MAGIC - Belo Horizonte: 548
# MAGIC - Brasília: 512
# MAGIC - Porto Alegre: 404
# MAGIC
# MAGIC ### Capilaridade
# MAGIC
# MAGIC - 2.295 municípios possuem apenas um ponto de atendimento.
# MAGIC - 355 municípios possuem dez ou mais pontos de atendimento.
# MAGIC
# MAGIC ### Qualidade Geográfica
# MAGIC
# MAGIC - 12.890 registros possuem coordenadas válidas.
# MAGIC - 13.052 registros possuem coordenadas zeradas.
# MAGIC - 49,7% dos registros possuem coordenadas válidas.
# MAGIC - 50,3% dos registros possuem coordenadas zeradas.
# MAGIC
# MAGIC ### Qualidade dos Identificadores
# MAGIC
# MAGIC - 339 registros apresentam identificador 00000000000000.
# MAGIC - Foram identificados identificadores especiais ou não convencionais.
# MAGIC - Os registros foram preservados para manter a fidelidade da fonte oficial.
# MAGIC
# MAGIC ## Observações
# MAGIC
# MAGIC Os indicadores produzidos nesta etapa servirão como base para a construção das consultas SQL, dos KPIs analíticos e do dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusão da Análise Exploratória
# MAGIC
# MAGIC A análise exploratória permitiu identificar características relevantes da rede de pontos de atendimento Pix disponibilizada pela Caixa Econômica Federal.
# MAGIC
# MAGIC ## Principais Achados
# MAGIC
# MAGIC - Cobertura nacional em todas as unidades federativas.
# MAGIC - Presença em 5.281 municípios.
# MAGIC - Rede composta por 25.942 pontos de atendimento.
# MAGIC - Presença de 25.003 agentes distintos.
# MAGIC - Forte concentração da rede nos estados mais populosos.
# MAGIC - Elevada capilaridade territorial.
# MAGIC - Disponibilidade parcial de coordenadas geográficas.
# MAGIC - Existência de identificadores especiais ou não convencionais mantidos para preservar a fidelidade da fonte original.
# MAGIC
# MAGIC ## Próxima Etapa
# MAGIC
# MAGIC Construção de consultas analíticas e indicadores na camada SQL para suporte ao dashboard final do projeto.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Possíveis Evoluções
# MAGIC
# MAGIC As análises realizadas nesta etapa consideram apenas os dados disponibilizados pela API da Caixa.
# MAGIC
# MAGIC Em etapas futuras, a base poderá ser enriquecida com informações externas, como:
# MAGIC
# MAGIC - População por estado;
# MAGIC - Produto Interno Bruto (PIB);
# MAGIC - PIB per capita;
# MAGIC - Densidade populacional.
# MAGIC
# MAGIC O enriquecimento permitirá análises relativas e comparativas sobre a cobertura da rede de atendimento Pix.