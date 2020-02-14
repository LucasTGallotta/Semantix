# Semantix

1 - Qual o objetivo do comando cache em Spark?

R: No Spark, existem operações lazy evaluation, ou seja, operações em um RDD não são executadas imediatamente - ele mantém um registro de quais operações estão sendo executadas através da criação de uma DAG. Essas operações só são realmente executadas através de ações que não são operações lazy, pois só podem ser avaliadas a partir da obtenção de valores do RDD. O uso do comando cache, que é nativo do Spark, permite que resultados intermediários de operações lazy possam ser armazenados e reutilizados repetidamente. Isso gera um ganho de performance e evita a sobrecarga.

2 -  O mesmo código implementado em Spark é normalmente mais rápido que a implementação equivalente em MapReduce. Por quê?

R: Um dos motivos pelo qual o Spark é mais rápido que o MapReduce é o uso de memória. Os Jobs MapReduce fazem I/O em disco para armazenar o resultado ou passar para o próximo job, enquanto o Spark permite que os resultados dos jobs sejam gravados direto em memória. O Spark também dispõem de função nativa de cache, possibilitando que diversas operações sejam executadas sobre um mesmo dataset - o que diminui a necessidade de I/O em disco. Existem outras peculiaridades do Spark que o colocam à frente quando o assunto é performance: o fato dele manter a JVM em constante execução em cada nó, com isso criando somente uma nova thread para o novo job que será executado. Já no MapReduce, uma nova instância é criada para cada job a ser executado.

3 - Qual é a função do SparkContext?

R: O SparkContext é a primeira configuração a ser feita em uma aplicação Spark: ele representa a conexão entre o Driver Program, (hospedeiro da função main) e o Cluster Manager, servidor responsável por se comunicar com todos os nós que formam o cluster. Ele possibilita especificação e alocação de recursos, como memória, processadores (executors) e o próprio Cluster Manager que será utilizado. É possível utilizar os recursos do Spark Context fazendo o acesso através de sua variável.

4 - Explique com suas palavras o que é Resilient Distributed Datasets (RDD).

R: Os RDDs são uma abstração de dados do Spark: Resilient, Distributed & Dataset. Entre suas características, a resiliência se deve ao fato de serem tolerantes a falhas, ou seja, têm a capacidade de se recuperar caso algum dos nós do cluster venham a falhar. Também são distribuídos, já que podem estar dividos em diferentes partições em um único cluster. Há mais características em um RDD: são imutáveis (objetos que permitem apenas leitura). Para modifica-lo, é necessário fazer a transformação desejada e criar um novo RDD no qual a mudança será implementada - eles podem ser operados em paralelo e têm valores categorizado em tipo (float, string, int).

5 - GroupByKey é menos eficiente que reduceByKey em grandes dataset. Por quê?

R: A diferença está na quantidade de informações que serão trafegadas utilizando cada uma das funções - e na performance das mesmas. O reduceByKey é mais eficiente: o Spark entende que pode realizar uma operação passada como parâmetro em todos os elementos de mesma chave em cada partição para obter um resultado parcial. Isso ocorre antes de passar esses dados para os executores que vão calcular o resultado final. Com isso, será transferido um conjunto e dados menor. A função GroupByKey, por outro lado (utilizada para aplicar a agregação) não gera um cálculo de resultados parciais nos mesmos moldes. Assim, um volume muito maior de dados é desnecessariamente transferido através dos executores.

6 - Explique o que o código Scala abaixo faz.

R: Na primeira linha, o RDD "textFile" é criado. Nele, após utilizar o método textFile do objeto SparkContext, é atribuído o conteúdo de um arquivo texto que está armazenado no HDFS. Na segunda linha, um segundo RDD é criado: "counts", nele está contido o resultado de uma única coleção com todas as palavras que estão contidas no RDD criado na linha anterior (textFile). Em seguida, cada palavra da lista é transformada em um mapeamento e passa a ser chave-valor, onde a chave é a palavra e o valor é igual a 1. O comando reduceByKey, então, irá reduzir e realizar uma operação de soma para expressar a quantidade de ocorrência das palavras repetidas. Por fim, na última linha, o resultado da contagem é armazenado em um arquivo de texto no HDFS.
