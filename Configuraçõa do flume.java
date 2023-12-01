# Configuração das fontes de dados
agent.sources = source1 source2

# Configuração da primeira fonte de dados
agent.sources.source1.type = exec
agent.sources.source1.command = tail -F /var/log/NASA_access_log_Aug95

# Configuração da segunda fonte de dados
agent.sources.source2.type = exec
agent.sources.source2.command = tail -F /var/log/NASA_access_log_Jul95

# Configuração do canal
agent.channels = channel1
agent.channels.channel1.type = memory
agent.channels.channel1.capacity = 10000
agent.channels.channel1.transactionCapacity = 1000

# Configuração do sink (usando HBase como exemplo)
# agent.sinks = sink1
# agent.sinks.sink1.type = org.apache.flume.sink.hbase.HBaseSink
# agent.sinks.sink1.table = <nome_da_tabela_no_HBase>
# agent.sinks.sink1.columnFamily = <família_de_colunas_no_HBase>
# agent.sinks.sink1.batchSize = 100
# agent.sinks.sink1.serializer = org.apache.flume.sink.hbase.SimpleHbaseEventSerializer

# Configuração da ligação entre as fontes, canal e sink
agent.sources.source1.channels = channel1
agent.sources.source2.channels = channel1
agent.sinks.sink1.channel = channel1



# Configuração do destino do Flume (Spark Streaming)
agent.sinks.sink1.type = org.apache.spark.streaming.flume.sink.SparkSink
agent.sinks.sink1.channel = channel1
agent.sinks.sink1.hostname = localhost
agent.sinks.sink1.port = 9999


# Neste exemplo, o Flume está configurado para monitorar dois arquivos de log, /var/log/application1.log e /var/log/application2.log, 
# utilizando duas fontes de dados diferentes (source1 e source2). Cada fonte é configurada para executar 
# o comando tail -F no respectivo arquivo de log.

# Os dados coletados pelas fontes são enviados para um canal (channel1), que é configurado como um canal de memória com uma capacidade de 10.000 eventos.

# Os dados do canal são então enviados para um sink (sink1) configurado para gravar os eventos no HBase. Os detalhes da configuração do sink podem variar dependendo da versão do HBase e do tipo de evento a ser gravado.

# Lembre-se de que esta é apenas uma configuração básica e que é necessário ajustá-la de acordo com as necessidades do seu ambiente.






# Inicie o agente Flume usando o arquivo de configuração flume.conf:

$ flume-ng agent --conf /opt/flume/conf --conf-file flume.conf --name agent





# Esse comando é utilizado para iniciar um agente do Flume com as configurações definidas no arquivo flume.conf.

# O parâmetro agent indica que estamos iniciando um agente do Flume.
# O parâmetro --conf indica o diretório onde estão as configurações do Flume (/etc/flume-ng/conf).
# O parâmetro --conf-file indica o arquivo de configuração do Flume (flume.conf).
# O parâmetro --name define um nome para o agente (agent).
# O arquivo flume.conf contém a definição dos componentes do pipeline do Flume, como as fontes de dados, os canais e os destinos. Ao iniciar o agente com o comando acima, o Flume carregará as configurações do arquivo flume.conf e iniciará a execução do pipeline.

# Além disso, é importante notar que o Flume precisa estar instalado na máquina onde o comando está sendo executado para que seja possível iniciar o agente.


# Status do Flume 

 ps -ef | grep "[f]lume-ng agent --name agent"


 # Substitua <nome-do-agente> pelo nome que você deu para o agente quando o iniciou 
 # (por exemplo, agent). O comando irá listar os processos em execução que correspondem ao 
 # agente com o nome especificado. Se o agente estiver em execução, você deverá ver uma saída semelhante a esta:



user     1234  5678  0 10:00 ?        00:00:00 /usr/bin/java -Xmx256m -Dflume.root.logger=INFO,console -cp ...

# Onde user é o usuário que iniciou o agente, 1234 é o PID do processo correspondente ao agente, 
# e /usr/bin/java é o caminho para o executável do Java utilizado para executar o agente.

# Se você não ver nenhuma saída ao executar o comando, o agente não está em execução ou foi iniciado com um 
# nome diferente do que você especificou.