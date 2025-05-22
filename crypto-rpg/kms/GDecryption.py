from google.cloud import kms_v1
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
import datetime
import os

# === 憑證驗證 ===
def load_pem_cert(path):
    with open(path, "rb") as f:
        data = f.read()
    return x509.load_pem_x509_certificate(data, default_backend())

def verify_cert(cert_path, root_ca_path):
    cert = load_pem_cert(cert_path)
    root_ca = load_pem_cert(root_ca_path)

    now = datetime.datetime.now(datetime.timezone.utc)  # 帶時區現在時間
    if not (cert.not_valid_before_utc <= now <= cert.not_valid_after_utc):
        print("憑證不在有效期限內")
        return False
    # print("憑證在有效期限內")

    try:
        root_ca.public_key().verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        # print("憑證簽章驗證成功")
    except InvalidSignature:
        print("憑證簽章驗證失敗")
        return False

    return True

# === 解封 DEK ===
def decrypt_dek_with_kms(project_id, location_id, key_ring_id, key_id, ciphertext_file):
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, "1")

    with open(ciphertext_file, "rb") as f:
        encrypted_dek = f.read()

    response = client.asymmetric_decrypt(request={
        "name": key_name,
        "ciphertext": encrypted_dek,
    })

    return response.plaintext

# === 解密資料 (從同一檔案讀 nonce + ciphertext) ===
def decrypt_data(dek: bytes, combined_file: str, nonce_len=12) -> str:
    with open(combined_file, "rb") as f:
        data = f.read()

    nonce = data[:nonce_len]
    ciphertext = data[nonce_len:]

    aesgcm = AESGCM(dek)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

def decryption(ciphertext, dek_file):
    # === 主流程 ===
        player_cert_path = "kms/data/player_cert.pem"
        root_cert_path = "kms/my-root-ca.pem"

        if verify_cert(player_cert_path, root_cert_path):
            # print("憑證驗證成功")

            dek = decrypt_dek_with_kms(
                project_id="cryptography-final-project",
                location_id="global",
                key_ring_id="game-key-ring",
                key_id="rsa-key",
                ciphertext_file=dek_file
            )

            plaintext = decrypt_data(dek, ciphertext)
            print(plaintext)
        else:
            print("憑證驗證失敗，禁止解密")

if __name__ == '__main__':
    decryption()