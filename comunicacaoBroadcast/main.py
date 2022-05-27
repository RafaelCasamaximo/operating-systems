from chat import Chat
import sys

def main():
    size = len(sys.argv)

    ''' 
        Flags:
            -p: Porta da nova ponta (obrigatório)
            -n: Criar novo chat
            -u: Usar chat. Passar ip e porta do host

        Exemplos:
            $ python3 ./main.py -p 44404 Iury -n (Cria um novo chat na porta 44404)
            $ python3 ./main.py -p 44405 Rafael -u 127.0.1.1 44404 (Conecta com o host 127.0.1.1:44404)
    '''

    if size > 1:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == '-p':
                chat = Chat(int(sys.argv[i + 1]), sys.argv[i + 2])

            elif sys.argv[i] == '-n':
                chat.createChat()

            elif sys.argv[i] == '-u':
                chat.useChat(sys.argv[i + 1], int(sys.argv[i + 2]))
            
            else:
                continue

    else:
        print("Leia README para executar o programa corretamente.")

if __name__ == "__main__":
    main()