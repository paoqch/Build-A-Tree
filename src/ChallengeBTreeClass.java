/**
 * Clase para el challege arbol Binary Search Tree
 */
public class ChallengeBTreeClass {
    BTree J1 = new BTree();
    BTree  J2 = new BTree();
    Integer count1 = 0;
    Integer count2 = 0;

    /**
     * Metodo para llevar los arboles de cada jugar a tiempo real con todas sus operaciones
     *
     * @param jugador jugador al que le pertenece el arbol
     * @param valor   Numero que desea insertar al arbol
     */
    public void ChallengeBTree(int jugador, int valor) {
        switch (jugador) {
            case 1:
                if (count1 == 6) {
                    J1.root = null;
                    System.out.println("#######  WIN  #######");

                } else {
                    if (valor == 0) {
                        J1.root = null;
                        count1 = 0;
                    } else {

                        J1.add(valor);
                        System.out.println("Arbol J1");
                        System.out.println("\n");
                        J1.display(J1.root,3);
                        //J1.prettyPrint();
                        //System.out.println("\n");
                        //J1.inorder();
                        //System.out.println("\n");
                        count1++;
                    }

                }
                break;

            case 2:
                if (count2 == 6) {
                    J2.root = null;
                    System.out.println("#######  WIN  #######");

                } else {
                    if (valor == 0) {
                        J2.root = null;
                        count2 = 0;
                    } else {

                        J2.add(valor);
                        System.out.println("Arbol J2");
                        System.out.println("\n");
                        J2.display(J2.root,3);
                        //System.out.println("\n");

                        count2++;
                    }
                }
                break;
        }

    }
}