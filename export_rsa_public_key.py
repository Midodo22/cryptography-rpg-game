from google.cloud import kms_v1
from cryptography.hazmat.primitives import serialization

client = kms_v1.KeyManagementServiceClient()

project_id = "cryptography-final-project"
location_id = "global"
key_ring_id = "game-key-ring"
crypto_key_id = "rsa-sign-key"  # 改成簽章用的 key
crypto_key_version = "1"        # 若尚未輪轉，版本通常是 1

# 組合完整的 key version 路徑
key_version_name = client.crypto_key_version_path(
    project_id, location_id, key_ring_id, crypto_key_id, crypto_key_version
)

# 取得公開金鑰（PEM 格式）
public_key = client.get_public_key(request={"name": key_version_name})
pem = public_key.pem.encode("utf-8")

# 儲存成 .pem 檔案
with open("rsa_sign_public_key.pem", "wb") as f:
    f.write(pem)

print("✅ RSA 簽章公鑰已儲存為 rsa_sign_public_key.pem")
