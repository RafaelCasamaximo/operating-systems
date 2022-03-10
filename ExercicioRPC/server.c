#include <stdio.h>
#include "notebook.h"

/**
 * Implementação das funções definidas no notebook.h criadas pelo rpcgen
 * Funções básicas de CRUD
 * 
 * TODOs:
 * - Criação da lista de pessoas
 */

struct contact *create_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    return (&result);
}

struct contact *read_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    return (&result);
}

struct contact *update_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    return (&result);
}

struct contact *delete_1_svc(contact *argp, struct svc_req *rqstp)
{
    static contact result;

    return (&result);
}
