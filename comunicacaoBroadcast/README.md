Integrantes:
    Rafael Furlanetto Casamaximo
    Iury Pereira de Souza

Execução do programa:
- Quando alguém quiser iniciar um novo chat essa pessoa executará o comando:
    python3 main.py -u <Username> -s -mip <MeuIp> -p <MinhaPorta>
- Quando alguém quiser se conectar ao chat já iniciado deve executar o comando:
    python3 main.py -u <Username> -e -mip <MeuIp> -p <MinhaPorta> -hip <IpDoHost> -hp <PortaDoHost>
Ao executar esse comando, o host e os outros elementos se organizarão para fornecer uma lista de todos os elementos existentes na rede até o momento.
Assim, o novo elemento testará a conexão com todos e escolherá como elemento pai aquele que menos demorar para responder. Dessa forma, as conexões ficam estruturadas em forma de grafo.

- Para executar o programa em modo debug deve-se utilizar a flag -d. Esse modo mostra as mensagens do sistema e as comunicações ocultas entre pais e filhos.

Funcionamento do programa:
- Algumas mensagens são trocadas entre nodes pais e filhos para assegurar a integridade do chat:
    - O pai manda para o filho uma mensagem confirmando sua existencia a cada 15 segundos;
    - Caso o pai seja o host, ele manda também uma mensagem extra falando que o filho é um futuro candidato a host caso o pai falhe (fisrtInstanceSon);
    - O pai manda para cada filho uma cópia da lista de filhos dele, dessa forma, todos os filhos possuem uma lista de siblings. Isso é usado no sistema de eleição;
    - Os filhos mandam uma mensagem confirmando a existencia deles para o pai de 15 em 15 segundos. Caso essa mensagem não seja enviada, o pai remove o filho da lista de endereçõs para retransmissão e retira eles do chat;
    - Quando o pai de um node deixa de enviar mensagens confirmando a existencia para os filhos, cada um dos fihos realiza um algoritmo de eleição utilizando os siblings como candidatos;
    - O paramtro arbitrário de eleição utilizado é o filho com o menor número de porta e mais velho caso precise de desempate;
    - Quando a eleição ocorre existem duas possibilidades, ou o filho é escolhido como host, ou ele não é;
    - Caso ele seja escolhido como host, ele define todos seus siblings como seus filhos. Logo, ele começará a retransmitir para todos que perderam a conexão com o pai;
    - Caso ele não seja escolhido, ele aguarda um tempo e espera para ver se a conexão com o novo pai foi estabelecida;
    - Caso um pai caia e ele seja o host, o que é um caso específico porém importante, existe mais um passo na eleição;
    - A eleição do novo host é realizada e caso o filho seja um firstInstanceSon, significa que ele é filho direto do host. Logo, agora todos que enviavam mensagem para o host vão passar a enviar mensagens pra ele;
    - Dessa forma, ele envia uma mensagem que é propagada para todos os outros filhos e siblings, informando os detalhes do novo host;