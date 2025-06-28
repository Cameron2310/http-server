# http-server

## Setup
1. Clone repo
2. Create .venv, activate .venv, & run `pip install -r requirements.txt`
3. Create a SSL cert & private key in the `tls` directory with OpenSSL (openssl req -x509 -newkey rsa:4096 -keyout private_key.pem -out server.crt -sha256 -days 1095).
