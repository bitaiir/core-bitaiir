#importando as bibliotecas
from hashlib import sha256
from datetime import datetime

#criando a classe Blockchain
class Blockchain:

  #inicializando a lista de blocos e o índice
  def __init__(self):
    self.blocks = []
    self.index = 0

    #criando o bloco gênesis
    self.construct_genesis()

  #criando o método para construir o bloco gênesis
  def construct_genesis(self):
    data = "Genesis"
    timestamp = datetime.utcnow().timestamp()
    prev_hash = 0

    #chamando o método para construir um bloco com os dados acima
    self.construct_block(prev_hash, data, timestamp)

  #criando o método para construir um novo bloco
  def construct_block(self, prev_hash, data, timestamp):

    #incrementando o índice
    self.index += 1

    #calculando o hash do bloco com os dados fornecidos
    hash = self.hash_block(data, prev_hash, timestamp)

    #adicionando o bloco à lista de blocos
    self.blocks.append({
      'index': self.index,
      'timestamp': timestamp,
      'data': data,
      'hash': hash,
      'prev_hash': prev_hash})

  #criando o método para calcular o hash de um bloco usando sha256
  def hash_block(self, data, prev_hash, timestamp):

    #concatenando os dados em uma string
    block_string = str(data) + str(prev_hash) + str(timestamp)

    #codificando a string em bytes
    block_bytes = block_string.encode()

    #calculando o hash em hexadecimal e retornando-o
    return sha256(block_bytes).hexdigest()

#testando a classe Blockchain

#criando uma instância da classe Blockchain chamada chain
chain = Blockchain()

#imprimindo os blocos da chain na tela usando json.dumps para formatar melhor a saída
import json
print(json.dumps(chain.blocks, indent=4))

#adicionando alguns blocos à chain com dados fictícios
chain.construct_block(chain.blocks[-1]['hash'], "Segundo Bloco", datetime.utcnow().timestamp())
chain.construct_block(chain.blocks[-1]['hash'], "Terceiro Bloco", datetime.utcnow().timestamp())

#imprimindo novamente os blocos da chain na tela
print(json.dumps(chain.blocks, indent=4))