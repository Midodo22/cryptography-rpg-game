from google.cloud import kms_v1
from asn1crypto import pem, csr, keys, algos
import hashlib

# KMS 參數
project_id = "cryptography-final-project"
location_id = "global"
key_ring_id = "game-key-ring"
crypto_key_id = "rsa-sign-key"
crypto_key_version = "1"

client = kms_v1.KeyManagementServiceClient()

key_version_name = client.crypto_key_version_path(
    project_id, location_id, key_ring_id, crypto_key_id, crypto_key_version
)

# 1. 從 KMS 取得公鑰 PEM
public_key_resp = client.get_public_key(request={"name": key_version_name})
public_key_pem = public_key_resp.pem.encode("utf-8")

# 2. 將 PEM 公鑰轉成 asn1crypto PublicKeyInfo
if pem.detect(public_key_pem):
    type_name, headers, der_bytes = pem.unarmor(public_key_pem)
else:
    der_bytes = public_key_pem

public_key_info = keys.PublicKeyInfo.load(der_bytes)

# 3. 建立 CSR Info (CertificationRequestInfo)
subject = csr.Name.build({
    'common_name': 'game-player.example.com'
})

csr_info = csr.CertificationRequestInfo({
    'version': 'v1',
    'subject': subject,
    'subject_pk_info': public_key_info,
    'attributes': []
})

# 4. 計算 CSR Info bytes 並作 SHA256 摘要
tbs_bytes = csr_info.dump()
digest = hashlib.sha256(tbs_bytes).digest()

# 5. 用 KMS 私鑰簽名 CSR Info 的摘要
sign_response = client.asymmetric_sign(
    request={
        "name": key_version_name,
        "digest": {"sha256": digest}
    }
)
signature = sign_response.signature

# 6. 建立完整 CSR 結構，直接用原始簽名字節，不用 BitString.load()
signature_algorithm = algos.SignedDigestAlgorithm({
    'algorithm': 'sha256_rsa'
})

final_csr = csr.CertificationRequest({
    'certification_request_info': csr_info,
    'signature_algorithm': signature_algorithm,
    'signature': signature  # 直接放 bytes
})

# 7. 輸出 PEM 格式 CSR
pem_bytes = pem.armor("CERTIFICATE REQUEST", final_csr.dump())
with open("kms_signed_player.csr", "wb") as f:
    f.write(pem_bytes)

print("完成 CSR，已儲存為 kms_signed_player.csr")
