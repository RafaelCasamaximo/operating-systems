/* Cliente RPC simples */

#include <stdio.h>
#include <string.h>
#include "notebook.h"

/*
    Implementação da Interface de comunicação RPC do cliente
*/

contact createContact(CLIENT *clnt, char name[500], char number[500], char address[500])
{
   contact newContact;
   contact *result;

    strcpy(newContact.name, name);
    strcpy(newContact.number, number);
    strcpy(newContact.address, address);

   /*
        Invoca a função remota
   */
   result = create_1 (&newContact, clnt);
   if (result == NULL)
   {
     printf ("Problemas ao chamar a função remota\n");
     exit (1);
   }
}

contact readContact(CLIENT *clnt, char name[500], char number[500], char address[500])
{
   contact newContact;
   contact *result;

    strcpy(newContact.name, name);
    strcpy(newContact.number, number);
    strcpy(newContact.address, address);

   /*
        Invoca a função remota
   */
   result = read_1 (&newContact, clnt);
   if (result == NULL)
   {
     printf ("Problemas ao chamar a função remota\n");
     exit (1);
   }
}

contact updateContact(CLIENT *clnt, char name[500], char number[500], char address[500])
{
    contact newContact;
    contact *result;

        strcpy(newContact.name, name);
        strcpy(newContact.number, number);
        strcpy(newContact.address, address);

    /*
            Invoca a função remota
    */
    result = update_1 (&newContact, clnt);
    if (result == NULL)
    {
        printf ("Problemas ao chamar a função remota\n");
        exit (1);
    }
}

contact deleteContact(CLIENT *clnt, char name[500], char number[500], char address[500])
{
    contact newContact;
    contact *result;

        strcpy(newContact.name, name);
        strcpy(newContact.number, number);
        strcpy(newContact.address, address);

    /*
            Invoca a função remota
    */
    result = delete_1 (&newContact, clnt);
    if (result == NULL)
    {
        printf ("Problemas ao chamar a função remota\n");
        exit (1);
    }
}


int main(int argc, char* argv[])
{
    /*
        Código responsável pela configuração e execução do cliente conectando-se ao servidor
    */
    CLIENT *clnt;

    if (argc != 2)
    {
        fprintf(stderr,"Usage: %s hostname\n", argv[0]);
        exit(1);
    }

    clnt = clnt_create (argv[1], NOTEBOOK_PROG, NOTEBOOK_VERSION, "udp");

    if(clnt == (CLIENT *) NULL)
    {
        clnt_pcreateerror(argv[1]);
        exit(1);
    }

    /*
        Implementação do menu da agenda de contatos
    */

    char name[500];
    char number[500];
    char address[500]; 

    char choice = 0;

    do{

        printf("\n\n\n[INFO] Agenda de Contatos\n");
        printf("[INFO] 1 - Adicionar Novo Contato;\n");
        printf("[INFO] 2 - Ler Contato Pelo Nome;\n");
        printf("[INFO] 3 - Alterar Contato Pelo Nome;\n");
        printf("[INFO] 4 - Remover Contato Pelo Nome;\n");
        printf("[INFO] 0 - Sair do Programa;\n");

        choice = getc(stdin);

        switch (choice)
        {
        case '1':
    
            printf("\n\n\n[INFO] Adicionando Novo Contato:\n");
            printf("[INFO] Nome:\n");
            scanf(" %[^\n]s", name);
            printf("[INFO] Número:\n");
            scanf(" %[^\n]s", number);
            printf("[INFO] Endereço:\n");
            scanf(" %[^\n]s", address);
            createContact(clnt, name, number, address);
            break;

        case '2':
    
            printf("\n\n\n[INFO] Lendo Informações Sobre Contato Existente:\n");
            printf("[INFO] Nome do Contato Existente:\n");
            scanf(" %[^\n]s", name);
            
            contact recentContact;
            recentContact = readContact(clnt, name, name, name);

            printf("[INFO] Informações do Contato Buscado:\n");
            printf("[INFO] Número: %s\n", recentContact.number);
            printf("[INFO] Endereço: %s\n", recentContact.address);
            
            break;

        case '3':
            printf("\n\n\n[INFO] Alterando Informações Sobre Contato Existente:\n");
            printf("[INFO] Nome Atual do Contato Existente:\n");
            scanf(" %[^\n]s", name);
            printf("[INFO] Novo Número:\n");
            scanf(" %[^\n]s", number);
            printf("[INFO] Novo Endereço:\n");
            scanf(" %[^\n]s", address);
            
            contact alteredContact;
            alteredContact = updateContact(clnt, name, number, address);
            break;

        case '4':
            printf("\n\n\n[INFO] Removendo Informações Sobre Contato Existente:\n");
            printf("[INFO] Nome do Contato Existente:\n");
            scanf(" %[^\n]s", name);
            
            contact deletedContact; 
            deletedContact = deleteContact(clnt, name, name, address);
            break;
        default:
            break;
        }

    }while(choice != '0');
   

}
