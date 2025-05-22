import requests

# 這裡貼你的 CSR PEM（包含標頭和換行）
csr_pem = """-----BEGIN CERTIFICATE REQUEST-----
MIICVDCCATwCAQAwDzENMAsGA1UEAwwEdGVzdDCCASIwDQYJKoZIhvcNAQEBBQAD
ggEPADCCAQoCggEBAL1CZgWfD93qdAjNKWjHiIPeIzSjYyEO9/gqz3cpl8bBL5Po
erOD93UwJ4nr3Mc+esmeRLCb8cxciuFQOl3775Xdsa9rsLKYkDqAJzVRtf864Piw
zcLQvmr9YHLj6rzuJ+GxFFqqw4zMjqcPJnoRZ4zFwO5vga9AptBnWzFGEPuEJLLN
H1Xwj0Ao7Md1XCZIc//lbfKQg0eUmjGEYCWFJkYMT0Rk1Sh+kGJ15DBaZXTv0YwJ
WL1FjU86cNDgBOqZICElOa/ze4JFlZuBDOlUyCmik3Pgf5excMh19Mil1L4FEGLc
cfk4uAtnPvBZn5+cdWwsxCxWnY0nO5Usr8gTsv0CAwEAAaAAMA0GCSqGSIb3DQEB
CwUAA4IBAQAq75oaXWj9vSA3lKezv2T515n7VfW1hkLKhqH/xaAuUnkJRQtVCMCC
XfV5NcACW0r72JAtbXUB7dKb3pYFPdeamIX0Id8jtWroSLantj+i03TC6lBnQXED
yYuA49Tez9LqKqm7ym9H43V01VJ5Yx2cYG3etsmaZrh3AGZLSRWjC9kW7k82aYMi
FcSdrfwzmpjD6PJlToUt2/dpzPshpg2EpGaCGKxMAq8Y+0q4pfYtD6Jk2SIKf76C
yGp5nYvddVEdiqGuHI/ttGSAdMTxt04gFtWa1s1N6er44X33XA++ka9fN8MdoGIT
FLUS+M6C3LAcyapBQ1GG2nRslz4Ce6qQ
-----END CERTIFICATE REQUEST-----"""

response = requests.post(
    "http://localhost:5000/sign_csr",
    json={"csr_pem": csr_pem}
)

if response.status_code == 200:
    data = response.json()
    print("成功取得簽署憑證：")
    print(data["signed_cert_pem"])
else:
    print("發生錯誤:", response.status_code, response.text)
