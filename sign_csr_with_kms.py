from flask import Flask, request, jsonify
from google.cloud.security import privateca_v1
import base64
import uuid
import os

app = Flask(__name__)

# Google CAS 設定（請換成你自己的環境參數）
PROJECT_ID = "cryptography-final-project"
LOCATION = "us-central1"
POOL = "game-ca-pool"
CA_NAME = "my-root-ca"

# 建立 CA 服務客戶端
client = privateca_v1.CertificateAuthorityServiceClient()

# CA 全名 (CA resource path)
ca_pool_path = client.ca_pool_path(PROJECT_ID, LOCATION, POOL)

@app.route("/sign_csr", methods=["POST"])
def sign_csr():
    # 1. 從 POST JSON 取得 CSR PEM
    data = request.json
    if not data or "csr_pem" not in data:
        return jsonify({"error": "Missing csr_pem in JSON body"}), 400

    csr_pem = data["csr_pem"]

    # 2. 檢查並確保 CSR 是 PEM 格式 (可選)
    if not (csr_pem.startswith("-----BEGIN CERTIFICATE REQUEST-----") and 
            csr_pem.strip().endswith("-----END CERTIFICATE REQUEST-----")):
        return jsonify({"error": "csr_pem 格式錯誤，需包含 PEM 標頭尾"}), 400

    # 3. 建立 Certificate 物件，設定簽發期限為 1 年
    certificate = privateca_v1.Certificate(
        pem_csr=csr_pem,
        lifetime={"seconds": 365 * 24 * 60 * 60}
    )

    certificate_id = f"cert-{uuid.uuid4().hex[:8]}"
    # 4. 建立 CreateCertificateRequest，certificate_id 空字串讓系統自動產生
    request_obj = privateca_v1.CreateCertificateRequest(
        parent=ca_pool_path,
        certificate=certificate,
        certificate_id=certificate_id
    )

    try:
        # 5. 呼叫 Google CAS 產生憑證
        response = client.create_certificate(request=request_obj)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 6. 取得簽發憑證 PEM
    signed_cert_pem = response.pem_certificate

    # 7. 將簽發憑證寫入檔案（可選，目錄要存在）
    os.makedirs("signed_certs", exist_ok=True)
    cert_filename = response.name.split("/")[-1] + ".pem"
    cert_path = os.path.join("signed_certs", cert_filename)
    with open(cert_path, "w") as f:
        f.write(signed_cert_pem)

    # 8. 回傳簽發憑證 PEM
    return jsonify({"signed_cert_pem": signed_cert_pem})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
