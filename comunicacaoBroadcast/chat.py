from socket import *
import threading
import time
import os
from termcolor import colored

class Chat:

    def __init__(self, port, username):
        self.port     = port
        self.username = username
        host_name     = gethostname()
        self.ip       = gethostbyname(host_name)
        self.children = []
        self.host     = None
        self.socket   = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", port))

    # Thread receptora de mensagens
    def __receive(self):
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                msg = data.decode('ascii')

            except:
                print(colored("[ERROR] ", "red"), "Falha ao receber a mensagem.")
                self.socket.close()
                os._exit(1)

            if msg == "new":
                try:
                    aux = ""
                    for childrenAddress in self.children:
                        aux += childrenAddress[0] + ":" + str(childrenAddress[1]) + ","
                    self.socket.sendto(aux.encode('ascii'), address)

                except:
                    print(colored("[ERROR] ", "red"), "Falha ao percorrer a lista de endereços. Tente novamente.")
                    self.socket.close()
                    os._exit(1)

            elif msg == "newChild":
                try:
                    self.children.append(address)
                    self.socket.sendto("added".encode('ascii'), address)
                    print(colored("[INFO] ", "blue"), "Um novo elemento foi inserido nessa folha.")

                except:
                    print(colored("[ERROR] ", "red"), "Não foi possível adicionar novo elemento.")
                    self.socket.close()
                    os._exit(1)
            else:
                aux = msg.split(' ')
                address = aux[0].split(':')
                if self.ip != address[0] or self.port != int(address[1]):
                    print(colored(msg, 'magenta'))
                for i in self.children:
                    self.socket.sendto(data, i)
            

    # Thread que emite as mensagens
    def __write(self):
        while True:
            user_input = input('')
            message = '{}: {}'.format(self.username, user_input)
            if self.host == None:
                for address in self.children:
                    self.socket.sendto(message.encode('ascii'), address)

            else:
                self.socket.sendto(message.encode('ascii'), self.host)
            

    # Criar novo chat
    def createChat(self):
        print(colored("[INFO] ", "blue"), "IP do chat: ", self.ip)
        print(colored("[INFO] ", "blue"), "Porta do chat: ", self.port)

        print(colored("[INFO] ", "blue"), 'Iniciando Thread para receber novas mensagens e elementos.')
        receive_thread = threading.Thread(target=self.__receive, args=())
        receive_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')
        print(colored("[INFO] ", "blue"), 'Iniciando Thread para enviar novas mensagens e elementos.')
        write_thread = threading.Thread(target=self.__write, args=())
        write_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')


    # Conecta-se a um chat
    def useChat(self, ip, porta):
        self.host = (ip, porta)
        address_list = []
        address_list.append(self.host)
        i = 0
        minTime = 0
        auxAddress = None

        while(i < len(address_list)):
            start = time.time()
            self.socket.sendto("new".encode('ascii'), address_list[i])
            data, address = self.socket.recvfrom(1024)

            for address in data.decode('ascii').split(','):
                if address != "":
                    aux = address.split(':')
                    address_list.append((aux[0],int(aux[1])))
            temp = time.time() - start
            if temp < minTime or minTime == 0:
                minTime = temp
                auxAddress = address_list[i]
            i += 1

        if auxAddress == None:
            print(colored("[ERROR] ", "red"), "Falha ao iniciar nova conexão.")
            self.socket.close()
            quit()

        else:
            self.socket.sendto("newChild".encode("ascii"), auxAddress)
            data, address = self.socket.recvfrom(1024)

            if data.decode("ascii") == "added":
                print(colored("[INFO] ", "blue"), "Conexão realizada com sucesso.")

            else:
                print(colored("[ERROR] ", "red"), "Falha ao entrar no chat.")
                self.socket.close()
                quit()

        print(colored("[INFO] ", "blue"), 'Iniciando Thread para receber novas mensagens e elementos.')
        receive_thread = threading.Thread(target=self.__receive, args=())
        receive_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')
        print(colored("[INFO] ", "blue"), 'Iniciando Thread para enviar novas mensagens e elementos.')
        write_thread = threading.Thread(target=self.__write, args=())
        write_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')