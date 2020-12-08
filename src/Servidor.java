import java.io.*;
import java.net.*;

public class Servidor {
    ChallegeAVLClass Ch1= new ChallegeAVLClass();
    ChallegeSplayClass Ch3= new ChallegeSplayClass();
    Tokens tokens = new Tokens();
    String[] TokensGenerados = tokens.GenerarTokensAleatorios(16);
    static final int PUERTO=5555;

    public Servidor(){
        try{
            System.out.println("Inicializando Servidor");
            //Creo un socket que escucha solicitudes
            ServerSocket socketServidor = new ServerSocket(PUERTO);

            System.out.println("Conectado al puerto: "+PUERTO);
            System.out.println("Esperando cliente(s)");

            for (int numCliente = 0; numCliente<1000;numCliente++){
                //Creo un nuevo socket que getiona la conexion
                Socket socketCliente = socketServidor.accept();

                System.out.println("Atendiendo a cliente "+numCliente+" en el puerto: "+PUERTO);
                //Flujo de salida
                OutputStream mensajeParaCliente = socketCliente.getOutputStream();
                DataOutputStream flujo = new DataOutputStream(mensajeParaCliente);
                //Formato string
                String[] available_cards = {"BST", "B", "AVL", "Splay"};
                java.util.Random random = new java.util.Random();
                int random_Tree_Order = random.nextInt(available_cards.length);
                int random_Tree_Order2 = random.nextInt(available_cards.length);
                int random_Tree_Order3 = random.nextInt(available_cards.length);
                System.out.println(available_cards[random_Tree_Order]+","+available_cards[random_Tree_Order2]+","+available_cards[random_Tree_Order3]);

                flujo.writeUTF("|"+available_cards[random_Tree_Order]+","+available_cards[random_Tree_Order2]+","+available_cards[random_Tree_Order3]);
                //flujo.writeUTF( "|" + TokensGenerados);

                InputStreamReader in = new InputStreamReader(socketCliente.getInputStream());
                BufferedReader bf = new BufferedReader(in);

                String str = bf.readLine();
                System.out.println("client: "+ str);
                int cont = 0;
                String [] msg = str.split("/");
                String tree = msg[0];

                Integer jugador = Integer.parseInt(msg[1]);
                Integer valor = Integer.parseInt(msg[2]) ;
                System.out.println(msg);


                if (tree == "AVL");{
                    Ch1.ChallegeAVL(jugador,valor);
                    cont+=1;
                    System.out.println("funciona");
                    System.out.println(cont);
                }
                if (tree == "Splay");{
                    cont+=2;
                    Ch3.ChallegeSplay(jugador,valor);
                    System.out.println("funciona");
                    System.out.println(cont);
                }

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
