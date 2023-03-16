import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Criando o bloco genesis
        self.new_block(proof=100, previous_hash='1')

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco na blockchain

        :param proof: <int> A prova fornecida pelo algoritmo de prova de trabalho
        :param previous_hash: (Opcional) <str> Hash do bloco anterior
        :return: <dict> Novo bloco
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Resetando a lista de transações atuais
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Cria uma nova transação que será adicionada ao próximo bloco

        :param sender: <str> Endereço do remetente
        :param recipient: <str> Endereço do destinatário
        :param amount: <int> Valor da transação
        :return: <int> O índice do bloco que conterá esta transação
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Cria um hash SHA-256 do bloco

        :param block: <dict> Bloco
        :return: <str> Hash do bloco
        """

        # Certifique-se de que o dicionário está ordenado, ou teremos hashes inconsistentes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Retorna o último bloco na blockchain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Implementa o algoritmo de prova de trabalho.

        :param last_proof: <int> A prova do último bloco
        :return: <int> Uma prova válida para o bloco atual
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Verifica se a prova é válida.

        :param last_proof: <int> A prova do último bloco
        :param proof: <int> A prova atual
        :return: <bool> True se a prova é válida, False se não for.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


if __name__ == '__main__':
    # Criando uma nova instância da blockchain
    blockchain = Blockchain()

    # Adicionando algumas transações
    blockchain.new_transaction('Alice', 'Bob', 10)
    blockchain.new_transaction('Bob', 'Charlie', 5)

    # Mineração de um novo bloco
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # Imprimindo a blockchain
    print('Blockchain:')
    print(blockchain.chain)
