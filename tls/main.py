import socket
from . import client, server, utils


def handle_https_request(request: bytes, client_sock: socket.socket):
    client_hello = client.parse_client_message(request)
    server_hello = server.create_server_hello(client_hello.session_id)
    server_hello_msg = bytes(server_hello.message)

    client_sock.send(server_hello_msg)

    handshake_keys = utils.make_handshake_keys(client_hello.public_key, server_hello.private_key, request[5:], server_hello_msg[5:])

    wrapper = server.Wrapper(handshake_keys.shs_key, handshake_keys.shs_iv, handshake_keys.chs_iv, handshake_keys.chs_key)
    change_cipher_spec = bytes([0x14, 0x03, 0x03, 0x00, 0x01, 0x01]) 
    
    s_extensions = bytes([0x08, 0x00, 0x00, 0x02, 0x00, 0x00])
    s_encrypted_extensions = wrapper.wrap(s_extensions)
   
    cert = utils.get_server_cert()
    cert_message_type = bytes([0x0b])
    cert_payload_len = (len(cert) + 4).to_bytes(3, "big")
    cert_handshake_header = cert_message_type + cert_payload_len

    request_context = bytes([0x00])
    certificates_len = bytes([0x00, 0x03, 0x2a])  # len of all certs
    cert_len = len(cert).to_bytes(3, "big")
    cert_extensions = bytes([0x00, 0x00])

    cert_data = cert_handshake_header + request_context + certificates_len + cert_len + cert + cert_extensions

    s_cert_wrapped = wrapper.wrap(cert_data)


    msgs = request[5:] + server_hello_msg[5:] + s_extensions + cert_data
    hashed_msgs = utils.hash_messages(msgs)

    signed_data = utils.sign_hash(hashed_msgs)

    cert_verify_msg_type = bytes([0x0f])
    cert_verify_payload_len = (len(signed_data) + 4).to_bytes(3, "big")
    cert_verify_header = cert_verify_msg_type + cert_verify_payload_len

    cert_verify_data = cert_verify_header + signed_data
    s_cert_verify = wrapper.wrap(cert_verify_data)


    client_sock.send(change_cipher_spec)
    client_sock.sendall(s_encrypted_extensions)
    client_sock.sendall(s_cert_wrapped)
    client_sock.sendall(s_cert_verify)


