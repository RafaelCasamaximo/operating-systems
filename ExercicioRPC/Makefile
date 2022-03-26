output: notebook_svc.o notebook_xdr.o server.o doublyLinkedList.o
	gcc notebook_svc.o notebook_xdr.o server.o doublyLinkedList.o -o server -lnsl
	gcc client.c notebook_clnt.c notebook_xdr.c -o client -lnsl
	rm -rf *.o

notebook_svc.o: notebook_svc.c
	gcc -c notebook_svc.c

notebook_xdr.o: notebook_xdr.c
	gcc -c notebook_xdr.c

doublyLinkedList.o: doublyLinkedList.c doublyLinkedList.h
	gcc -c doublyLinkedList.c

server.o: server.c
	gcc -c server.c


clean:
	rm -rf *.o