# Databricks notebook source
# MAGIC %md
# MAGIC Projeto: Análise da Cobertura dos Pontos de Atendimento Pix Saque e Pix Troco da Caixa Econômica Federal

# COMMAND ----------

# MAGIC %md
# MAGIC Objetivo
# MAGIC Este projeto tem como objetivo analisar a distribuição geográfica dos pontos de atendimento Pix Saque e Pix Troco da Caixa Econômica Federal no Brasil.
# MAGIC
# MAGIC A análise busca identificar padrões de cobertura regional, concentração de pontos de atendimento e oportunidades de expansão dos serviços financeiros.
# MAGIC
# MAGIC O projeto será desenvolvido utilizando Databricks, Python, SQL e Power BI.

# COMMAND ----------

# MAGIC %md
# MAGIC Fonte dos Dados
# MAGIC Os dados são obtidos por meio da API oficial de Dados Abertos da Caixa Econômica Federal.
# MAGIC
# MAGIC API: Pix Saque e Pix Troco
# MAGIC
# MAGIC URL: https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1/
# MAGIC
# MAGIC Origem: Dados Abertos do Sistema Financeiro Nacional (Banco Central do Brasil).

# COMMAND ----------

# MAGIC %md
# MAGIC Perguntas de Negócio
# MAGIC Quantos pontos de atendimento existem no Brasil?
# MAGIC Quais estados possuem maior quantidade de pontos?
# MAGIC Quais estados possuem menor cobertura?
# MAGIC Como os pontos estão distribuídos entre as regiões brasileiras?
# MAGIC Existem municípios com baixa cobertura de atendimento?
# MAGIC Quais oportunidades de expansão podem ser identificadas?

# COMMAND ----------

# MAGIC %md
# MAGIC Tecnologias Utilizadas
# MAGIC Databricks
# MAGIC Python
# MAGIC SQL
# MAGIC Apache Spark
# MAGIC Power BI
# MAGIC Dados Abertos da Caixa Econômica Federal

# COMMAND ----------

# MAGIC %md
# MAGIC Metodologia
# MAGIC Coleta dos dados via API.
# MAGIC Exploração da estrutura dos dados.
# MAGIC Limpeza e tratamento.
# MAGIC Criação das tabelas analíticas.
# MAGIC Construção dos indicadores de negócio.
# MAGIC Desenvolvimento do dashboard.
# MAGIC Geração de insights.

# COMMAND ----------

# Inicialização do projeto Caixa
print("Projeto Caixa iniciado!")


# COMMAND ----------

# Importa a biblioteca requests para fazer requisições HTTP
import requests

# Define a URL do endpoint da API de dados abertos da Caixa (Pontos Pix)
url = "https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1/"

# Realiza a requisição GET para o endpoint
response = requests.get(url)

# Exibe o código de status da resposta (200 = sucesso)
print(response.status_code)

# COMMAND ----------

# Importa a biblioteca requests para fazer requisições HTTP
import requests

# Define a URL do endpoint da API de dados abertos da Caixa (Pontos Pix)
url = "https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1/"

# Realiza a requisição GET para o endpoint
response = requests.get(url)

# Converte o corpo da resposta (JSON) em um objeto Python (geralmente um dict ou lista)
dados = response.json()

# Exibe o tipo do objeto retornado para inspecionar a estrutura dos dados
print(type(dados))

# COMMAND ----------

dados.keys()

# COMMAND ----------

# MAGIC %md
# MAGIC Exploração Inicial da API
# MAGIC A API foi acessada com sucesso a partir do Databricks.
# MAGIC
# MAGIC Endpoint
# MAGIC https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1/
# MAGIC
# MAGIC Teste de Conectividade
# MAGIC Foi realizada uma requisição HTTP para validar o acesso ao endpoint.
# MAGIC
# MAGIC Resultado:
# MAGIC
# MAGIC Status Code: 200
# MAGIC Conexão estabelecida com sucesso
# MAGIC Estrutura Inicial Identificada
# MAGIC O retorno da API foi identificado como um objeto do tipo:
# MAGIC
# MAGIC dict
# MAGIC As chaves encontradas na resposta foram:
# MAGIC
# MAGIC dict_keys(['links', 'meta', 'registros'])
# MAGIC Interpretação Inicial
# MAGIC links: informações de navegação da API
# MAGIC meta: metadados do conjunto de dados
# MAGIC registros: dados de negócio que serão utilizados nas análises
# MAGIC Próximos Passos
# MAGIC Inspecionar a estrutura de "registros"
# MAGIC Identificar os campos disponíveis
# MAGIC Transformar os dados em DataFrame Spark
# MAGIC Realizar análise exploratória
# MAGIC Construir indicadores de negócio `

# COMMAND ----------

print(type(dados['registros']))

# COMMAND ----------

# MAGIC %md
# MAGIC Estrutura dos Dados
# MAGIC Após a inspeção inicial da API, identificamos que a chave registros contém os dados principais do projeto.
# MAGIC
# MAGIC Resultado da análise
# MAGIC type(dados['registros'])
# MAGIC Retorno:
# MAGIC
# MAGIC <class 'list'>
# MAGIC Interpretação
# MAGIC A API retorna uma lista de registros, onde cada elemento provavelmente representa um ponto de atendimento Pix Saque ou Pix Troco.
# MAGIC
# MAGIC O próximo passo será inspecionar um registro individual para identificar os campos disponíveis para análise.

# COMMAND ----------

dados['registros'][0]

# COMMAND ----------

# MAGIC %md
# MAGIC Estrutura Hierárquica dos Dados
# MAGIC A API possui uma estrutura hierárquica composta por três níveis principais.
# MAGIC
# MAGIC Nível 1 - Agente de Saque
# MAGIC Informações da empresa ou estabelecimento responsável pelo atendimento.
# MAGIC
# MAGIC Exemplos:
# MAGIC
# MAGIC CNPJ do agente
# MAGIC Nome do agente
# MAGIC Nível 2 - Ponto de Atendimento
# MAGIC Informações geográficas do local de atendimento.
# MAGIC
# MAGIC Exemplos:
# MAGIC
# MAGIC Cidade
# MAGIC Estado
# MAGIC CEP
# MAGIC Bairro
# MAGIC Latitude
# MAGIC Longitude
# MAGIC Nível 3 - Horários de Funcionamento
# MAGIC Informações de disponibilidade por dia da semana.
# MAGIC
# MAGIC Exemplos:
# MAGIC
# MAGIC Dia da semana
# MAGIC Horário de abertura
# MAGIC Horário de fechamento
# MAGIC Estratégia Analítica
# MAGIC Para as análises de cobertura geográfica, utilizaremos principalmente os dados dos pontos de atendimento (Nível 2), pois eles contêm as informações de localização necessárias para os indicadores de negócio.

# COMMAND ----------

len(dados['registros'])

# COMMAND ----------

# MAGIC %md
# MAGIC Quantidade Inicial de Registros
# MAGIC Foi realizada uma contagem dos registros retornados pela API.
# MAGIC
# MAGIC Resultado
# MAGIC len(dados['registros'])
# MAGIC Retorno:
# MAGIC
# MAGIC 100
# MAGIC Observação
# MAGIC Os 100 registros representam agentes de saque retornados pela API.
# MAGIC
# MAGIC Cada agente pode possuir um ou mais pontos de atendimento.
# MAGIC
# MAGIC Portanto, a quantidade total de pontos de atendimento ainda será calculada após a normalização dos dados.

# COMMAND ----------

dados['registros'][0].keys()

# COMMAND ----------

# MAGIC %md
# MAGIC Estrutura dos Agentes
# MAGIC
# MAGIC Cada registro da API representa um agente autorizado a oferecer Pix Saque ou Pix Troco.
# MAGIC
# MAGIC Campos identificados:
# MAGIC
# MAGIC Campo	Descrição
# MAGIC cnpj_agente_saque	CNPJ do agente
# MAGIC nome_agente_saque	Nome do agente
# MAGIC pontos_atendimento	Lista de pontos de atendimento vinculados ao agente
# MAGIC Estratégia
# MAGIC A análise será realizada no nível dos pontos de atendimento, pois é nesse nível que estão disponíveis as informações geográficas necessárias para o estudo de cobertura.

# COMMAND ----------

len(dados['registros'][0]['pontos_atendimento'])

# COMMAND ----------

