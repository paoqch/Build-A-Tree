/**
 * Clase para el challege arbol Splay
 */
public class ChallegeSplayClass {
    SplayTree J1 = new SplayTree();
    SplayTree J2 = new SplayTree();
    Integer count1 = 0;
    Integer count2 = 0;

    /**
     * Metodo para llevar los arboles de cada jugar a tiempo real con todas sus operaciones
     *
     * @param jugador jugador al que le pertenece el arbol
     * @param valor   Numero que desea insertar al arbol
     */
    public void ChallegeSplay(int jugador, int valor) {
        switch (jugador) {
            case 1:
                if (count1 == 7) {
                    J1.root = null;
                    System.out.println("#######  WIN  #######");

                } else {
                    if (valor == 0) {
                        J1.root = null;
                        count1 = 0;
                    } else {

                        J1.insert(J1.root, valor);
                        System.out.println("Arbol J1");
                        System.out.println("\n");
                        J1.prettyPrint();
                        System.out.println("\n");
                        J1.inorder();
                        System.out.println("\n");
                        count1++;
                    }

                }
                break;

            case 2:
                if (count2 == 7) {
                    J2.root = null;
                    System.out.println("#######  WIN  #######");

                } else {
                    if (valor == 0) {
                        J2.root = null;
                        count2 = 0;
                    } else {

                        J2.insert(J2.root, valor);
                        System.out.println("Arbol J2");
                        System.out.println("\n");
                        J2.prettyPrint();
                        System.out.println("\n");
                        J2.inorder();
                        System.out.println("\n");
                        count2++;
                    }
                }
                break;
        }

    }
}
