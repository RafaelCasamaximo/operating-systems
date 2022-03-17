// TicketServerImpl.java
import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;
public class TicketServerImpl extends UnicastRemoteObject 
          implements TicketServer 
{
  int nextTicket=0;
  TicketServerImpl() throws RemoteException { };
  public int getNextTicket(String name) throws RemoteException {
    System.out.println("Issue a new ticket for " + name);
    return nextTicket++;
  }
  public static void main(String [] args) {
    // install RMI security manager
    System.setSecurityManager(new RMISecurityManager());
    // arg. 0 = rmi url
    if (args.length!=1) {
      System.err.println("Usage: TicketServerImpl <server-rmi-url>");
      System.exit(-1);
    }
    try {  
      // name with which we can find it = user name
      String name = args[0];
      //create new instance
      TicketServerImpl server = new TicketServerImpl();
      // register with nameserver
      Naming.rebind(name, server);
      System.out.println("Started TicketServer, registered as " + name);
    }
    catch(Exception e) {
      System.out.println("Caught exception while registering: " + e);
      System.exit(-1);
    }
  }
}
