import os
from google.cloud import kms
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from kms.ExportRsaPublicKey import export_public_key
import os

def encryption(message, ciphertext_file, dek_file):
    export_public_key()
    
    # 設定資訊
    project_id = "cryptography-final-project"
    location_id = "global"
    key_ring_id = "game-key-ring"
    key_id = "rsa-key"
    key_version_id = "1"

    # 要加密的訊息
    plaintext_message = message

    # 初始化 KMS client
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    # 1. 使用 AES 產生 DEK 並加密訊息
    dek = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_message, None)

    # 2. 從 KMS 抓取 RSA 公鑰
    public_key = client.get_public_key(request={"name": key_name})
    public_key_pem = public_key.pem.encode("utf-8")
    rsa_public_key = serialization.load_pem_public_key(public_key_pem)

    # 3. 使用 RSA 公鑰封裝 DEK
    wrapped_dek = rsa_public_key.encrypt(
        dek,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 4. 儲存密文與封裝後的 DEK
    with open(ciphertext_file, "wb") as f:
        f.write(nonce + ciphertext)

    with open(dek_file, "wb") as f:
        f.write(wrapped_dek)

    # print("✅ 加密完成：已儲存 ciphertext 與 wrapped DEK")

if __name__ == '__main__':
    encryption()