



# Aplicação do Spark com Kafka


from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from happybase import Connection


def insert_to_hbase(row):
    conn = Connection('localhost', port=2181)
    table = conn.table('nasa')
    table.put(row[0], {'dados_nasa': str(row[1])})


# O código começa importando a classe Connection do pacote happybase, que é usado para se conectar ao HBase. 
# A função insert_to_hbase recebe um parâmetro row, que é uma lista ou tupla contendo os valores da linha que se deseja inserir.

# Dentro da função, é criada uma conexão com o HBase especificando o endereço e a porta do servidor HBase 
# através da chamada à função Connection. 

# Em seguida, é obtida uma referência à tabela no HBase em que a linha será inserida usando o método table. 
# O nome da tabela é especificado como um argumento da função table.

# Finalmente, a função put é usada para inserir a linha na tabela. O primeiro argumento para a função put é a 
# chave da linha, que é o primeiro elemento da lista row. 
# O segundo argumento é um dicionário que mapeia as famílias de colunas em suas respectivas células de valor, onde a 
# família de colunas é especificada como uma string e o valor da célula é o segundo elemento da lista row.

# Em resumo, essa função se conecta ao HBase, insere uma linha em uma tabela específica e fecha a conexão com o banco de dados.

def process_logs(rdd):
    # Separa cada linha do log em campos separados por vírgula
    fields = rdd.map(lambda x: x.split(" "))

    # Remove as linhas que não possuem todos os campos esperados
    filtered_fields = fields.filter(lambda x: len(x) == 9)

    # Converte os campos para um formato apropriado para inserção no HBase
    formatted_fields = filtered_fields.map(lambda x: (x[0], {'dados_nasa': x[1]}))

    # Insere os dados no HBase
    formatted_fields.foreach(insert_to_hbase)

# Neste exemplo, a função process_logs recebe um RDD (Resilient Distributed Dataset) do Spark Streaming contendo as linhas 
# de log coletadas pelo Flume. 

# A função então processa os dados, filtrando as linhas que não possuem todos os campos esperados, formatando os campos para 
# um formato apropriado para inserção no HBase e, em seguida, inserindo os dados no HBase utilizando a 
# função insert_to_hbase.

# A função insert_to_hbase utiliza a biblioteca happybase para estabelecer uma conexão com o HBase e inserir os dados na 
# tabela especificada.

# Para executar este código, é necessário:
#   ajustar as configurações do HBase e do Flume, 
#   bem como definir o número de campos esperados em cada linha de log (<número_de_campos>);
#   e o intervalo de processamento em segundos (<intervalo_de_processamento_em_segundos>).

if __name__ == "__main__":

    # Configuração do contexto de streaming do Spark
    sc = SparkContext(appName='LogProcessing', master='local')
    ssc = StreamingContext(sc, 1)

    # Cria um DStream que lê dados do Kafka
    kafkaStream = KafkaUtils.createStream(ssc, "localhost:2181", "grupo", {"logs": 1})

    # Processa os dados recebidos pelo DStream
    kafkaStream.map(lambda x: x[1]).foreachRDD(process_logs)

    
    # Inicia o processamento de streaming
    ssc.start()
    ssc.awaitTermination()


# Estamos configurando o contexto de streaming do Spark com um intervalo de tempo de 1 segundo (1 em segundos), 
# criando um DStream que lê dados do Kafka através de um cluster Zookeeper que está executando localmente na porta padrão 2181. 
# Estamos especificando que o grupo que o Spark Streaming usará é "grupo" e que o tópico que será lido é "logs", 
# com um fator de replicação de 1 (ou seja, apenas uma cópia dos dados será lida).

# Observe que a função lambda passada para o map() extrai o segundo elemento da tupla, que contém o valor real da mensagem recebida do Kafka.

# Com base no exemplo de arquivo log fornecido, cada registro do arquivo log possui 9 campos separados por espaços em branco. Esses campos são:
# 1.  endereço IP do cliente (ou nome de host, se a resolução reversa estiver habilitada)
# 2.  identificador de cliente remoto (geralmente "-")
# 3.  nome de usuário (geralmente "-")
# 4.  data e hora em que a solicitação foi recebida
# 5.  método HTTP (GET, POST, etc.)
# 6.  caminho do recurso solicitado
# 7.  protocolo HTTP utilizado (geralmente "HTTP/1.0" ou "HTTP/1.1")
# 8.  código de status HTTP retornado pelo servidor (200, 404, etc.)
# 9.  tamanho do arquivo retornado em bytes (geralmente "-")



spark-submit --master local[2] processamento_log.py

spark-submit processamento_log.py
