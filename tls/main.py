import socket
from . import client, server, utils


def handle_https_request(request: bytes, client_sock: socket.socket):
    client_hello = client.parse_client_message(request)
    server_hello = server.create_server_hello(client_hello.session_id)
    server_hello_msg = bytes(server_hello.message)

    client_sock.send(server_hello_msg)

    handshake_keys = utils.make_handshake_keys(client_hello.public_key, server_hello.private_key, request[5:], server_hello_msg[5:])
    
    change_cipher_spec = bytes([0x14, 0x03, 0x03, 0x01, 0x01, 0x01]) 
    
    s_extensions = [0x08, 0x00, 0x00, 0x02, 0x00, 0x00, 0x16]
    s_encrypted_extensions = server.create_wrapped_record(handshake_keys.shs_key, handshake_keys.shs_iv, bytes(s_extensions))
   
    cert_headers = [0x0b, 0x00, 0x03, 0x2e, 0x00]
    cert = utils.get_server_cert()

    cert_headers_len = (len(cert) + len(cert_headers)).to_bytes(3, "big")
    cert_len = len(cert).to_bytes(3, "big")
    
    cert_data = bytes(cert_headers) + cert_headers_len + cert_len + cert
    s_cert = server.create_wrapped_record(handshake_keys.shs_key, handshake_keys.shs_iv, cert_data + bytes([0x16, 0x00, 0x00]))

    client_sock.send(change_cipher_spec)
    client_sock.send(s_encrypted_extensions)
    client_sock.send(s_cert)
