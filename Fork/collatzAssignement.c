#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

/*
Rafael Furlanetto Casamaximo
This code is an assignement of 5COP010 - Sistemas Operacionais
Fork Implementation
Universidade Estadual de Londrina

gcc collatzAssignement.c -o collatzAssignement

Run with:
./collatzAssignement [number]
*/

//Calcula a Conjectura de Collatz de um número de forma simples. Imprime os valores enquanto calcula.
void collatzConjecture(int x){
    while(x != 1){
        if(x % 2 == 0){
            printf("\nValor: %d", x);
            x /= 2;
            continue;
        }
        if(x % 2 == 1){
            printf("\nValor: %d", x);
            x = (3 * x) + 1;
            continue;
        }
    }
    printf("\nValor: %d\n", x);
}

int main(int argc, char *argv[]){
    pid_t cpid;
    cpid = fork();
    if( cpid == -1 ){
		printf("Falha no fork!");
		return 1;
	}
    if(cpid == 0){
        //Implementação da Conjectura de Collatz
        int valor = atoi(argv[1]);
        if(valor > 0){
            collatzConjecture(valor);
            printf("Encerrando o processo filho.\n");
            return 0;
        }
        printf("O número precisa ser maior que 0!");
        return 1;
    }
    if(cpid > 0){
        //Implementação do codigo pai
        //Espera pela execução do processo filho
        wait(NULL);
        printf("Encerrando o processo pai.\n");
    }
    return 0;
}