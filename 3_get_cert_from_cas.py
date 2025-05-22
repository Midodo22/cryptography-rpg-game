from google.cloud.security import privateca_v1 as privateca
from cryptography import x509
from cryptography.hazmat.primitives import serialization
import time

def get_cert_from_cas():
    # === 參數設定 ===
    project_id = "cryptography-final-project"
    location = "us-central1"  # 你部署 CA pool 的位置
    ca_pool_id = "game-ca-pool"
    ca_id = "my-root-ca"
    csr_path = "kms_signed_player.csr"
    cert_output_path = "player_cert.pem"

    # === 初始化 CAS 客戶端 ===
    client = privateca.CertificateAuthorityServiceClient()

    # === 讀取 CSR ===
    with open(csr_path, "rb") as f:
        csr_pem = f.read()

    # === 構造 Certificate 欲簽發的內容 ===
    parent = client.ca_pool_path(project=project_id, location=location, ca_pool=ca_pool_id)
    certificate = privateca.Certificate(
        pem_csr=csr_pem.decode("utf-8"),
        lifetime={"seconds": 31536000},  # 1 年
        certificate_template=None,
    )

    # === 發送請求簽發憑證 ===
    certificate_id = f"player-cert-{int(time.time())}"
    request = privateca.CreateCertificateRequest(
        parent=parent,
        certificate=certificate,
        certificate_id=certificate_id,  # 憑證名稱 ID，可自訂
    )

    response = client.create_certificate(request=request)

    # === 儲存簽發結果（PEM）===
    cert_pem = response.pem_certificate.encode("utf-8")
    with open(cert_output_path, "wb") as f:
        f.write(cert_pem)

    print(f"成功產生憑證，儲存為 {cert_output_path}")

if __name__ == "__main__":
    get_cert_from_cas()
