from socket import *
import threading
import time
import os
from tracemalloc import start
from termcolor import colored
import pprint

class Chat:

    def __init__(self, myip, port, username, start, debug):
        self.myip                               = myip
        self.port                               = port
        self.username                           = username
        host_name                               = gethostname()
        self.ip                                 = gethostbyname(host_name)
        self.children                           = []
        self.childrenLastUpdates                = {}
        self.siblings                           = []
        self.host                               = None
        self.socket                             = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", port))
        self.start                              = start
        self.debug                              = debug
        self.timeoutTimer                       = time.time()
        self.firstInstanceSon                   = start
        self.sendNewHostInfoNextIteration       = False

    def __timer_sender(self):
        while True:
            time.sleep(15)
            if self.debug == True:
                print(colored("[DEBUG] ", "cyan"), "Enviando mensagem para filhos para checar integridade da comunicação.")
            message = 'confirmExistence'
            aux = ""
            for childrenAddress in self.children:
                aux += childrenAddress[0] + ":" + str(childrenAddress[1]) + ","
            for address in self.children:
                self.socket.sendto(message.encode('ascii'), address)
                self.socket.sendto(aux.encode('ascii'), address)
            message = 'confirmChildExistence'
            if self.host != None:
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), "Enviando mensagem para pai para checar integridade da comunicação.")
                self.socket.sendto(message.encode('ascii'), self.host)
            if self.sendNewHostInfoNextIteration == True:
                self.host = None
                message = 'newHostInfo'
                newHostInfo = '{}:{}'.format(self.myip, self.port)
                for address in self.children:
                    self.socket.sendto(message.encode('ascii'), address)
                    self.socket.sendto(newHostInfo.encode('ascii'), address)
                print(colored("[INFO] ", "blue"), "Esse dispositivo foi eleito para ser o novo host.")
                self.firstInstanceSon = True
                self.sendNewHostInfoNextIteration = False
            if self.host == None:
                message = 'confirmImHost'
                for address in self.children:
                    self.socket.sendto(message.encode('ascii'), address)
        pass
 
    def __timer_reciever(self):
        while True:
            if self.host != None:
                if time.time() - self.timeoutTimer >= 17:
                    print(colored("[ERROR] ", "red"), "Timeout na comunicão. Elemento não está conseguindo se comunicar com pai/ host.")
                    print(colored("[INFO] ", "blue"), "O sistema irá tentar eleger um novo host. Aguarde...")
                    electionResult = self.electionSystem(self.siblings)
                    if electionResult[1] != True:
                        return
                    self.siblings.remove((self.myip, self.port))
                    for sibling in self.siblings:
                        self.childrenLastUpdates[sibling] = time.time()
                    self.children += self.siblings
                    self.sendNewHostInfoNextIteration = True
                    pass
            childrenToRemove = []
            for child in self.children:
                if time.time() - self.childrenLastUpdates[child] >= 17:
                    if self.debug == True:
                        print(colored("[DEBUG] ", "cyan"), 'O filho {} deixou de responder. Ele será removido do chat.'.format(child))
                    childrenToRemove.append(child)
            for childToRemove in childrenToRemove:
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), 'Removendo o filho {}.'.format(child))
                self.children.remove(childToRemove)
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), 'Filho {} removido com sucesso.'.format(childToRemove))
                print(colored("[INFO] ", "blue"), 'O usuário de conexão {} saiu do chat.'.format(childToRemove))
        
        pass

    # Thread receptora de mensagens
    def __receive(self):
        self.timeoutTimer = time.time()

        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                msg = data.decode('ascii')

            except:
                print(colored("[ERROR] ", "red"), "Falha ao receber a mensagem.")
                self.socket.close()
                os._exit(1)

            if msg == "new":
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), "Message: new.")
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
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), "Message: newChild.")
                try:
                    self.children.append(address)
                    self.childrenLastUpdates[address] = time.time()
                    self.socket.sendto("added".encode('ascii'), address)
                    print(colored("[INFO] ", "blue"), "Um novo elemento foi inserido nessa folha.")

                except:
                    print(colored("[ERROR] ", "red"), "Não foi possível adicionar novo elemento.")
                    self.socket.close()
                    os._exit(1)
            elif msg == "exit":
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), "Message: exit.")
                data, address = self.socket.recvfrom(1024)
                for adrs in data.decode('ascii').split(','):
                    if adrs != "":
                        aux = adrs.split(':')
                        self.children.append((aux[0],int(aux[1])))
            elif msg == "confirmExistence":
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), "Mensagem de integridade recebida do pai.")
                self.timeoutTimer = time.time()
                # Recebe a lista de siblings
                data, address = self.socket.recvfrom(1024)
                for adrs in data.decode('ascii').split(','):
                    if adrs != "":
                        aux = adrs.split(':')
                        if not (aux[0],int(aux[1])) in self.siblings:
                            self.siblings.append((aux[0],int(aux[1])))
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), 'Siblings: {}'.format(data.decode('ascii')))
                pass
            elif msg == "confirmChildExistence":
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), 'Mensagem de integridade recebida do filho: {}.'.format(address))
                self.childrenLastUpdates[address] = time.time()
                pass
            elif msg == "confirmImHost":
                self.firstInstanceSon = True
                if self.debug == True:
                    print(colored("[DEBUG] ", "cyan"), "Definindo este nó como um filho direto do host e futuro candidato a host em caso de falha.")
            elif msg == "newHostInfo":
                data, address = self.socket.recvfrom(1024)
                newHost = data.decode('ascii')
                newHostTuple = (newHost.split(':')[0], int(newHost.split(':')[1]))
                self.host = newHostTuple
                for child in self.children:
                    self.socket.sendto(newHost, child)
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
            # Responsável por lidar com a saída planejada
            user_input = input('')
            if user_input == "exit":
                if self.host == None:
                    for adrs in self.children:
                        # Se esse for o caso o node que saiu voluntariamente é o Host da aplicação, logo o chat é encerrado.
                        self.socket.sendto("Chat Finalizado".encode('ascii'), adrs)
                else:
                    aux = ""
                    self.socket.sendto("exit".encode('ascii'), self.host)
                    for adrs in self.children:
                        aux += adrs[0] + ":" + str(adrs[1]) + ","
                    self.socket.sendto(aux.encode('ascii'), self.host)
                print(colored("[INFO] ", "blue"), "Chat finalizado com sucesso.", self.ip)
                self.socket.close()
                os._exit(1)
            if user_input == "debugState":
                print(colored("[DEBUG] ", "cyan"), '------------------ESTADO DA APLICAÇÃO------------------')
                print(colored("[DEBUG] ", "cyan"), 'Port: {}'.format(self.port))
                print(colored("[DEBUG] ", "cyan"), 'Username: {}'.format(self.username))
                print(colored("[DEBUG] ", "cyan"), 'IP: {}'.format(self.ip))
                print(colored("[DEBUG] ", "cyan"), 'Children and Last Updates:')
                pprint.pprint(self.childrenLastUpdates)
                print(colored("[DEBUG] ", "cyan"), 'Host: {}'.format(self.host))
                print(colored("[DEBUG] ", "cyan"), 'Socket: {}'.format(self.socket))
                print(colored("[DEBUG] ", "cyan"), 'Start: {}'.format(self.start))
                print(colored("[DEBUG] ", "cyan"), 'Debug: {}'.format(self.debug))
                print(colored("[DEBUG] ", "cyan"), 'TimeoutTimer: {}'.format(self.timeoutTimer))
                print(colored("[DEBUG] ", "cyan"), '-------------------------------------------------------')
                continue

            # Responsável por formatar o resto das mensagens
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
        print(colored("[INFO] ", "blue"), 'Iniciando Thread de integridade de envio de mensagens.')
        timer_thread = threading.Thread(target=self.__timer_reciever, args=())
        timer_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')
        print(colored("[INFO] ", "blue"), 'Iniciando Thread de integridade de elementos.')
        timer_thread = threading.Thread(target=self.__timer_sender, args=())
        timer_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')


    # Conecta-se a um chat
    def useChat(self, ip, porta):
        self.host = (ip, porta)
        address_list = []
        address_list.append(self.host)
        i = 0
        minTime = 0
        auxAddress = None

        self.socket.settimeout(2)
        while(i < len(address_list)):
            start = time.time()
            self.socket.sendto("new".encode('ascii'), address_list[i])
            try:
                data, address = self.socket.recvfrom(1024)
                for address in data.decode('ascii').split(','):
                    if address != "":
                        aux = address.split(':')
                        address_list.append((aux[0],int(aux[1])))
            except:
                pass
            temp = time.time() - start
            if temp < minTime or minTime == 0:
                minTime = temp
                auxAddress = address_list[i]
            i += 1
        self.socket.settimeout(200)

        if auxAddress == None:
            print(colored("[ERROR] ", "red"), "Falha ao iniciar nova conexão. Se a conexão parou de forma inesperada aguarde 20 segundos e tente novamente.")
            self.socket.close()
            quit()

        else:
            self.socket.sendto("newChild".encode("ascii"), auxAddress)
            data, address = self.socket.recvfrom(1024)

            if data.decode("ascii") == "added":
                print(colored("[INFO] ", "blue"), "Conexão realizada com sucesso.")

            else:
                print(colored("[ERROR] ", "red"), "Falha ao iniciar nova conexão. Se a conexão parou de forma inesperada aguarde 20 segundos e tente novamente.")
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
        print(colored("[INFO] ", "blue"), 'Iniciando Thread de integridade de envio de mensagens.')
        timer_thread = threading.Thread(target=self.__timer_reciever, args=())
        timer_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')
        print(colored("[INFO] ", "blue"), 'Iniciando Thread de integridade de recepção de mensagens.')
        timer_thread = threading.Thread(target=self.__timer_sender, args=())
        timer_thread.start()
        print(colored("[INFO] ", "blue"), 'Thread iniciada com sucesso.')

    # O sistema de eleição será básico e utilizará como parametro para o próximo lider aquele que tiver a menor porta de conexão. O critério pode ser qualquer um e arbitrário.
    def electionSystem(self, candidates):
        listOfPorts = []
        for candidate in candidates:
            listOfPorts.append(candidate[1])
        selectedPort = min(listOfPorts)
        selectedIndex = listOfPorts.index(selectedPort)
        isMe = False
        if (self.myip, self.port) == candidates[selectedIndex]:
            isMe = True
        return (candidates[selectedIndex], isMe)

