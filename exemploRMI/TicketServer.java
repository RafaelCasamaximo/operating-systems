// TicketServer.java

import java.rmi.*;

public interface TicketServer extends Remote 
{
  public int getNextTicket(String name) throws RemoteException;
}

