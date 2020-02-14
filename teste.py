# Utilizado para que seja possível o uso do Spark em conjunto com o Python.
from pyspark import SparkConf, SparkContext
# Bibliteca utilizada para realizar as operações de adição.
from operator import add
# Biblioteca utilizada para garantir a interoperabilidade ao obter o path do arquivo desejado.
import pathlib   


# Atribuindo o path dos arquivos que serão utilizados.
path = pathlib.Path('access_log_Jul95')
pathJ = str(path.absolute())

path = pathlib.Path('access_log_Aug95')
pathA = str(path.absolute())

# Atribuindo as configurações do Spark que serão utilizadas.
conf = (SparkConf()
         .setMaster("local")
         .setAppName("SPark")
         .set("spark.executor.memory", "12g"))

# Criando o SparkContext e atribuindo a variável que será utilizada no programa. 
sc = SparkContext.getOrCreate();


julho = sc.textFile(pathJ)
julho = julho.cache()

agosto = sc.textFile(pathA)
agosto = agosto.cache()


# Obtendo o número de hosts únicos.
julho_count = julho.flatMap(lambda linha: linha.split(' ')[0]).distinct().count()
agosto_count = agosto.flatMap(lambda linha: linha.split(' ')[0]).distinct().count()
print(f'Número de hosts únicos no mês de julho: {julho_count}')
print(f'Número de hosts únicos no mês de agosto: {agosto_count}')


# Obtendo o total de erros 404.
def response_code_404(linha):
    try:
        code = linha.split(' ')[-2]
        if code == '404':
            return True
    except:
        pass
    return False
    
julho_404 = julho.filter(response_code_404).cache()
agosto_404 = agosto.filter(lambda linha: linha.split(' ')[-2] == '404').cache()

print(f'\nQuantidade de erros 404 no mês de julho: {julho_404.count()}')
print(f'Quantidade de erros 404 no mês de agosto: {agosto_404.count()}')


# Obtendo as 5 URLs que mais causaram erro 404.
def top5_endpoints(rdd):
    endpoints = rdd.map(lambda linha: linha.split('"')[1].split(' ')[1])
    counts = endpoints.map(lambda endpoint: (endpoint, 1)).reduceByKey(add)
    top = counts.sortBy(lambda pair: -pair[1]).take(5)
    
    print('\nTop 5 dos endpoints que mais causaram o erro 404:')
    for endpoint, count in top:
        print(endpoint, count)       
    return top

top5_endpoints(julho_404)
top5_endpoints(agosto_404)


# Obtendo a quantidade de erros 404 por dia.
def dia_count(rdd):
    dias = rdd.map(lambda linha: linha.split('[')[1].split(':')[0])
    counts = dias.map(lambda dia: (dia, 1)).reduceByKey(add).collect()
    
    print('\nQuantidade de erros 404 por dia:')
    for dia, count in counts:
        print(dia, count)
        
    return counts

dia_count(julho_404)
dia_count(agosto_404)


# Obtendo ootal de bytes retornados.
def total_bytes(rdd):
    def byte_count(linha):
        try:
            count = int(linha.split(" ")[-1])
            if count < 0:
                raise ValueError()
            return count
        except:
            return 0
        
    count = rdd.map(byte_count).reduce(add)
    return count

print(f'\nTotal de byte no mês de julho: {total_bytes(julho)}')
print(f'Total de byte no mês de agosto: {total_bytes(agosto)}')

sc.stop()