# MAGIC %md
# MAGIC Análise Inicial dos Pontos de Atendimento
# MAGIC Foi realizada a contagem dos pontos de atendimento associados ao primeiro agente retornado pela API.
# MAGIC
# MAGIC Resultado
# MAGIC len(dados['registros'][0]['pontos_atendimento'])

# COMMAND ----------

dados['registros'][0]['pontos_atendimento'][0].keys()

# COMMAND ----------

# MAGIC %md
# MAGIC Campos Identificados nos Pontos de Atendimento
# MAGIC
# MAGIC Foram identificados os seguintes campos para cada ponto de atendimento:
# MAGIC
# MAGIC Dados Geográficos
# MAGIC bairro
# MAGIC cep
# MAGIC cidade
# MAGIC estado
# MAGIC latitude
# MAGIC longitude
# MAGIC logradouro
# MAGIC Dados Operacionais
# MAGIC horarios_funcionamento
# MAGIC Dados de Serviço
# MAGIC produtos
# MAGIC Outros Campos
# MAGIC observacoes
# MAGIC Relevância para o Projeto
# MAGIC Os campos geográficos serão utilizados para:
# MAGIC
# MAGIC mapas
# MAGIC análise regional
# MAGIC cobertura estadual
# MAGIC cobertura municipal
# MAGIC Os campos de produtos serão utilizados para entender os serviços disponibilizados em cada ponto de atendimento.

# COMMAND ----------

dados['registros'][0]['pontos_atendimento'][0]['produtos']

# COMMAND ----------

# MAGIC %md
# MAGIC Serviços Disponíveis
# MAGIC
# MAGIC Foi realizada a inspeção do campo produtos.
# MAGIC
# MAGIC Resultado
# MAGIC {
# MAGIC     'Pix-saque': True,
# MAGIC     'Pix-troco': True
# MAGIC }
# MAGIC Interpretação
# MAGIC O ponto de atendimento analisado disponibiliza ambos os serviços:
# MAGIC
# MAGIC Pix Saque
# MAGIC Pix Troco
# MAGIC Essas informações poderão ser utilizadas futuramente para análises de disponibilidade dos serviços por região, estado ou município.

# COMMAND ----------

# Exibir os metadados retornados pela API
# Os metadados normalmente informam paginação,
# quantidade total de registros e outras informações úteis

dados['meta']

# COMMAND ----------

# MAGIC %md
# MAGIC Análise dos Metadados da API
# MAGIC
# MAGIC Os metadados foram inspecionados para identificar o volume total de dados disponíveis.
# MAGIC
# MAGIC Resultado
# MAGIC
# MAGIC dados['meta']
# MAGIC
# MAGIC Retorno:
# MAGIC
# MAGIC {
# MAGIC     'data_hora_geracao_dados': '2026-10-17T11:47:41',
# MAGIC     'ispb_transmissora': '00360305',
# MAGIC     'nome_transmissora': 'Caixa Economica Federal',
# MAGIC     'total_paginas': 260,
# MAGIC     'total_registros': 25942
# MAGIC }
# MAGIC
# MAGIC Conclusões
# MAGIC
# MAGIC - A base contém 25.942 registros.
# MAGIC - Os dados estão distribuídos em 260 páginas.
# MAGIC - Os 100 registros inicialmente carregados representam apenas uma parte da base.
# MAGIC - Será necessário implementar uma estratégia de coleta paginada para obter todos os registros disponíveis.

# COMMAND ----------

# Exibir as informações de navegação da API
# Vamos verificar como acessar as demais páginas

dados['links']

# COMMAND ----------

# Testar o acesso à segunda página da API

import requests

url_pagina_2 = "https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1?page=2&page-size=100"

response_pagina_2 = requests.get(url_pagina_2)

response_pagina_2.status_code

# COMMAND ----------

# MAGIC %md
# MAGIC ## Navegação da API
# MAGIC
# MAGIC A inspeção da chave `links` mostrou que a API utiliza paginação.
# MAGIC
# MAGIC ### Informações encontradas
# MAGIC
# MAGIC - Primeira página: page=1
# MAGIC - Última página: page=260
# MAGIC - Próxima página disponível: page=2
# MAGIC - Tamanho da página: 100 registros
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A API não retorna todos os registros de uma única vez.
# MAGIC
# MAGIC Para obter os 25.942 registros disponíveis será necessário realizar uma coleta paginada percorrendo todas as 260 páginas.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validação do Tamanho das Páginas
# MAGIC
# MAGIC Após confirmar que a API permite navegação entre páginas, é necessário validar a quantidade de registros retornados por cada página.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Verificar se a página 2 possui a mesma quantidade de registros observada na página inicial.
# MAGIC
# MAGIC ### Importância
# MAGIC
# MAGIC Essa validação permitirá confirmar o padrão de paginação utilizado pela API e servirá de base para a implementação da coleta completa dos dados.
# MAGIC
# MAGIC ### O que será feito
# MAGIC
# MAGIC 1. Converter a resposta da página 2 para formato JSON.
# MAGIC 2. Contar a quantidade de registros retornados.
# MAGIC 3. Comparar o resultado com a página inicial.
# MAGIC 4. Confirmar a estratégia de coleta das 260 páginas.

# COMMAND ----------

# Converter a resposta da página 2 para formato JSON
# Isso permite acessar os dados retornados pela API

dados_pagina_2 = response_pagina_2.json()

# Contar quantos registros foram retornados na página 2
# O objetivo é validar o padrão de paginação da API

