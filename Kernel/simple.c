#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/types.h>
#include <linux/slab.h>

/*
Rafael Furlanetto Casamaximo
This code is an assignement of 5COP010 - Sistemas Operacionais
Simple Kernel Implementation
Universidade Estadual de Londrina
*/

/*
Defines the birthday struct with the list_head to use in a list.
*/
struct birthday{
       int day;
       int month;
       int year;
       struct list_head list;
};

/*
Declares a birthday_list variable
*/
static LIST_HEAD(birthday_list);

/* This function is called when the module is loaded. */
int simple_init(void)
{
       //Load module
       printk(KERN_INFO "Carregando Módulo\n");

       //Creates a birthday pointer
       struct birthday *person;

       //Allocates a new person with kmalloc
       int i = 0;
       for(i = 0; i < 5; i++){
              person = kmalloc(sizeof(*person), GFP_KERNEL);
              person->day = 1+i;
              person->month = 1+i;
              person->year = 2001+i;
              INIT_LIST_HEAD(&person->list);
              list_add_tail(&person->list, &birthday_list);
       }

       //Iterates over the linked list and print the values
       struct birthday *ptr;
       list_for_each_entry(ptr, &birthday_list, list){
              printk(KERN_INFO "Aniversário: %d/%d/%d", ptr->day, ptr->month, ptr->year);
       }

       return 0;
}

/* This function is called when the module is removed. */
void simple_exit(void) {
	printk(KERN_INFO "Removendo Módulo\n");

       //Iterates over the linked list end kfree() all the memory allocated.
       struct birthday *ptr, *next;
       list_for_each_entry_safe(ptr, next, &birthday_list, list){
              list_del(&ptr->list);
              kfree(ptr);
       }

}

/* Macros for registering module entry and exit points. */
module_init( simple_init );
module_exit( simple_exit );

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Simple Module");
MODULE_AUTHOR("SGG");

