from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import datetime

def load_pem_cert(path):
    with open(path, "rb") as f:
        data = f.read()
    return x509.load_pem_x509_certificate(data, default_backend())

def verify_cert(cert_path, root_ca_path):
    # 載入玩家憑證與根憑證
    cert = load_pem_cert(cert_path)
    root_ca = load_pem_cert(root_ca_path)

    # 取得現在UTC時間（避免 CryptographyDeprecationWarning）
    now = datetime.datetime.now(datetime.timezone.utc)

    # 驗證憑證是否在有效期內（使用 .not_valid_before_utc, .not_valid_after_utc）
    if not (cert.not_valid_before_utc <= now <= cert.not_valid_after_utc):
        print("憑證不在有效期限內")
        return False
    print("憑證在有效期限內")

    # 驗證憑證簽章 (使用根憑證公鑰驗簽)
    try:
        root_ca.public_key().verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm
        )
        print("憑證簽章驗證成功")
    except InvalidSignature:
        print("憑證簽章驗證失敗")
        return False

    # 其他驗證可自行補充

    return True

def verify_run():
    player_cert = "player_cert.pem"  # 你剛剛從 CAS 取得的憑證
    root_ca_cert = "my-root-ca.pem"  # 你的根憑證 PEM

    if verify_cert(player_cert, root_ca_cert):
        print("整體驗證成功！")
    else:
        print("驗證失敗！")

if __name__ == "__main__":
    verify_run()