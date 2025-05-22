# get_signed_public_key.py
from google.cloud import kms_v1

def export_kms_public_key():
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

    # 取得 Public Key（PEM 格式）
    public_key_response = client.get_public_key(request={"name": key_version_name})
    public_key_pem = public_key_response.pem.encode()

    # 儲存到檔案
    with open("player_public_key.pem", "wb") as f:
        f.write(public_key_pem)

    print("已從 KMS 取得簽章用 public key，儲存為 player_public_key.pem")

if __name__ == "__main__":
    export_kms_public_key()