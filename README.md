# tls-server

## About
The goal of this project was to help me learn the intricate details of HTTP & TLS 1.3.

## Setup
1. Clone repo
2. Create .venv, activate .venv, & run `pip install -r requirements.txt`
3. Create a SSL cert & private key in the `tls` directory with OpenSSL `openssl req -x509 -newkey rsa:2048 -keyout cert_priv_key.pem -out server_cert.pem -sha256 -days 1095 -nodes`.
    a. If you change the name of the private key or certm, you will have to change it in `tls/utils.py`
4. Run `python3 main.py`
5. Make `curl` requests against it with `--cacert <path to server cert created above>`. Check out the `routing.py` for options. The `/file` path does not work with HTTPS.
