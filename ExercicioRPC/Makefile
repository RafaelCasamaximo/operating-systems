output: notebook_svc.o notebook_xdr.o server.o 
	gcc notebook_svc.o notebook_xdr.o server.o -o server -lnsl
	gcc client.c notebook_clnt.c notebook_xdr.c -o client -lnsl
	rm -rf *.o notebook.txt

notebook_svc.o: notebook_svc.c
	gcc -c notebook_svc.c

notebook_xdr.o: notebook_xdr.c
	gcc -c notebook_xdr.c

server.o: server.c
	gcc -c server.c

clean:
	rm -rf *.o notebook.txt