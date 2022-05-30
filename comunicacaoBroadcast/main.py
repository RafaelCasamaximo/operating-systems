from email.policy import default
from chat import Chat
import click
from termcolor import colored

@click.command()
@click.option('--userName', '-u', required=True, help='Nome de usuário no chat.')
@click.option('--port', '-p', default=55555, help='Porta que será utilizada na execução. [DEFAULT=55555]')
@click.option('--start', '-s', is_flag=True, help='Flag indicando que a execução iniciará um novo chat.')
@click.option('--enter', '-e', is_flag=True, help='Flag indicando que a execução entrará em um chat já existente.')
@click.option('--debug', '-d', is_flag=True, help='Flag indicando que a execução no modo debug.')
@click.option('--hostIp', '-hip', help='IP do host para a conexão. Para essa opção ser válida o programa deverá possuir a flag --enter/ -e.')
@click.option('--hostPort', '-hp', help='Porta do host para a conexão. Para essa opção ser válida o programa deverá possuir a flag --enter/ -e.')
def cli(username, port, start, enter, debug, hostip, hostport):
    # ERROR CHECKING
    if start == False and enter == False:
        print(colored("[ERROR] ", "red"), "É necessário ou criar um chat ou entrar em um chat para a execução do programa. Execute com a flag --help para ver as opções.")
        return

    if start == True and enter == True:
        print(colored("[ERROR] ", "red"), "Não é possível criar e entrar em um chat ao mesmo tempo. Execute com a flag --help para ver as opções.")
        return

    if enter == True and (hostip == None or hostport == None):
        print(colored("[ERROR] ", "red"), "Para entrar em um chat é necessário informar o IP e a porta do host. Execute com a flag --help para ver as opções.")
        return
    if port == 55555:
        print(colored("[WARNING] ", "yellow"), "Utilizando a porta padrão", colored("55555.", "yellow"), "Essa porta pode estar sendo utilizada por outra execução ou processo. É recomendado alterar.")   
    if debug == True:
        print(colored("[DEBUG] ", "cyan"), "Executando o programa no modo debug. Mensagens de integridade serão informadas.")   

    info = colored('DUPLA: RAFAEL FURLANETTO CASAMAXIMO E IURY PEREIRA DE SOUZA', 'red', attrs=['reverse', 'blink'])
    print('\n', info, '\n')

    # INSTANCIANDO CHAT
    print(colored("[INFO] ", "blue"), "Instanciando novo chat...")
    chat = Chat(int(port), username, start, debug)
    print(colored("[INFO] ", "blue"), "Chat instanciado com sucesso.")

    if start == True:
        print(colored("[INFO] ", "blue"), "Criando nova sala...")
        chat.createChat()
        print(colored("[INFO] ", "blue"), "Sala criada com sucesso. Já é possível enviar mensagens.")
    elif enter == True:
        print(colored("[INFO] ", "blue"), "Entrando na sala...")
        chat.useChat(hostip, int(hostport))
        print(colored("[INFO] ", "blue"), "Conexão realizada com sucesso. Já é possível enviar mensagens.")
    else:
        print(colored("[ERROR] ", "red"), "Ocorreu algum erro nos argumentos. Verifique os dados e tente novamente.")
    pass

if __name__ == "__main__":
    cli()