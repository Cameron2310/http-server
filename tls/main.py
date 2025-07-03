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
    cert_payload_len = (len(cert) + 9).to_bytes(3, "big")
    cert_handshake_header = cert_message_type + cert_payload_len

    request_context = bytes([0x00])
    certificates_len = (len(cert) + 5).to_bytes(3, "big")  # len of all certs
    cert_len = len(cert).to_bytes(3, "big")
    cert_extensions = bytes([0x00, 0x00])

    cert_data = cert_handshake_header + request_context + certificates_len + cert_len + cert + cert_extensions

    s_cert_wrapped = wrapper.wrap(cert_data)

    # NOTE: Cert verify
    hashed_msgs = utils.hash_messages(request[5:] + server_hello_msg[5:] + s_extensions + cert_data)
    msgs = bytes([0x20] * 64) + b"TLS 1.3, server CertificateVerify" + b"\0"

    # signed_data = utils.sign_hash(hashed_msgs, msgs)
    signed_data = utils.sign_hash(utils.hash_messages(msgs + hashed_msgs))

    algorithm_val = bytes([0x08, 0x04])
    len_signature = len(signed_data).to_bytes(2, "big")

    cert_verify_msg_type = bytes([0x0f])
    cert_verify_payload_len = (len(signed_data) + len(algorithm_val) + len(len_signature)).to_bytes(3, "big")
    cert_verify_header = cert_verify_msg_type + cert_verify_payload_len

    cert_verify_data = cert_verify_header + algorithm_val + len_signature + signed_data
    s_cert_verify = wrapper.wrap(cert_verify_data)

    # NOTE: Server Handshake Finished

    verify_hash = utils.verify_data(handshake_keys.shs, request[5:] + server_hello_msg[5:] + s_extensions + cert_data + cert_verify_data)
    hs_done_msg_type = bytes([0x14])
    hs_final_header = hs_done_msg_type + (len(verify_hash)).to_bytes(3, "big")

    s_hs_final_msg = wrapper.wrap(hs_final_header + verify_hash)

    client_sock.sendall(change_cipher_spec + s_encrypted_extensions + s_cert_wrapped + s_cert_verify + s_hs_final_msg)
    # client_sock.sendall(s_cert_wrapped)
    # client_sock.sendall(s_cert_verify)
    # client_sock.sendall(s_hs_final_msg)
    client_return = client_sock.recv(2048)
    print("\n\n client return ----> ", client_return.hex(sep=" "))

