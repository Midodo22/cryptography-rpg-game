from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
from google.protobuf import duration_pb2
from google.api_core.exceptions import AlreadyExists

# === 參數設定 ===
project_id = "cryptography-final-project"
location_id = "global"
key_ring_id = "game-key-ring"
decrypt_key_id = "rsa-decrypt-key"
sign_key_id = "rsa-sign-key"

# === 初始化 KMS 客戶端 ===
client = KeyManagementServiceClient()
parent = f"projects/{project_id}/locations/{location_id}"
key_ring_path = f"{parent}/keyRings/{key_ring_id}"

# === 建立 Key Ring ===
try:
    key_ring = {}
    response = client.create_key_ring(
        request={
            "parent": parent,
            "key_ring_id": key_ring_id,
            "key_ring": key_ring
        }
    )
    print(f"Created key ring: {response.name}")
except AlreadyExists:
    print(f"Key ring '{key_ring_id}' already exists.")

# === 建立 RSA 解密金鑰（用於封裝/解封 DEK）===
try:
    decrypt_key = {
        "purpose": kms_v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT,
        "version_template": {
            "algorithm": kms_v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_DECRYPT_OAEP_2048_SHA256
        }
    }
    response = client.create_crypto_key(
        request={
            "parent": key_ring_path,
            "crypto_key_id": decrypt_key_id,
            "crypto_key": decrypt_key
        }
    )
    print(f"Created RSA decryption key: {response.name}")
except AlreadyExists:
    print(f"RSA decryption key '{decrypt_key_id}' already exists.")

# === 建立 RSA 簽章金鑰（用於簽名 CSR）===
try:
    sign_key = {
        "purpose": kms_v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN,
        "version_template": {
            "algorithm": kms_v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_2048_SHA256
        }
    }
    response = client.create_crypto_key(
        request={
            "parent": key_ring_path,
            "crypto_key_id": sign_key_id,
            "crypto_key": sign_key
        }
    )
    print(f"Created RSA signing key: {response.name}")
except AlreadyExists:
    print(f"RSA signing key '{sign_key_id}' already exists.")
