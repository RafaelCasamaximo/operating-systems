#include <stdio.h>
#include <string.h>
#include "notebook.h"

contact notebook[1000];
int currentNotebook = 0;


/*
    Implementação da Interface de comunicação RPC do servidor
*/
contact *create_1_svc(contact *argp, struct svc_req *rqstp)
{

    static contact result;

    printf("[INFO] Criando novo contato.\n[INFO] Nome: %s\n[INFO] Número: %s\n[INFO] Endereço: %s\n\n", argp->name, argp->number, argp->address);
    strcpy(result.name, argp->name);
    strcpy(result.number, argp->number);
    strcpy(result.address, argp->address);

    if(currentNotebook < 500)
    {
        notebook[currentNotebook] = result;
        currentNotebook++;
    }
    return (&result);
}

contact *read_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    printf("[INFO] Lendo contato.\n[INFO] Nome: %s\n", argp->name);

    for(int i = 0; i < currentNotebook; i++)
    {
        if(strcmp(argp->name, notebook[i].name) == 0)
        {
            strcpy(result.name, notebook[i].name);
            strcpy(result.number, notebook[i].number);
            strcpy(result.address, notebook[i].address);
        }
    }

    return (&result);
}

contact *update_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    printf("[INFO] Alterando contato.\n[INFO] Nome: %s\n[INFO] Novo Número: %s\n[INFO] Novo Endereço: %s\n", argp->name, argp->number, argp->address);

    for(int i = 0; i < currentNotebook; i++)
    {
        if(strcmp(argp->name, notebook[i].name) == 0)
        {
            strcpy(notebook[i].number, argp->number);
            strcpy(notebook[i].address, argp->address);
        }
    }

    return (&result);
}

contact *delete_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    printf("[INFO] Removendo Contato.\n[INFO] Nome: %s\n", argp->name);

    for(int i = 0; i < currentNotebook; i++)
    {
        if(strcmp(argp->name, notebook[i].name) == 0)
        {
            char aux[500] = "NA";
            strcpy(notebook[i].name, aux);
            strcpy(notebook[i].number, aux);
            strcpy(notebook[i].address, aux);
            strcpy(result.name, aux);
            strcpy(result.number, aux);
            strcpy(result.address, aux);
        }
    }

    return (&result);
}





