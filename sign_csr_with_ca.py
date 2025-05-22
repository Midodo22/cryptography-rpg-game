import google.cloud.security.privateca_v1 as privateca_v1
from google.protobuf import duration_pb2

def create_certificate_from_csr(
    project_id: str,
    location: str,
    ca_pool_name: str,
    ca_name: str,
    certificate_id: str,
    certificate_lifetime_seconds: int,
    csr_pem_path: str,
    output_cert_path: str
):
    # 初始化 CA Service 客戶端
    ca_service_client = privateca_v1.CertificateAuthorityServiceClient()

    # 讀取 CSR 檔案內容
    with open(csr_pem_path, "rb") as f:
        pem_csr = f.read().decode("utf-8")

    # 設定憑證的有效期限
    lifetime = duration_pb2.Duration(seconds=certificate_lifetime_seconds)

    # 建立憑證物件
    certificate = privateca_v1.Certificate(
        pem_csr=pem_csr,
        lifetime=lifetime
    )

    # 設定 CA Pool 的路徑
    parent = ca_service_client.ca_pool_path(project_id, location, ca_pool_name)

    # 建立憑證請求
    request = privateca_v1.CreateCertificateRequest(
        parent=parent,
        certificate_id=certificate_id,
        certificate=certificate,
        issuing_certificate_authority_id=ca_name
    )

    # 發送請求並取得回應
    response = ca_service_client.create_certificate(request=request)

    # 將簽署後的憑證寫入檔案
    with open(output_cert_path, "w") as f:
        f.write(response.pem_certificate)

    print(f"憑證已成功建立並儲存至 {output_cert_path}")
    print("簽署的憑證內容：")
    print(response.pem_certificate)
    print("憑證鏈：")
    for cert in response.pem_certificate_chain:
        print(cert)
