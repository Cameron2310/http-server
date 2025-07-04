# tls-server

## About
The goal of this project was to help me learn the intricate details of HTTP & TLS.

## Setup
1. Clone repo
2. Create .venv, activate .venv, & run `pip install -r requirements.txt`
3. Create a SSL cert & private key in the `tls` directory with OpenSSL `openssl req -x509 -newkey rsa:2048 -keyout private_key.pem -out server.crt -sha256 -days 1095 -nodes`.
    a. If you change the name of the private key or certm, you will have to change it in `tls/utils.py`
4. Run `python3 main.py`
5. Make `curl` requests against it. Check out the `routing.py` for options. The `/file` path does not work with HTTPS.
