#include <stdio.h>
#include <string.h>
#include "doublyLinkedList.h"
#include "notebook.h"

void saveList(DoublyLinkedList lista)
{
    FILE* notebookFilePtr = fopen("notebook.bin", "wb");

    for(Node aux = getFirst(lista); aux != NULL; aux = getNext(aux))
    {
        Info info = getInfo(aux);
        fwrite(&info, sizeof(contact), 1, notebookFilePtr);
    }
    fclose(notebookFilePtr);
}

void loadList(DoublyLinkedList lista)
{
    FILE* notebookFilePtr = fopen("notebook.bin", "rb");
    if(notebookFilePtr == NULL)
    {
        return;
    }
    
    contact newContact;

    /* Attempt to read */
    // while (fread(&newContact, sizeof(struct contact), 1, notebookFilePtr) == sizeof(struct contact)) {
    //     insert(lista, newContact);
    // }

    fclose(notebookFilePtr);
}


/**
 * Implementação das funções definidas no notebook.h criadas pelo rpcgen
 * Funções básicas de CRUD
 * 
 * TODOs:
 * - Criação da lista de pessoas
 */

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

    DoublyLinkedList lista = createDoublyLinkedList();
    loadList(lista);
    /*
        TODO: Adicionar na lista
    */
    saveList(lista);
    removeList(lista, 0);
    return (&result);
}

contact *read_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    printf("[INFO] Lendo contato.\n");

    DoublyLinkedList lista = createDoublyLinkedList();
    loadList(lista);
    /*
        TODO: Adicionar na lista
    */
    saveList(lista);
    removeList(lista, 0);
    return (&result);
}

contact *update_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    printf("[INFO] Alterando contato.\n");

    DoublyLinkedList lista = createDoublyLinkedList();
    loadList(lista);
    /*
        TODO: Adicionar na lista
    */
    saveList(lista);
    removeList(lista, 0);
    return (&result);
}

contact *delete_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    printf("[INFO] Removendo contato.\n");

    DoublyLinkedList lista = createDoublyLinkedList();
    loadList(lista);
    /*
        TODO: Adicionar na lista
    */
    saveList(lista);
    removeList(lista, 0);
    return (&result);
}





