#define PROGRAM_NUMBER 12345678
#define VERSION_NUMBER 1

struct contact
{
    char name[500];
    char number[500];
    char address[500];
};

program NOTEBOOK_PROG
{
    version NOTEBOOK_VERSION
    {
        struct contact create(contact) = 1;
        struct contact read(contact) = 2;
        struct contact update(contact) = 3;
        struct contact delete(contact) = 4;
    } = VERSION_NUMBER;
} = PROGRAM_NUMBER;