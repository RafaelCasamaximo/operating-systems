// TicketClient.java

import java.rmi.*;

public class TicketClient {
  public static void main(String [] args) {
    // install RMI security manager
    System.setSecurityManager(new RMISecurityManager());

    // arg. 0 = name of server
    if (args.length!=1) {
      System.err.println("Usage: TicketClient <server-rmi-url>");
      System.exit(-1);
    }

    // look up in nameserver
    String fullname = args[0];
    TicketServer server = null;    
    try {
      server = (TicketServer)Naming.lookup(fullname);
    } catch (Exception e) {
      System.out.println("Caught an exception doing name lookup on "+fullname
			 +": "+e);
      System.exit(-1);
    }

    // get ticket - remote method invocation!
    try {
      int ticket = server.getNextTicket("TicketClient");
      System.out.println("Got ticket " + ticket);
    } catch (Exception e) {
      System.out.println("Exception caught while getting ticket: "+e);
      System.exit(-1);
    }
  }
}

