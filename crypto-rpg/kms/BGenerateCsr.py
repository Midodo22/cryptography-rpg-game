# generate_kms_csr.py
from google.cloud import kms_v1
from asn1crypto import pem, csr, keys, algos
import hashlib
import os

def generate_kms_signed_csr():
    # Google Cloud KMS 設定
    project_id = "cryptography-final-project"
    location_id = "global"
    key_ring_id = "game-key-ring"
    crypto_key_id = "rsa-sign-key"
    crypto_key_version = "1"

    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, crypto_key_id, crypto_key_version
    )

    if not os.path.isfile("kms/data/player_public_key.pem"):
        print("Nobody hears you.\n")
        return 0
    
    # 讀取之前儲存的 public key PEM
    with open("kms/data/player_public_key.pem", "rb") as f:
        public_key_pem = f.read()

    # 轉 ASN.1 PublicKeyInfo
    if pem.detect(public_key_pem):
        _, _, der_bytes = pem.unarmor(public_key_pem)
    else:
        der_bytes = public_key_pem

    public_key_info = keys.PublicKeyInfo.load(der_bytes)

    # 構造 CertificationRequestInfo
    subject = csr.Name.build({
        "common_name": "player123"
    })
    csr_info = csr.CertificationRequestInfo({
        "version": "v1",
        "subject": subject,
        "subject_pk_info": public_key_info,
        "attributes": []
    })

    # 計算 SHA256 digest
    tbs_bytes = csr_info.dump()
    digest = hashlib.sha256(tbs_bytes).digest()

    # 使用 KMS 簽名
    sign_response = client.asymmetric_sign(
        request={
            "name": key_version_name,
            "digest": {"sha256": digest}
        }
    )
    signature = sign_response.signature

    # 組合完整 CSR
    signature_algorithm = algos.SignedDigestAlgorithm({
        "algorithm": "sha256_rsa"
    })
    final_csr = csr.CertificationRequest({
        "certification_request_info": csr_info,
        "signature_algorithm": signature_algorithm,
        "signature": signature
    })

    # 儲存 PEM 格式 CSR
    pem_bytes = pem.armor("CERTIFICATE REQUEST", final_csr.dump())
    with open("kms/data/kms_signed_player.csr", "wb") as f:
        f.write(pem_bytes)

    # print("✅ 成功產生 CSR（使用 KMS 簽名），已儲存為 kms_signed_player.csr")
    print('A hand reaches through the window and gives you an old key.\n')
    return 'CSR'

if __name__ == "__main__":
    generate_kms_signed_csr()