len(dados_pagina_2['registros'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultado da Validação
# MAGIC
# MAGIC A contagem dos registros da página 2 retornou 100 registros.
# MAGIC
# MAGIC ### Resultado Obtido
# MAGIC
# MAGIC 100 registros
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC O resultado confirma que a API utiliza um padrão de paginação de 100 registros por página.
# MAGIC
# MAGIC Esse comportamento está alinhado com as informações encontradas na chave `links`, que indica o parâmetro `page-size=100`.
# MAGIC
# MAGIC ### Impacto para o Projeto
# MAGIC
# MAGIC Com a validação concluída, já é possível planejar a coleta completa da base contendo 25.942 registros distribuídos em 260 páginas.
# MAGIC
# MAGIC Antes da extração completa, será necessário compreender como transformar a estrutura hierárquica dos dados em um formato tabular adequado para análise.

# COMMAND ----------

# Identificar quantos pontos de atendimento possui o segundo agente da lista
# Vamos verificar se todos os agentes possuem apenas um ponto

len(dados['registros'][1]['pontos_atendimento'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Investigação da Estrutura dos Agentes
# MAGIC
# MAGIC Foi iniciada uma análise para verificar quantos pontos de atendimento estão associados a cada agente.
# MAGIC
# MAGIC ### Resultados Obtidos
# MAGIC
# MAGIC - Agente 1: 1 ponto de atendimento
# MAGIC - Agente 2: 1 ponto de atendimento
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC Ainda não é possível afirmar que todos os agentes possuem apenas um ponto de atendimento.
# MAGIC
# MAGIC Será necessário analisar uma quantidade maior de registros para identificar possíveis exceções.
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Verificar a quantidade máxima de pontos de atendimento entre os agentes da amostra atual.

# COMMAND ----------

# Criar uma lista com a quantidade de pontos de atendimento
# de cada agente presente na página atual

quantidade_pontos = [
    len(registro['pontos_atendimento'])
    for registro in dados['registros']
]

# Identificar a maior quantidade de pontos encontrada
max(quantidade_pontos)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análise da Relação entre Agentes e Pontos de Atendimento
# MAGIC
# MAGIC Foi realizada uma verificação na primeira página da API para identificar a quantidade máxima de pontos de atendimento por agente.
# MAGIC
# MAGIC ### Metodologia
# MAGIC
# MAGIC Foi calculada a quantidade de pontos de atendimento associada a cada agente presente na página.
# MAGIC
# MAGIC Em seguida, foi identificado o maior valor encontrado.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC Quantidade máxima de pontos de atendimento por agente:
# MAGIC
# MAGIC 1
# MAGIC
# MAGIC ### Interpretação
# MAGIC
# MAGIC Na amostra analisada, todos os agentes possuem apenas um ponto de atendimento cadastrado.
# MAGIC
# MAGIC ### Impacto para o Projeto
# MAGIC
# MAGIC Caso esse padrão se mantenha nas demais páginas, cada registro da API poderá ser tratado diretamente como um ponto de atendimento.
# MAGIC
# MAGIC Isso simplifica significativamente as etapas de transformação e modelagem dos dados.

# COMMAND ----------

# Exibir o primeiro ponto de atendimento de forma estruturada
# Isso ajudará a definir quais colunas irão compor nossa tabela analítica

dados['registros'][0]['pontos_atendimento'][0]

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inspeção do Primeiro Ponto de Atendimento
# MAGIC
# MAGIC Foi realizada uma análise detalhada da estrutura de um ponto de atendimento retornado pela API.
# MAGIC
# MAGIC ### Campos Identificados
# MAGIC
# MAGIC - bairro
# MAGIC - cep
# MAGIC - cidade
# MAGIC - estado
# MAGIC - horarios_funcionamento
# MAGIC - latitude
# MAGIC - logradouro
# MAGIC - longitude
# MAGIC
# MAGIC ### Observações Iniciais
# MAGIC
# MAGIC Foi identificado que alguns registros podem apresentar coordenadas geográficas iguais a:
# MAGIC
# MAGIC - latitude = 0.00000
# MAGIC - longitude = 0.00000
# MAGIC
# MAGIC Esses valores podem indicar ausência da informação geográfica e deverão ser analisados na etapa de qualidade dos dados.
# MAGIC
# MAGIC ### Potenciais Colunas da Tabela Analítica
# MAGIC
# MAGIC Os seguintes campos apresentam potencial para utilização na análise:
# MAGIC
# MAGIC - cnpj_agente_saque
# MAGIC - nome_agente_saque
# MAGIC - bairro
# MAGIC - cidade
# MAGIC - estado
# MAGIC - cep
# MAGIC - logradouro
# MAGIC - latitude
# MAGIC - longitude
# MAGIC - pix_saque
# MAGIC - pix_troco

# COMMAND ----------

# Exibir todas as informações do primeiro ponto de atendimento
# de forma organizada para facilitar a leitura

from pprint import pprint

pprint(dados['registros'][0]['pontos_atendimento'][0])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação Inicial da Estrutura dos Dados
# MAGIC
# MAGIC A inspeção do primeiro ponto de atendimento permitiu identificar os principais campos disponíveis para análise.
# MAGIC
# MAGIC ### Campos observados
# MAGIC
# MAGIC - bairro
# MAGIC - cep
# MAGIC - cidade
# MAGIC - estado
# MAGIC - logradouro
# MAGIC - latitude
# MAGIC - longitude
# MAGIC - horarios_funcionamento
# MAGIC
# MAGIC ### Observações
# MAGIC
# MAGIC Foi identificado que a estrutura dos dados é parcialmente hierárquica, contendo listas e objetos aninhados.
# MAGIC
# MAGIC O campo `horarios_funcionamento` armazena os horários de atendimento para cada dia da semana.
# MAGIC
# MAGIC Além disso, foram identificadas coordenadas geográficas iguais a zero, o que poderá indicar problemas de qualidade dos dados que serão tratados futuramente.
# MAGIC
# MAGIC ### Próximos Passos
# MAGIC
# MAGIC Avaliar os campos restantes da estrutura para definir quais serão utilizados na construção da tabela analítica.

# COMMAND ----------

# Listar as chaves (colunas) disponíveis
# dentro do primeiro ponto de atendimento

dados['registros'][0]['pontos_atendimento'][0].keys()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Primeira Proposta de Modelagem
# MAGIC
# MAGIC Após a inspeção dos registros da API, foi realizada uma avaliação inicial da estrutura da futura tabela analítica.
# MAGIC
# MAGIC ### Campos Simples
# MAGIC
# MAGIC Os seguintes campos possuem estrutura simples e podem ser transformados diretamente em colunas:
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
# MAGIC
# MAGIC ### Campos Complexos
# MAGIC
# MAGIC Os seguintes campos possuem estrutura aninhada:
# MAGIC
# MAGIC - horarios_funcionamento
# MAGIC - produtos
# MAGIC
# MAGIC ### Estratégia Inicial
# MAGIC
# MAGIC Para a primeira versão da tabela analítica serão priorizadas as informações geográficas e de identificação dos agentes.
# MAGIC
# MAGIC Os campos complexos serão avaliados posteriormente para enriquecimento da análise.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Criar uma tabela consolidada que permita:
# MAGIC
# MAGIC - análise geográfica;
# MAGIC - distribuição por estado;
# MAGIC - distribuição por município;
# MAGIC - construção de dashboards;
# MAGIC - cálculo de indicadores de cobertura.

# COMMAND ----------

# Verificar o conteúdo do campo observacoes
# para o primeiro ponto de atendimento

dados['registros'][0]['pontos_atendimento'][0]['observacoes']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação Inicial do Campo Observações
# MAGIC
# MAGIC Foi realizada a inspeção do campo `observacoes` do primeiro registro.
# MAGIC
# MAGIC ### Resultado Observado
# MAGIC
# MAGIC O campo apresentou uma mensagem informativa relacionada às condições de atendimento do estabelecimento.
# MAGIC
# MAGIC ### Problemas Identificados
# MAGIC
# MAGIC Foi observada a presença de caracteres inválidos, indicando possível problema de codificação de texto (encoding).
# MAGIC
# MAGIC Exemplo:
# MAGIC
# MAGIC - Informa��es
# MAGIC - altera��o
# MAGIC - com�rcio
# MAGIC
# MAGIC ### Hipótese Inicial
# MAGIC
# MAGIC O campo pode conter mensagens padronizadas utilizadas pela Caixa para todos os pontos de atendimento.
# MAGIC
# MAGIC Essa hipótese deverá ser validada analisando outros registros da amostra.
# MAGIC
# MAGIC ### Possíveis Tratamentos Futuros
# MAGIC
# MAGIC - Correção de encoding;
# MAGIC - Remoção da coluna caso possua conteúdo padronizado;
# MAGIC - Utilização apenas se existirem observações relevantes por estabelecimento.

# COMMAND ----------

# Verificar a observação do segundo registro
# para identificar se o texto se repete

dados['registros'][1]['pontos_atendimento'][0]['observacoes']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação do Campo Observações
# MAGIC
# MAGIC Foi realizada uma comparação entre os dois primeiros registros da API.
# MAGIC
# MAGIC ### Resultados
# MAGIC
# MAGIC Registro 1:
# MAGIC "Informações sujeitas a alteração de acordo com as regras do comércio local."
# MAGIC
# MAGIC Registro 2:
# MAGIC "Informações sujeitas a alteração de acordo com as regras do comércio local."
# MAGIC
# MAGIC ### Conclusão Inicial
# MAGIC
# MAGIC O campo `observacoes` apresentou o mesmo conteúdo nos registros analisados.
# MAGIC
# MAGIC Isso sugere que a informação pode ser um aviso padrão fornecido pela Caixa e não uma característica específica do estabelecimento.
# MAGIC
# MAGIC ### Decisão Provisória
# MAGIC
# MAGIC O campo será mantido durante a etapa de coleta.
# MAGIC
# MAGIC Na fase de tratamento dos dados será avaliada a necessidade de remover a coluna caso o conteúdo permaneça padronizado em toda a base.

# COMMAND ----------

# Exibir a estrutura do campo produtos
# para entender como transformá-lo em colunas

dados['registros'][0]['pontos_atendimento'][0]['produtos']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação do Campo Produtos
# MAGIC
# MAGIC Foi realizada a inspeção do campo `produtos` do primeiro ponto de atendimento.
# MAGIC
# MAGIC ### Estrutura Identificada
# MAGIC
# MAGIC {
# MAGIC     'Pix-saque': True,
# MAGIC     'Pix-troco': True
# MAGIC }
# MAGIC
# MAGIC ### Interpretação
# MAGIC
# MAGIC O campo informa quais serviços estão disponíveis no estabelecimento.
# MAGIC
# MAGIC ### Estratégia de Modelagem
# MAGIC
# MAGIC Durante a transformação dos dados, o campo será desmembrado nas seguintes colunas:
# MAGIC
# MAGIC - pix_saque
# MAGIC - pix_troco
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC Essa estrutura facilitará:
# MAGIC
# MAGIC - contagens por serviço;
# MAGIC - análises por estado;
# MAGIC - análises por município;
# MAGIC - criação de indicadores;
# MAGIC - construção de dashboards.

# COMMAND ----------

# Verificar as coordenadas geográficas
# do segundo registro da API

dados['registros'][1]['pontos_atendimento'][0]['latitude'], dados['registros'][1]['pontos_atendimento'][0]['longitude']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação Inicial das Coordenadas Geográficas
# MAGIC
# MAGIC Foi realizada a inspeção das coordenadas geográficas dos dois primeiros registros.
# MAGIC
# MAGIC ### Resultados
# MAGIC
# MAGIC Registro 1
# MAGIC
# MAGIC - latitude: 0.00000
# MAGIC - longitude: 0.00000
# MAGIC
# MAGIC Registro 2
# MAGIC
# MAGIC - latitude: 0.00000
# MAGIC - longitude: 0.00000
# MAGIC
# MAGIC ### Problema Identificado
# MAGIC
# MAGIC Os valores encontrados não representam coordenadas geográficas válidas para os municípios analisados.
# MAGIC
# MAGIC ### Hipóteses
# MAGIC
# MAGIC 1. A API não disponibiliza coordenadas reais para os pontos de atendimento.
# MAGIC 2. Apenas parte dos registros possui coordenadas válidas.
# MAGIC
# MAGIC ### Impacto no Projeto
# MAGIC
# MAGIC Caso a maioria dos registros possua coordenadas zeradas, os mapas precisarão ser construídos utilizando município e estado em vez de latitude e longitude.

# COMMAND ----------

# Verificar as coordenadas do décimo registro
# para identificar se existem coordenadas válidas na base

dados['registros'][9]['pontos_atendimento'][0]['latitude'], dados['registros'][9]['pontos_atendimento'][0]['longitude']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Investigação das Coordenadas Geográficas
# MAGIC
# MAGIC Foi realizada uma análise preliminar das coordenadas geográficas disponibilizadas pela API.
# MAGIC
# MAGIC ### Registros Avaliados
# MAGIC
# MAGIC Registro 1
# MAGIC
# MAGIC - latitude: 0.00000
# MAGIC - longitude: 0.00000
# MAGIC
# MAGIC Registro 2
# MAGIC
# MAGIC - latitude: 0.00000
# MAGIC - longitude: 0.00000
# MAGIC
# MAGIC Registro 10
# MAGIC
# MAGIC - latitude: 0.00000
# MAGIC - longitude: 0.00000
# MAGIC
# MAGIC ### Conclusão Inicial
# MAGIC
# MAGIC Todos os registros analisados apresentaram coordenadas geográficas zeradas.
# MAGIC
# MAGIC ### Hipótese
# MAGIC
# MAGIC A API pode não disponibilizar coordenadas reais dos pontos de atendimento.
# MAGIC
# MAGIC ### Impacto para o Projeto
# MAGIC
# MAGIC Caso essa característica seja confirmada após a coleta completa, a construção dos mapas será baseada nos campos:
# MAGIC
# MAGIC - cidade
# MAGIC - estado
# MAGIC - CEP
# MAGIC
# MAGIC em vez de latitude e longitude.

# COMMAND ----------

# Verificar os produtos do décimo registro
# para identificar se existem combinações diferentes de serviços

dados['registros'][9]['pontos_atendimento'][0]['produtos']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Avaliação Inicial dos Serviços Disponíveis
# MAGIC
# MAGIC Foi realizada uma análise preliminar do campo `produtos` para entender quais serviços são disponibilizados nos pontos de atendimento.
# MAGIC
# MAGIC ### Registros Avaliados
# MAGIC
# MAGIC Registro 1
# MAGIC
# MAGIC - Pix-saque: True
# MAGIC - Pix-troco: True
# MAGIC
# MAGIC Registro 10
# MAGIC
# MAGIC - Pix-saque: True
# MAGIC - Pix-troco: True
# MAGIC
# MAGIC ### Conclusão Inicial
# MAGIC
# MAGIC Todos os registros avaliados até o momento oferecem simultaneamente os serviços:
# MAGIC
# MAGIC - Pix Saque
# MAGIC - Pix Troco
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC Será necessário validar esse comportamento após a coleta completa dos dados.
# MAGIC
# MAGIC Caso todos os registros possuam a mesma configuração, os campos poderão ter baixo valor analítico para segmentação.

# COMMAND ----------

# MAGIC %md
# MAGIC # Arquitetura do Projeto
# MAGIC
# MAGIC Este projeto seguirá uma arquitetura em camadas.
# MAGIC
# MAGIC ## Camada RAW
# MAGIC
# MAGIC Responsável por armazenar os dados exatamente como foram recebidos da API.
# MAGIC
# MAGIC Objetivos:
# MAGIC
# MAGIC - preservar os dados originais;
# MAGIC - permitir auditoria;
# MAGIC - evitar perda de informação;
# MAGIC - possibilitar o reprocessamento dos dados.
# MAGIC
# MAGIC ## Camada Tratada
# MAGIC
# MAGIC Responsável por:
# MAGIC
# MAGIC - limpeza;
# MAGIC - padronização;
# MAGIC - tratamento de valores inválidos;
# MAGIC - modelagem analítica.
# MAGIC
# MAGIC ## Camada Analítica
# MAGIC
# MAGIC Responsável por:
# MAGIC
# MAGIC - consultas SQL;
# MAGIC - indicadores;
# MAGIC - dashboards;
# MAGIC - visualizações.

# COMMAND ----------

# Consultar a quantidade total de páginas informada pela API

dados['meta']['total_paginas']

# COMMAND ----------

# MAGIC %md
# MAGIC ## Planejamento da Camada RAW
# MAGIC
# MAGIC Foi definida a arquitetura em camadas para o projeto.
# MAGIC
# MAGIC ### Estrutura
# MAGIC
# MAGIC API Caixa
# MAGIC ↓
# MAGIC RAW
# MAGIC ↓
# MAGIC Tratado
# MAGIC ↓
# MAGIC Análise
# MAGIC ↓
# MAGIC Dashboard
# MAGIC
# MAGIC ### Objetivo da Camada RAW
# MAGIC
# MAGIC Armazenar os dados exatamente como foram recebidos da API.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Preservação dos dados originais;
# MAGIC - Possibilidade de auditoria;
# MAGIC - Reprocessamento dos dados;
# MAGIC - Separação entre coleta e tratamento.
# MAGIC
# MAGIC ### Informações Confirmadas
# MAGIC
# MAGIC - Total de páginas: 260
# MAGIC - Total de registros: 25.942
# MAGIC - Registros por página: 100
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Implementar a coleta automática de todas as páginas da API para formar a base RAW.

# COMMAND ----------

# Armazenar a quantidade total de páginas da API
# Esta variável será utilizada posteriormente
# no processo de coleta automática

total_paginas = dados['meta']['total_paginas']

# Exibir o valor armazenado

print(f"Total de páginas: {total_paginas}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparação da Extração Completa
# MAGIC
# MAGIC Até este momento foram realizadas as seguintes atividades:
# MAGIC
# MAGIC ### Entendimento da Fonte
# MAGIC
# MAGIC - Conexão com a API oficial da Caixa.
# MAGIC - Validação do acesso.
# MAGIC - Análise da estrutura JSON.
# MAGIC - Entendimento da paginação.
# MAGIC
# MAGIC ### Descobertas
# MAGIC
# MAGIC - Total de registros: 25.942
# MAGIC - Total de páginas: 260
# MAGIC - Registros por página: 100
# MAGIC
# MAGIC ### Avaliação da Estrutura
# MAGIC
# MAGIC Campos principais identificados:
# MAGIC
# MAGIC - cnpj_agente_saque
# MAGIC - nome_agente_saque
# MAGIC - bairro
# MAGIC - cidade
# MAGIC - estado
# MAGIC - cep
# MAGIC - logradouro
# MAGIC - latitude
# MAGIC - longitude
# MAGIC - produtos
# MAGIC - observacoes
# MAGIC
# MAGIC ### Problemas de Qualidade Identificados
# MAGIC
# MAGIC - Coordenadas geográficas aparentemente zeradas.
# MAGIC - Possíveis problemas de codificação de caracteres.
# MAGIC - Campo observacoes com conteúdo aparentemente padronizado.
# MAGIC
# MAGIC ### Próxima Etapa
# MAGIC
# MAGIC Realizar um teste controlado de coleta automática antes de extrair todas as 260 páginas da API.

# COMMAND ----------

# Lista que armazenará os registros coletados
registros_teste = []

# Percorrer apenas as três primeiras páginas da API
for pagina in range(1, 4):

    # Montar a URL da página atual
    url = (
        f"https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1"
        f"?page={pagina}&page-size=100"
    )

    # Realizar a requisição
    response = requests.get(url)

    # Converter a resposta para JSON
    dados_pagina = response.json()

    # Adicionar os registros da página à lista de teste
    registros_teste.extend(dados_pagina['registros'])

# Exibir a quantidade total coletada
print(f"Total de registros coletados: {len(registros_teste)}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Teste da Coleta Automatizada
# MAGIC
# MAGIC Antes da extração completa da base, foi realizado um teste controlado utilizando as três primeiras páginas da API.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Validar a estratégia de coleta automática antes de processar todas as 260 páginas disponíveis.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC Páginas coletadas:
# MAGIC
# MAGIC - Página 1
# MAGIC - Página 2
# MAGIC - Página 3
# MAGIC
# MAGIC Total de registros coletados:
# MAGIC
# MAGIC 300
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A estratégia de paginação funcionou corretamente.
# MAGIC
# MAGIC Os registros foram consolidados em uma única estrutura de dados, demonstrando que o processo pode ser escalado para a coleta completa da base.
# MAGIC
# MAGIC ### Próximos Passos
# MAGIC
# MAGIC - Coletar as 260 páginas da API.
# MAGIC - Armazenar os dados na camada RAW.
# MAGIC - Analisar o volume real de registros.
# MAGIC - Iniciar a etapa de transformação dos dados.

# COMMAND ----------

# Verificar o tipo da estrutura criada
# para confirmar que os registros foram consolidados corretamente

type(registros_teste)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validação da Estrutura de Armazenamento
# MAGIC
# MAGIC Após o teste de coleta das três primeiras páginas, foi realizada uma validação da estrutura utilizada para armazenar os dados.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC Tipo da estrutura:
# MAGIC
# MAGIC list
# MAGIC
# MAGIC ### Interpretação
# MAGIC
# MAGIC Os registros das diferentes páginas foram consolidados corretamente em uma única lista.
# MAGIC
# MAGIC ### Benefício
# MAGIC
# MAGIC Essa abordagem permite:
# MAGIC
# MAGIC - percorrer todas as páginas da API;
# MAGIC - armazenar os registros em uma única estrutura;
# MAGIC - transformar os dados posteriormente em DataFrame;
# MAGIC - carregar os dados na camada RAW.
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A arquitetura de coleta foi validada com sucesso e está pronta para escalar para o volume total de dados da API.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Extração Completa da Camada RAW
# MAGIC
# MAGIC Após validar a conexão com a API, a paginação e a estratégia de coleta, será realizada a extração completa dos dados.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Coletar todos os registros disponíveis na API da Caixa.
# MAGIC
# MAGIC ### Volume Esperado
# MAGIC
# MAGIC - 260 páginas
# MAGIC - Aproximadamente 25.942 registros
# MAGIC
# MAGIC ### Estratégia
# MAGIC
# MAGIC 1. Percorrer todas as páginas da API.
# MAGIC 2. Coletar os registros de cada página.
# MAGIC 3. Consolidar todos os registros em uma única estrutura.
# MAGIC 4. Validar a quantidade final de registros coletados.
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC Os dados serão mantidos em seu formato original nesta fase, sem qualquer tratamento ou limpeza.
# MAGIC
# MAGIC Essa abordagem garante a preservação integral da camada RAW.%md
# MAGIC

# COMMAND ----------

# Lista que armazenará todos os registros da camada RAW
registros_raw = []

# Percorrer todas as páginas da API
for pagina in range(1, total_paginas + 1):

    # Montar a URL da página atual
    url = (
        f"https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1"
        f"?page={pagina}&page-size=100"
    )

    # Realizar a requisição para a API
    response = requests.get(url)

    # Converter a resposta para JSON
    dados_pagina = response.json()

    # Adicionar os registros da página à estrutura RAW
    registros_raw.extend(dados_pagina["registros"])

# Exibir a quantidade total coletada
print(f"Total de registros coletados: {len(registros_raw)}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultado da Extração Completa
# MAGIC
# MAGIC A extração completa dos dados foi realizada com sucesso.
# MAGIC
# MAGIC ### Volume Coletado
# MAGIC
# MAGIC - Total de páginas processadas: 260
# MAGIC - Total de registros coletados: 25.942
# MAGIC
# MAGIC ### Validação
# MAGIC
# MAGIC A quantidade coletada corresponde exatamente ao valor informado nos metadados da API.
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A camada RAW foi criada com sucesso.
# MAGIC
# MAGIC Todos os registros foram mantidos em sua estrutura original, sem qualquer transformação ou tratamento.
# MAGIC
# MAGIC ### Próximos Passos
# MAGIC
# MAGIC - Inspecionar a estrutura da camada RAW.
# MAGIC - Transformar os registros em DataFrame.
# MAGIC - Persistir os dados no Databricks.
# MAGIC - Iniciar a criação da camada tratada.

# COMMAND ----------

# Verificar o tipo da estrutura RAW
# que acabou de ser criada

type(registros_raw)

# COMMAND ----------

# MAGIC %md
# MAGIC # Marco do Projeto: Camada RAW Criada
# MAGIC
# MAGIC A extração completa da API foi concluída com sucesso.
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC - Estrutura criada: registros_raw
# MAGIC - Tipo: list
# MAGIC - Quantidade de registros: 25.942
# MAGIC
# MAGIC ## Objetivo Alcançado
# MAGIC
# MAGIC Os dados foram coletados e armazenados em memória sem qualquer transformação.
# MAGIC
# MAGIC A integridade dos dados originais foi preservada.
# MAGIC
# MAGIC ## Próxima Etapa
# MAGIC
# MAGIC Transformar a estrutura RAW em um DataFrame para facilitar:
# MAGIC
# MAGIC - exploração dos dados;
# MAGIC - tratamento;
# MAGIC - modelagem;
# MAGIC - persistência no Databricks;
# MAGIC - análises futuras.

# COMMAND ----------

# Validar a quantidade de registros presentes
# na estrutura RAW

len(registros_raw)

# COMMAND ----------

# MAGIC %md
# MAGIC # Conclusão da Camada RAW
# MAGIC
# MAGIC A extração completa dos dados foi finalizada com sucesso.
# MAGIC
# MAGIC ## Resultados
# MAGIC
# MAGIC - Fonte: API Caixa Econômica Federal
# MAGIC - Páginas processadas: 260
# MAGIC - Registros coletados: 25.942
# MAGIC
# MAGIC ## Validações realizadas
# MAGIC
# MAGIC - Estrutura de dados validada.
# MAGIC - Paginação validada.
# MAGIC - Total de registros conferido.
# MAGIC - Dados armazenados na variável registros_raw.
# MAGIC
# MAGIC ## Status
# MAGIC
# MAGIC CAMADA RAW CONCLUÍDA ✅
# MAGIC
# MAGIC ## Próxima Etapa
# MAGIC
# MAGIC Transformação dos dados em DataFrame para persistência e tratamento.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conversão da Camada RAW para DataFrame
# MAGIC
# MAGIC Para facilitar a exploração e o tratamento dos dados, os registros coletados serão convertidos para um DataFrame.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Visualização tabular;
# MAGIC - Integração com Spark;
# MAGIC - Persistência em tabelas;
# MAGIC - Consultas SQL;
# MAGIC - Transformações estruturadas.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Criar a primeira representação tabular da camada RAW.

# COMMAND ----------

# Importar a biblioteca pandas
import pandas as pd

# Converter os registros RAW em um DataFrame
df_raw = pd.DataFrame(registros_raw)

# Exibir as dimensões do DataFrame
df_raw.shape

# COMMAND ----------

# MAGIC %md
# MAGIC ## Estrutura Inicial do DataFrame RAW
# MAGIC
# MAGIC Após a conversão dos dados para DataFrame, foi identificada a seguinte estrutura:
# MAGIC
# MAGIC ### Dimensões
# MAGIC
# MAGIC - Linhas: 25.942
# MAGIC - Colunas: 3
# MAGIC
# MAGIC ### Colunas
# MAGIC
# MAGIC - cnpj_agente_saque
# MAGIC - nome_agente_saque
# MAGIC - pontos_atendimento
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC A coluna `pontos_atendimento` contém uma estrutura aninhada e não pode ser utilizada diretamente em análises.
# MAGIC
# MAGIC Será necessário realizar uma transformação para expandir os atributos dos pontos de atendimento em colunas individuais.
# MAGIC
# MAGIC ### Próxima Etapa
# MAGIC
# MAGIC Inspecionar a estrutura do DataFrame e preparar a sua normalização.

# COMMAND ----------

# Exibir os nomes das colunas do DataFrame RAW

df_raw.columns

# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência da Camada RAW
# MAGIC
# MAGIC Até o momento os dados encontram-se apenas na memória da sessão do notebook.
# MAGIC
# MAGIC ### Risco
# MAGIC
# MAGIC Em caso de reinicialização da sessão, os dados precisarão ser coletados novamente da API.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Persistir a camada RAW em uma tabela do Databricks para garantir:
# MAGIC
# MAGIC - reprodutibilidade;
# MAGIC - segurança dos dados;
# MAGIC - reutilização em futuras etapas;
# MAGIC - separação entre coleta e tratamento.
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Salvar o DataFrame RAW em uma tabela permanente.

# COMMAND ----------

# Exibir as primeiras linhas do DataFrame RAW
# para validar a estrutura tabular antes da persistência

df_raw.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validação do DataFrame RAW
# MAGIC
# MAGIC Foi realizada a inspeção das primeiras linhas do DataFrame criado a partir da camada RAW.
# MAGIC
# MAGIC ### Estrutura Observada
# MAGIC
# MAGIC Colunas disponíveis:
# MAGIC
# MAGIC - cnpj_agente_saque
# MAGIC - nome_agente_saque
# MAGIC - pontos_atendimento
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC A coluna `pontos_atendimento` permanece armazenada em formato estruturado (lista de dicionários).
# MAGIC
# MAGIC Essa estrutura ainda não é adequada para análises, filtros ou consultas SQL.
# MAGIC
# MAGIC ### Próxima Etapa
# MAGIC
# MAGIC Expandir o conteúdo da coluna `pontos_atendimento` para criar uma tabela analítica com colunas individuais.

# COMMAND ----------

# Verificar o tipo armazenado na coluna
# pontos_atendimento da primeira linha

type(df_raw.loc[0, 'pontos_atendimento'])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparação para Normalização dos Dados
# MAGIC
# MAGIC Foi confirmado que a coluna `pontos_atendimento` possui estrutura do tipo lista.
# MAGIC
# MAGIC ### Situação Atual
# MAGIC
# MAGIC Cada linha do DataFrame representa um agente de saque.
# MAGIC
# MAGIC As informações geográficas estão armazenadas dentro da coluna:
# MAGIC
# MAGIC - pontos_atendimento
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Expandir a estrutura aninhada para criar colunas analíticas.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC Após a expansão será possível:
# MAGIC
# MAGIC - filtrar por estado;
# MAGIC - agrupar por município;
# MAGIC - construir dashboards;
# MAGIC - realizar consultas SQL;
# MAGIC - criar indicadores de cobertura.

# COMMAND ----------

# Expandir a coluna pontos_atendimento
# Transformando cada item da lista em uma linha

df_expandido = df_raw.explode('pontos_atendimento')

# Exibir as dimensões da nova estrutura

df_expandido.shape

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultado da Expansão de Pontos de Atendimento
# MAGIC
# MAGIC Foi realizada a expansão da coluna `pontos_atendimento` utilizando o método `explode()`.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC Dimensões antes da expansão:
# MAGIC
# MAGIC - 25.942 linhas
# MAGIC - 3 colunas
# MAGIC
# MAGIC Dimensões após a expansão:
# MAGIC
# MAGIC - 25.942 linhas
# MAGIC - 3 colunas
# MAGIC
# MAGIC ### Interpretação
# MAGIC
# MAGIC A expansão não alterou a quantidade de linhas.
# MAGIC
# MAGIC Isso indica que, para os registros analisados, cada agente possui apenas um ponto de atendimento associado.
# MAGIC
# MAGIC ### Impacto
# MAGIC
# MAGIC A modelagem dos dados será simplificada, pois não será necessário tratar múltiplos pontos por agente.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência da Camada RAW
# MAGIC
# MAGIC Após a conclusão da coleta completa da API, os dados serão persistidos para evitar nova extração.
# MAGIC
# MAGIC ### Objetivos
# MAGIC
# MAGIC - Preservar os dados coletados.
# MAGIC - Evitar novas chamadas à API.
# MAGIC - Permitir reutilização da base nas próximas etapas.
# MAGIC - Garantir reprodutibilidade do projeto.
# MAGIC
# MAGIC ### Estratégia
# MAGIC
# MAGIC Salvar o DataFrame RAW em formato CSV.
# MAGIC
# MAGIC Posteriormente o arquivo será utilizado para criação da camada tratada e das tabelas analíticas.

# COMMAND ----------

# Salvar a camada RAW em arquivo CSV
# index=False evita criar uma coluna extra de índice

df_raw.to_csv(
    "/Workspace/Projeto_Caixa_Pix/pix_caixa_raw.csv",
    index=False
)

print("Arquivo RAW salvo com sucesso!")

# COMMAND ----------

# Verificar o diretório atual de trabalho

import os

os.getcwd()
``

# COMMAND ----------

import os

print(os.getcwd())

# COMMAND ----------

# Verificar se o DataFrame ainda está na memória

df_raw.shape

# COMMAND ----------

# MAGIC %md
# MAGIC ## Recuperação da Sessão
# MAGIC
# MAGIC A sessão do Databricks foi reiniciada após o encerramento do ambiente.
# MAGIC
# MAGIC Como os dados ainda não haviam sido persistidos em armazenamento permanente, as variáveis em memória foram perdidas.
# MAGIC
# MAGIC ### Impacto
# MAGIC
# MAGIC Será necessário reconstruir:
# MAGIC
# MAGIC - registros_raw
# MAGIC - df_raw
# MAGIC - df_expandido
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC O notebook e toda a documentação permaneceram preservados.

# COMMAND ----------

# Verificar se a variável total_paginas ainda existe

total_paginas

# COMMAND ----------

# MAGIC %md
# MAGIC ## Recuperação da Camada RAW
# MAGIC
# MAGIC A sessão do Databricks foi reiniciada antes que os dados fossem persistidos.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Reconstruir a camada RAW e persisti-la em armazenamento permanente.
# MAGIC
# MAGIC ### Estratégia
# MAGIC
# MAGIC - Reexecutar a coleta completa da API.
# MAGIC - Criar novamente o DataFrame RAW.
# MAGIC - Persistir os dados imediatamente após a coleta.
# MAGIC
# MAGIC ### Observação
# MAGIC
# MAGIC As etapas exploratórias não serão repetidas, pois já foram documentadas e validadas anteriormente.

# COMMAND ----------

# Importar bibliotecas necessárias

import requests
import pandas as pd

# URL base da API

url = "https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1/"

# Obter metadados da API

dados = requests.get(url).json()

# Recuperar quantidade total de páginas

total_paginas = dados["meta"]["total_paginas"]

# Exibir resultado

print(f"Total de páginas encontradas: {total_paginas}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Estratégia de Persistência da Camada RAW
# MAGIC
# MAGIC Após a perda da sessão anterior, foi definida uma nova estratégia.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Persistir os dados imediatamente após a coleta.
# MAGIC
# MAGIC ### Motivação
# MAGIC
# MAGIC Os dados armazenados apenas em memória são perdidos quando a sessão do Databricks é encerrada.
# MAGIC
# MAGIC ### Nova Abordagem
# MAGIC
# MAGIC 1. Coletar a camada RAW.
# MAGIC 2. Salvar a camada RAW em armazenamento permanente.
# MAGIC 3. Continuar o tratamento a partir da versão persistida.
# MAGIC
# MAGIC ### Benefício
# MAGIC
# MAGIC Evita novas chamadas à API em futuros acessos ao projeto.

# COMMAND ----------

# Lista que armazenará todos os registros coletados

registros_raw = []

# Percorrer todas as páginas da API

for pagina in range(1, total_paginas + 1):

    # Montar URL da página atual
    url = (
        f"https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1"
        f"?page={pagina}&page-size=100"
    )

    # Buscar os dados da página
    response = requests.get(url)

    # Converter para JSON
    dados_pagina = response.json()

    # Adicionar os registros à estrutura RAW
    registros_raw.extend(dados_pagina["registros"])

# Validar a quantidade coletada

print(f"Registros coletados: {len(registros_raw)}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tratamento de Erros na Coleta
# MAGIC
# MAGIC Durante a reconstrução da camada RAW foi identificado um erro de conversão JSON.
# MAGIC
# MAGIC ### Erro Encontrado
# MAGIC
# MAGIC JSONDecodeError
# MAGIC
# MAGIC ### Possível Causa
# MAGIC
# MAGIC Em alguma das páginas a API retornou uma resposta inválida ou vazia.
# MAGIC
# MAGIC ### Ação
# MAGIC
# MAGIC Implementar validação da resposta antes de converter para JSON.
# MAGIC
# MAGIC ### Benefício
# MAGIC
# MAGIC Maior robustez na ingestão dos dados.

# COMMAND ----------

# Testar a primeira página da API
# antes de iniciar uma nova carga completa

url_teste = (
    "https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1"
    "?page=1&page-size=100"
)

response = requests.get(url_teste)

print("Status:", response.status_code)
print("Tamanho da resposta:", len(response.text))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Coletor Robusto da Camada RAW
# MAGIC
# MAGIC A primeira implementação de coleta apresentou falha durante a conversão de uma das páginas para JSON.
# MAGIC
# MAGIC ### Melhorias Implementadas
# MAGIC
# MAGIC - Exibição de progresso durante a execução;
# MAGIC - Tratamento de erros;
# MAGIC - Registro de páginas com falha;
# MAGIC - Validação da resposta da API;
# MAGIC - Relatório final da coleta.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Garantir uma extração mais confiável dos 25.942 registros disponibilizados pela API da Caixa.

# COMMAND ----------

# Lista que armazenará todos os registros coletados
registros_raw = []

# Lista para registrar páginas que apresentarem erro
paginas_com_erro = []

# Percorrer todas as páginas da API
for pagina in range(1, total_paginas + 1):

    try:

        # Montar URL da página atual
        url = (
            f"https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1"
            f"?page={pagina}&page-size=100"
        )

        # Realizar a requisição
        response = requests.get(url, timeout=30)

        # Validar o retorno HTTP
        if response.status_code != 200:
            paginas_com_erro.append(pagina)
            continue

        # Converter para JSON
        dados_pagina = response.json()

        # Adicionar registros à coleção RAW
        registros_raw.extend(dados_pagina["registros"])

        # Mostrar progresso a cada 10 páginas
        if pagina % 10 == 0 or pagina == total_paginas:

            percentual = round((pagina / total_paginas) * 100, 1)

            print(
                f"Página {pagina}/{total_paginas} "
                f"({percentual}%) "
                f"- Registros coletados: {len(registros_raw)}"
            )

    except Exception as erro:

        paginas_com_erro.append(pagina)

        print(
            f"Erro na página {pagina}: {erro}"
        )

# Resumo final

print("\nColeta concluída!")
print(f"Total de registros: {len(registros_raw)}")
print(f"Páginas com erro: {paginas_com_erro}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultado da Coleta Robusta
# MAGIC
# MAGIC A coleta foi concluída com sucesso, porém uma página apresentou falha de comunicação.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC - Registros esperados: 25.942
# MAGIC - Registros coletados: 25.842
# MAGIC - Diferença: 100 registros
# MAGIC
# MAGIC ### Página com Falha
# MAGIC
# MAGIC - Página 91
# MAGIC
# MAGIC ### Causa
# MAGIC
# MAGIC Timeout de leitura da API.
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Reprocessar apenas a página 91 para completar a camada RAW.

# COMMAND ----------

# Reprocessar apenas a página que apresentou erro

pagina_erro = 91

url = (
    f"https://api.caixa.gov.br:8443/dadosabertos/pontosPix/v1"
    f"?page={pagina_erro}&page-size=100"
)

response = requests.get(url, timeout=60)

dados_pagina_91 = response.json()

# Quantidade de registros recuperados

print(
    f"Registros recuperados: "
    f"{len(dados_pagina_91['registros'])}"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Recuperação da Página com Falha
# MAGIC
# MAGIC Durante a coleta foi identificado timeout na página 91.
# MAGIC
# MAGIC ### Tratamento Aplicado
# MAGIC
# MAGIC A página foi reprocessada individualmente.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC - Registros recuperados: 100
# MAGIC
# MAGIC ### Resultado Final
# MAGIC
# MAGIC - Registros esperados: 25.942
# MAGIC - Registros coletados: 25.942
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A camada RAW encontra-se completa e consistente.
# MAGIC
# MAGIC Nenhum registro foi perdido durante o processo de ingestão.

# COMMAND ----------

# Verificar se o DBFS está disponível

dbutils.fs.ls("/")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Recuperação Bem-Sucedida da Carga
# MAGIC
# MAGIC Durante a ingestão foi identificado timeout na página 91.
# MAGIC
# MAGIC ### Situação Inicial
# MAGIC
# MAGIC - Registros esperados: 25.942
# MAGIC - Registros carregados: 25.842
# MAGIC - Diferença: 100 registros
# MAGIC
# MAGIC ### Tratamento Aplicado
# MAGIC
# MAGIC A página 91 foi reprocessada individualmente.
# MAGIC
# MAGIC ### Resultado
# MAGIC
# MAGIC - Registros recuperados: 100
# MAGIC
# MAGIC ### Conclusão
# MAGIC
# MAGIC A estratégia de monitoramento e recuperação permitiu recuperar os registros faltantes sem necessidade de reexecutar toda a carga.
# MAGIC
# MAGIC Essa abordagem reduz tempo de processamento e aumenta a confiabilidade do pipeline.

# COMMAND ----------

# Adicionar os registros recuperados da página 91
# à coleção principal da camada RAW

registros_raw.extend(
    dados_pagina_91["registros"]
)

# Validar a quantidade final de registros

print(
    f"Total final de registros: {len(registros_raw)}"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparação para Persistência da Camada RAW
# MAGIC
# MAGIC Após a conclusão da coleta e recuperação da página com falha, a camada RAW será preparada para armazenamento permanente.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Evitar novas chamadas à API em futuras sessões.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Reutilização dos dados.
# MAGIC - Redução do tempo de processamento.
# MAGIC - Continuidade do projeto.
# MAGIC - Reprodutibilidade das análises.
# MAGIC
# MAGIC ### Resultado Esperado
# MAGIC
# MAGIC Criação de um arquivo contendo os 25.942 registros coletados.

# COMMAND ----------

# Converter a coleção RAW em DataFrame
# para permitir exportação

import pandas as pd

df_raw = pd.DataFrame(registros_raw)

# Validar as dimensões

print(df_raw.shape)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência da Camada RAW
# MAGIC
# MAGIC A camada RAW foi concluída com sucesso.
# MAGIC
# MAGIC ### Informações da Camada
# MAGIC
# MAGIC - Total de registros: 25.942
# MAGIC - Fonte: API oficial da Caixa
# MAGIC - Status: Completa
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Persistir os dados em armazenamento permanente do Databricks para evitar novas chamadas à API em futuras sessões.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Redução do tempo de processamento;
# MAGIC - Reprodutibilidade;
# MAGIC - Segurança;
# MAGIC - Versionamento da base.

# COMMAND ----------

# Verificar conteúdo da área Workspace do DBFS

dbutils.fs.ls("dbfs:/Workspace/")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Salvamento da Camada RAW
# MAGIC
# MAGIC Após a conclusão da coleta e da recuperação da página com falha, a camada RAW será armazenada permanentemente.
# MAGIC
# MAGIC ### Informações da Camada
# MAGIC
# MAGIC - Fonte: API da Caixa
# MAGIC - Total de registros: 25.942
# MAGIC - Tipo: RAW
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Persistir os dados para evitar novas chamadas à API em futuras sessões.
# MAGIC
# MAGIC ### Resultado Esperado
# MAGIC
# MAGIC Arquivo persistido no DBFS para reutilização nas etapas de tratamento e análise.

# COMMAND ----------

# Salvar a camada RAW em formato Parquet

df_raw.to_parquet(
    "/dbfs/Workspace/01_Coleta_RAW/pix_caixa_raw.parquet",
    index=False
)

print("Camada RAW salva com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Descoberta do Caminho de Persistência
# MAGIC
# MAGIC Foi identificado que o caminho do Workspace não pode ser utilizado diretamente pelo método `to_parquet()` do Pandas.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Identificar um local válido para armazenamento dos arquivos do projeto.
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Verificar os diretórios físicos disponíveis na sessão do Databricks.

# COMMAND ----------

# Verificar os diretórios físicos disponíveis
# na máquina do Databricks

import os

print(os.listdir("/"))


# COMMAND ----------

# MAGIC %md
# MAGIC ## Validação do Destino de Persistência
# MAGIC
# MAGIC Foi identificado que o ambiente possui DBFS disponível.
# MAGIC
# MAGIC O próximo passo consiste em localizar um diretório gravável para armazenar permanentemente a camada RAW.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Garantir o armazenamento seguro dos dados coletados antes de iniciar a fase de transformação.
# MAGIC
# MAGIC ### Critérios
# MAGIC
# MAGIC - Diretório persistente
# MAGIC - Compatível com Pandas
# MAGIC - Compatível com futuras leituras
# MAGIC ``

# COMMAND ----------

# Verificar se o diretório DBFS físico está acessível

import os

print(os.path.exists("/dbfs"))
print(os.listdir("/dbfs"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Criação da Área de Persistência
# MAGIC
# MAGIC Foi validado que o DBFS está acessível a partir da sessão do Databricks.
# MAGIC
# MAGIC ### Estratégia
# MAGIC
# MAGIC Criar um diretório dedicado ao projeto dentro do DBFS para armazenamento da camada RAW.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Persistência entre sessões;
# MAGIC - Reutilização dos dados;
# MAGIC - Organização do projeto;
# MAGIC - Eliminação da necessidade de novas chamadas à API.

# COMMAND ----------

# Criar diretório do projeto dentro do DBFS

import os

os.makedirs(
    "/dbfs/projeto_caixa_pix",
    exist_ok=True
)

print("Diretório criado com sucesso!")

# COMMAND ----------

# Verificar o diretório temporário local do Databricks

import os

print(os.path.exists("/tmp"))
print(os.access("/tmp", os.W_OK))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Descoberta de Área Gravável
# MAGIC
# MAGIC Antes da persistência definitiva da camada RAW será validado um local de gravação compatível com o ambiente Databricks.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Identificar um caminho onde seja possível:
# MAGIC
# MAGIC - criar arquivos;
# MAGIC - ler arquivos;
# MAGIC - persistir a camada RAW.
# MAGIC
# MAGIC ### Próximo Passo
# MAGIC
# MAGIC Executar um teste simples de escrita.

# COMMAND ----------

# Testar criação de um arquivo simples no diretório temporário

with open("/tmp/teste.txt", "w") as arquivo:
    arquivo.write("Projeto Caixa Pix")

print("Arquivo criado com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Teste de Escrita no DBFS
# MAGIC
# MAGIC Antes de persistir a camada RAW, será validada a capacidade de escrita utilizando os recursos nativos do Databricks.
# MAGIC
# MAGIC ### Objetivo
# MAGIC
# MAGIC Confirmar um local persistente para armazenamento dos dados do projeto.
# MAGIC
# MAGIC ### Benefício
# MAGIC
# MAGIC Após a validação, a camada RAW poderá ser armazenada permanentemente e reutilizada em futuras sessões.

# COMMAND ----------

# Criar um diretório de teste usando o mecanismo nativo do Databricks

dbutils.fs.mkdirs("dbfs:/tmp/projeto_caixa_pix")

print("Diretório criado com sucesso!")

# COMMAND ----------

spark.range(1).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência da Camada RAW em Tabela Delta
# MAGIC
# MAGIC Após identificar restrições de escrita no DBFS público, será utilizada a estratégia recomendada pelo Databricks.
# MAGIC
# MAGIC ### Estratégia
# MAGIC
# MAGIC Persistir a camada RAW como uma tabela Delta.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Persistência entre sessões;
# MAGIC - Integração com SQL;
# MAGIC - Melhor desempenho;
# MAGIC - Compatibilidade com futuras transformações.
# MAGIC
# MAGIC ### Resultado Esperado
# MAGIC
# MAGIC Criação da tabela:
# MAGIC
# MAGIC pix_caixa_raw

# COMMAND ----------

# Converter o DataFrame Pandas para Spark DataFrame

spark_df_raw = spark.createDataFrame(df_raw)

# Verificar quantidade de registros

print(
    f"Registros no Spark DataFrame: "
    f"{spark_df_raw.count()}"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparação para Persistência em Delta
# MAGIC
# MAGIC A gravação em DBFS público não está disponível neste ambiente.
# MAGIC
# MAGIC ### Decisão Arquitetural
# MAGIC
# MAGIC Persistir a camada RAW utilizando Delta Tables.
# MAGIC
# MAGIC ### Vantagens
# MAGIC
# MAGIC - Persistência entre sessões;
# MAGIC - Integração nativa com Spark;
# MAGIC - Consultas SQL;
# MAGIC - Versionamento;
# MAGIC - Melhor desempenho.
# MAGIC
# MAGIC ### Tabela Planejada
# MAGIC
# MAGIC pix_caixa_raw

# COMMAND ----------

# Listar os bancos de dados disponíveis
# no ambiente Databricks

spark.sql("SHOW SCHEMAS").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Persistência Utilizando Delta Table
# MAGIC
# MAGIC Foi identificado o schema padrão disponível no ambiente:
# MAGIC
# MAGIC - default
# MAGIC
# MAGIC ### Estratégia
# MAGIC
# MAGIC Persistir a camada RAW como uma tabela Delta gerenciada pelo Databricks.
# MAGIC
# MAGIC ### Benefícios
# MAGIC
# MAGIC - Persistência entre sessões;
# MAGIC - Integração nativa com Spark SQL;
# MAGIC - Eliminação da dependência de arquivos locais;
# MAGIC - Melhor aderência às práticas de Engenharia de Dados.
# MAGIC
# MAGIC ### Nome da Tabela
# MAGIC
# MAGIC default.pix_caixa_raw

# COMMAND ----------

# Salvar a camada RAW como tabela Delta gerenciada

spark_df_raw.write \
    .mode("overwrite") \
    .saveAsTable("default.pix_caixa_raw")

print("Tabela RAW criada com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC # Marco do Projeto: Camada RAW Persistida
# MAGIC
# MAGIC A camada RAW foi persistida com sucesso em uma tabela Delta gerenciada pelo Databricks.
# MAGIC
# MAGIC ## Informações da Tabela
# MAGIC
# MAGIC Nome:
# MAGIC
# MAGIC default.pix_caixa_raw
# MAGIC
# MAGIC Volume:
# MAGIC
# MAGIC 25.942 registros
# MAGIC
# MAGIC ## Benefícios
# MAGIC
# MAGIC - Persistência entre sessões;
# MAGIC - Integração com Spark SQL;
# MAGIC - Reprocessamento facilitado;
# MAGIC - Independência da API de origem.
# MAGIC
# MAGIC ## Status do Projeto
# MAGIC
# MAGIC ✅ Coleta concluída
# MAGIC ✅ Recuperação de falhas concluída
# MAGIC ✅ Camada RAW persistida
# MAGIC
# MAGIC ## Próxima Fase
# MAGIC
# MAGIC Criação da camada tratada.
# MAGIC ``

# COMMAND ----------

# Consultar as tabelas disponíveis
# no schema default

spark.sql(
    "SHOW TABLES IN default"
).show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC # Fase 1 Encerrada
# MAGIC
# MAGIC Status: CONCLUÍDA
# MAGIC
# MAGIC ## Entregáveis
# MAGIC
# MAGIC - Conexão com API da Caixa.
# MAGIC - Análise da estrutura JSON.
# MAGIC - Descoberta da paginação.
# MAGIC - Coleta completa dos 25.942 registros.
# MAGIC - Implementação de monitoramento da carga.
# MAGIC - Recuperação de falha na página 91.
# MAGIC - Persistência da camada RAW.
# MAGIC
# MAGIC ## Tabela Criada
# MAGIC
# MAGIC default.pix_caixa_raw
# MAGIC
# MAGIC ## Quantidade de Registros
# MAGIC
# MAGIC 25.942
# MAGIC
# MAGIC ## Resultado
# MAGIC
# MAGIC A camada RAW encontra-se persistida e disponível para futuras transformações.
# MAGIC
# MAGIC Não será mais necessário realizar nova ingestão da API para continuar o projeto.