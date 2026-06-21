import json
import struct

def enviar_mensagem(sock, mensagem_dict):
    mensagem_json = json.dumps(mensagem_dict)
    mensagem_bytes = mensagem_json.encode('utf-8')
    tamanho_bytes = struct.pack('I', len(mensagem_bytes))
    sock.sendall(tamanho_bytes + mensagem_bytes)

def receber_mensagem(sock):
    tamanho_bytes = _receber_exatamente(sock, 4)
    if not tamanho_bytes:
        return None
    tamanho_mensagem = struct.unpack('I', tamanho_bytes)[0]
    dados_bytes = _receber_exatamente(sock, tamanho_mensagem)
    if not dados_bytes:
        return None
    mensagem_json = dados_bytes.decode('utf-8')
    return json.loads(mensagem_json)

def _receber_exatamente(sock, num_bytes):
    dados = bytearray()
    while len(dados) < num_bytes:
        pacote = sock.recv(num_bytes - len(dados))
        if not pacote:
            return None
        dados.extend(pacote)
    return bytes(dados)