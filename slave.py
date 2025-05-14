import socket
import datetime
import random
from dateutil import parser
from colorama import Fore, init
import uuid

init(autoreset=True)

# ID do slave para logs
slave_id = str(uuid.uuid4())[:4]

# Desvio inicial aleatório em segundos entre -10 e +10
desvio_inicial = random.randint(-10, 10)
relogio_local = datetime.datetime.now() + datetime.timedelta(seconds=desvio_inicial)
print(Fore.YELLOW + f"[SLAVE {slave_id}] Relógio local com desvio de {desvio_inicial:+} segundos: {relogio_local.strftime('%H:%M:%S.%f')}")

def iniciar_cliente(host='127.0.0.1', porta=8080):
    cliente_socket = socket.socket()
    try:
        cliente_socket.connect((host, porta))
        print(Fore.GREEN + f"[SLAVE {slave_id}] Conectado ao mestre.")
    except Exception as e:
        print(Fore.RED + f"[SLAVE {slave_id}] Erro ao conectar: {e}")
        return

    try:
        # Aguarda comando de requisição de hora
        cmd = cliente_socket.recv(1024).decode()
        if cmd.strip() == 'REQUEST_TIME':
            print(Fore.CYAN + f"[SLAVE {slave_id}] Pedido de hora recebido do mestre.")
            # Envia o horário local
            cliente_socket.send(str(relogio_local).encode())
            print(Fore.CYAN + f"[SLAVE {slave_id}] Horário enviado: {relogio_local.strftime('%H:%M:%S.%f')}")
        else:
            print(Fore.RED + f"[SLAVE {slave_id}] Comando inesperado: {cmd}")
            cliente_socket.close()
            return

        # Recebe o horário sincronizado do mestre
        data = cliente_socket.recv(1024).decode()
        tempo_sincronizado = parser.parse(data)
        print(Fore.GREEN + f"[SLAVE {slave_id}] Novo horário recebido: {tempo_sincronizado.strftime('%H:%M:%S.%f')}")

    except Exception as e:
        print(Fore.RED + f"[SLAVE {slave_id}] Erro durante comunicação: {e}")
    finally:
        cliente_socket.close()

if __name__ == '__main__':
    iniciar_cliente()
