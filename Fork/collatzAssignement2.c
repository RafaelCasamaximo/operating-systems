#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <math.h>

/*
Rafael Furlanetto Casamaximo
This code is an assignement of 5COP010 - Sistemas Operacionais
Fork and POSIX Shared Memory Implementation
Universidade Estadual de Londrina

This code MUST be compiled with the following flags:
-lrt #Due to POSIX Shared Memory System Calls;
-lm #Due to math.h include for the helper funcion;

gcc collatzAssignement2.c -o collatzAssignement2 -lrt -lm

Run with:
./collatzAssignement2 [number]
*/


//Função helper para calcular quantos algarismos tem um número
//Calcula o valor absoluto do número, após isso calcula o log10 do número (número de algarismos), e depois arredonda o valor para baixo.
int digitHelper(int x){
    return (int)floor(log10(abs(x)));
}

//Calcula a Conjectura de Collatz de um número de forma simples.
void collatzConjecture(int x, void* ptr){
    while(x != 1){
        if(x % 2 == 0){
            sprintf(ptr, "%d ", x);
            ptr += digitHelper(x) + 2;
            x /= 2;
            continue;
        }
        if(x % 2 == 1){
            sprintf(ptr, "%d ", x);
            ptr += digitHelper(x) + 2;
            x = (3 * x) + 1;
            continue;
        }
    }
    sprintf(ptr, "%d ", x);
    ptr += digitHelper(x) + 2;
}

int main(int argc, char *argv[]){

    //Variáveis utilizadas para fazer o Memory Sharing
    //Não haveria necessidade de criar uma variável para o SIZE ou para o name. Poderia inserir os valores direto na função.
    const char* name = "Collatz";
    int shm_fd;
    void *ptr;
    const int SIZE = 4096 * 50;
    void *originalPtr = ptr;

    //Inicia a memória compartilhada no proceso original
    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    ftruncate(shm_fd, SIZE);
    ptr = mmap(0, SIZE, PROT_READ, MAP_SHARED, shm_fd, 0);

    pid_t cpid;
    cpid = fork();
    if( cpid == -1 ){
		printf("Falha no fork!");
		return 1;
	}
    if(cpid == 0){
        //Abre a memória compartilhada no processo filho
        shm_fd = shm_open(name, O_RDWR, 0666);
        ptr = mmap(0, SIZE, PROT_WRITE, MAP_SHARED, shm_fd, 0);
        //Implementação da Conjectura de Collatz
        int valor = atoi(argv[1]);
        if(valor > 0){
            collatzConjecture(valor, ptr);
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
        printf("Conjectura de Collatz do número inserido usando POSIX Shared Memory:\n%s\n", (char*) ptr);
        printf("Encerrando o processo pai.\n");
        //Retira o link da POSIX Shared Memory
        shm_unlink(name);
    }
    return 0;
}