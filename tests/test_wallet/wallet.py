import hashlib
import ecdsa
import base64

# Define a chave privada
private_key = "442db46ca1e922159529111533398760d19e46c5fa289d3d5a7b2bdbe6a15974"

# Define a mensagem que o usuário deseja assinar
message = "Exemplo de mensagem para assinatura"

# Define a função de assinatura
def sign_message(private_key, message):
    private_key_bytes = bytes.fromhex(private_key)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    signature = sk.sign(message.encode(), hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
    return signature

# Assina a mensagem
signature = sign_message(private_key, message)

# Define a função de verificação
def verify_signature(public_key, signature, message):
    vk = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    try:
        vk.verify(signature, message.encode(), hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der)
        return True
    except ecdsa.BadSignatureError:
        return False

# Define a chave pública correspondente à chave privada usada para assinar a mensagem
private_key_bytes = bytes.fromhex(private_key)
sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
public_key = sk.get_verifying_key().to_string()

# Verifica se a assinatura é válida
is_valid = verify_signature(public_key, signature, message)

# Convertendo a assinatura de hexadecimal para bytes
signature_bytes = bytes.fromhex(signature.hex())

# Codificando a assinatura em Base64
signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

# Imprime os resultados
print("Chave privada:", private_key)
print("Chave pública:", public_key.hex())
print("Mensagem:", message)
print("Assinatura:", signature.hex())
print("Assinatura (base64):", signature_b64)
print("Assinatura válida:", is_valid)
