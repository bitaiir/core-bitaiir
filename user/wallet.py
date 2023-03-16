from ecdsa.util import sigencode_der
import codecs
import hashlib
import ecdsa
import random
import time
import base58
import base64
import binascii
import os
import re


class Wallet:
    def __init__(self):
        self.POOL_SIZE = 256
        self.KEY_BYTES = 32
        self.CURVE_ORDER = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)
        self.pool = [0] * self.POOL_SIZE
        self.pool_pointer = 0
        self.prng_state = None
        self.__init_pool()

    def seed_input(self, str_input):
        time_int = int(time.time())
        self.__seed_int(time_int)
        for char in str_input:
            char_code = ord(char)
            self.__seed_byte(char_code)

    def generate_key(self):
        big_int = self.__generate_big_int()
        big_int = big_int % (self.CURVE_ORDER - 1)  # key < curve order
        big_int = big_int + 1  # key > 0
        key = hex(big_int)[2:]
        # Add leading zeros if the hex key is smaller than 64 chars
        key = key.zfill(self.KEY_BYTES * 2)
        return key

    def __init_pool(self):
        for i in range(self.POOL_SIZE):
            random_bytes = os.urandom(1)
            random_byte = int.from_bytes(random_bytes, byteorder="big")
            self.__seed_byte(random_byte)
        time_int = int(time.time())
        self.__seed_int(time_int)

    def __seed_int(self, n):
        self.__seed_byte(n)
        self.__seed_byte(n >> 8)
        self.__seed_byte(n >> 16)
        self.__seed_byte(n >> 24)

    def __seed_byte(self, n):
        self.pool[self.pool_pointer] ^= n & 255
        self.pool_pointer += 1
        if self.pool_pointer >= self.POOL_SIZE:
            self.pool_pointer = 0

    def __generate_big_int(self):
        if self.prng_state is None:
            seed = int.from_bytes(self.pool, byteorder='big', signed=False)
            random.seed(seed)
            self.prng_state = random.getstate()
        random.setstate(self.prng_state)
        big_int = random.getrandbits(self.KEY_BYTES * 8)
        self.prng_state = random.getstate()
        return big_int

    def generate_address(self, private_key):
        public_key = self.private_to_public(private_key)
        address = self.public_to_address(public_key)
        return address

    def generate_compressed_address(self, private_key):
        public_key = self.private_to_compressed_public(private_key)
        address = self.public_to_address(public_key)
        return address

    def private_to_public(self, private_key):
        private_key_bytes = codecs.decode(private_key, 'hex')
        # Get ECDSA public key
        key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        # Add bitcoin byte
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    def private_to_compressed_public(self, private_key):
        private_hex = codecs.decode(private_key, 'hex')
        # Get ECDSA public key
        key = ecdsa.SigningKey.from_string(private_hex, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        # Get X from the key (first half)
        key_string = key_hex.decode('utf-8')
        half_len = len(key_hex) // 2
        key_half = key_hex[:half_len]
        # Add bitcoin byte: 0x02 if the last digit is even, 0x03 if the last digit is odd
        last_byte = int(key_string[-1], 16)
        bitcoin_byte = b'02' if last_byte % 2 == 0 else b'03'
        public_key = bitcoin_byte + key_half
        return public_key

    def public_to_address(self, public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        # Run SHA256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        # Run ripemd160 for the SHA256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # Add network byte
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
        # Double SHA256 to get checksum
        sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_2_hex[:8]
        # Concatenate public key and checksum to get the address
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        wallet = self.base58(address_hex)
        return wallet

    def base58(self, address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        # Get the number of leading zeros and convert hex to decimal
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        # Convert hex to decimal
        address_int = int(address_hex, 16)
        # Append digits to the start of string
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        # Add '1' for each 2 leading zeros
        ones = leading_zeros // 2
        for one in range(ones):
            #b58_string = '1' + b58_string
            b58_string = "aiir" + b58_string
        return b58_string

    def privatekey_to_WIF(self, private_key):
       # extended_key = "80" + private_key # Bitcoin
        extended_key = "fe" + private_key # BitAiir
        first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()

        # add checksum to end of extended key
        final_key = extended_key + second_sha256[:8]

        # Wallet Import Format = base 58 encoded final_key
        WIF = base58.b58encode(binascii.unhexlify(final_key))

        return WIF

    def sign_message(self, private_key, message):
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        signature = sk.sign(message.encode())
        return base64.b64encode(signature).decode('utf-8')

    def verify_sign(self, public_key, message, signature):
        # Converter a mensagem para hash SHA-256
        hash_mensagem = hashlib.sha256(message.encode()).digest()

        # Decodificar a assinatura de base64
        signature = base64.b64decode(signature)

        # Public key verify
        vk = ecdsa.VerifyingKey.from_string(public_key.decode('utf-8'), curve=ecdsa.SECP256k1)

        try:
            # Verificar a assinatura usando a chave pública
            return vk.verify(signature, hash_mensagem, sigdecode=ecdsa.util.sigdecode_der)
        except ecdsa.BadSignatureError:
            # A assinatura é inválida
            return False

    # def sign_transaction(self, tx, private_key):
    #     private_key_bytes = codecs.decode(private_key, 'hex')
    #     tx_bytes = codecs.decode(tx, 'hex')
    #
    #     # Calculate the hash of the transaction
    #     tx_hash = hashlib.sha256(hashlib.sha256(tx_bytes).digest()).digest()
    #
    #     # Sign the hash using the private key
    #     sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    #     signature = sk.sign(tx_hash, hashfunc=hashlib.sha256)
    #
    #     # Encode the signature in DER format
    #     der_signature = ecdsa.util.sigencode_der_canonize(*signature)
    #
    #     # Append the hash type to the signature
    #     hash_type = b"01"
    #     signature_with_hash_type = der_signature + hash_type
    #
    #     # Add the signature to the transaction
    #     tx_signed_bytes = tx_bytes + signature_with_hash_type
    #     tx_signed_hex = codecs.encode(tx_signed_bytes, 'hex').decode('utf-8')
    #
    #     return tx_signed_hex
    #
    # def verify_transaction(self, tx_signed, public_key):
    #     public_key_bytes = codecs.decode(public_key, 'hex')
    #     tx_signed_bytes = codecs.decode(tx_signed, 'hex')
    #
    #     # Extract the signature and hash type from the signed transaction
    #     signature = tx_signed_bytes[-73:-1]
    #     hash_type = tx_signed_bytes[-1]
    #
    #     # Remove the signature and hash type from the transaction
    #     tx_bytes = tx_signed_bytes[:-73]
    #
    #     # Calculate the hash of the transaction
    #     tx_hash = hashlib.sha256(hashlib.sha256(tx_bytes).digest()).digest()
    #
    #     # Verify the signature using the public key
    #     vk = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.SECP256k1)
    #
    #     try:
    #         signature = ecdsa.util.sigdecode_der(signature, vk.pubkey.verifying_curve.order)
    #         valid_signature = vk.verify(signature, tx_hash, hashfunc=hashlib.sha256)
    #         return valid_signature
    #     except ecdsa.BadSignatureError:
    #         return False

    def generateWallet(self):
        private_key = self.generate_key()
        wallet_address = self.generate_address(private_key)
        wallet_address_compressed = self.generate_compressed_address(private_key)
        return wallet_address, wallet_address_compressed, private_key


if __name__ == "__main__":
    wallet = Wallet()
    # address, address_compressed, private_key = wallet.generateWallet()
    # print("Private Key: {0}\nAddress: {1}\nAddress Compressed: {2}".format(private_key, address, address_compressed))
    # print("WIF: {0}".format(wallet.privatekey_to_WIF(private_key).decode('utf-8')))

    message = "Hello GPT"
    address = "13rmkeG6q7wguJb8Lw6LhdUBbaVSEbA7vN"
    private_key = "442db46ca1e922159529111533398760d19e46c5fa289d3d5a7b2bdbe6a15974"

    print(wallet.private_to_public(private_key))

