import java.io.*;
import java.net.*;

public class Servidor {

    static final int PUERTO=5555;
    public Servidor(){
        try{
            System.out.println("Inicializando Servidor");
            //Creo un socket que escucha solicitudes
            ServerSocket socketServidor = new ServerSocket(PUERTO);

            System.out.println("Conectado al puerto: "+PUERTO);
            System.out.println("Esperando cliente(s)");

            for (int numCliente = 0; numCliente<4;numCliente++){
                //Creo un nuevo socket que getiona la conexion
                Socket socketCliente = socketServidor.accept();

                System.out.println("Atendiendo a cliente "+numCliente+" en el puerto: "+PUERTO);
                //Flujo de salida
                OutputStream mensajeParaCliente = socketCliente.getOutputStream();
                DataOutputStream flujo = new DataOutputStream(mensajeParaCliente);
                //Formato string
                flujo.writeUTF("Bienvenido cliente "+numCliente+ ", el puerto de escucha es el "+PUERTO+" y el puerto de comunicacion bidireccional es el "+socketCliente.getPort());

                socketCliente.close();
            }
            System.out.println("Demasiados clientes");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void main ( String[] args){
        Servidor miServidor = new Servidor();
    }
}
