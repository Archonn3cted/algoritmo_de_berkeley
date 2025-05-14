import socket
import datetime
from dateutil import parser
from colorama import Fore, init
import threading
import time

init(autoreset=True) 

conexoes = []
horarios_recebidos = []
esperando_conexoes = True

# Aceita conexões iniciais dos slaves
def aceitar_conexoes(servidor):
    global esperando_conexoes
    while esperando_conexoes:
        try:
            servidor.settimeout(1)
            conn, endereco = servidor.accept()
            print(Fore.LIGHTGREEN_EX + f"[MESTRE] Slave conectado: {endereco}")
            conexoes.append(conn)
        except socket.timeout:
            continue
        except Exception as e:
            print(Fore.RED + f"[ERRO] Falha na accept: {e}")

# Envia solicitação de hora a um slave e recebe o relógio
def solicitar_hora(conn, slave_id):
    try:
        # manda comando de requisição de tempo
        conn.send(b"REQUEST_TIME")
        print(Fore.CYAN + f"[MESTRE] Pedido de hora enviado ao Slave {slave_id}")
        # recebe o horário enviado pelo slave
        data = conn.recv(1024).decode()
        horario_slave = parser.parse(data)
        horarios_recebidos.append(horario_slave)
        print(Fore.YELLOW + f"[MESTRE] Horário recebido de Slave {slave_id}: {horario_slave.strftime('%H:%M:%S.%f')}")
    except Exception as e:
        print(Fore.RED + f"[ERRO] Comunicação com Slave {slave_id}: {e}")

# Thread para aguardar ENTER e parar recepção de conexões
def aguardar_enter():
    global esperando_conexoes
    input(Fore.MAGENTA + "[MESTRE] Pressione ENTER para iniciar sincronização...\n")
    esperando_conexoes = False

# Função principal do servidor mestre
def iniciar_servidor(porta=8080):
    servidor = socket.socket()
    servidor.bind(('0.0.0.0', porta))
    servidor.listen()
    print(Fore.BLUE + f"[MESTRE] Aguardando conexões de slaves em 0.0.0.0:{porta}")

    # Inicia thread para aceitar conexões
    tc = threading.Thread(target=aceitar_conexoes, args=(servidor,))
    tc.start()
    aguardar_enter()
    tc.join()

    if not conexoes:
        print(Fore.RED + "[MESTRE] Nenhum slave conectado. Encerrando.")
        servidor.close()
        return

    # Fase de requisição de hora a todos os slaves em paralelo
    print(Fore.BLUE + "[MESTRE] Iniciando requisição de hora a todos os slaves...")
    threads_req = []
    for idx, conn in enumerate(conexoes, start=1):
        t = threading.Thread(target=solicitar_hora, args=(conn, idx))
        t.start()
        threads_req.append(t)
    for t in threads_req:
        t.join()

    # Inclui o próprio relógio do mestre
    horario_mestre = datetime.datetime.now()
    horarios_recebidos.append(horario_mestre)
    print(Fore.CYAN + f"[MESTRE] Relógio local do mestre: {horario_mestre.strftime('%H:%M:%S.%f')}")

    # Calcula média dos timestamps
    media_ts = sum(h.timestamp() for h in horarios_recebidos) / len(horarios_recebidos)
    novo_horario = datetime.datetime.fromtimestamp(media_ts)
    print(Fore.GREEN + f"[MESTRE] Horário sincronizado calculado: {novo_horario.strftime('%H:%M:%S.%f')}")

    # Envia novo horário sincronizado para cada slave
    print(Fore.BLUE + "[MESTRE] Enviando horário sincronizado aos slaves...")
    threads_sync = []
    for idx, conn in enumerate(conexoes, start=1):
        def enviar_sync(c=conn, sid=idx):
            try:
                c.send(str(novo_horario).encode())
                c.close()
                print(Fore.LIGHTGREEN_EX + f"[MESTRE] Synchronization enviada ao Slave {sid}")
            except Exception as e:
                print(Fore.RED + f"[ERRO] Falha ao enviar sync ao Slave {sid}: {e}")
        t = threading.Thread(target=enviar_sync)
        t.start()
        threads_sync.append(t)
    for t in threads_sync:
        t.join()

    servidor.close()
    print(Fore.GREEN + "[MESTRE] Sincronização concluída.")

if __name__ == '__main__':
    iniciar_servidor(porta=8080)