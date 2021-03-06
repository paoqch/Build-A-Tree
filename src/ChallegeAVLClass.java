/**
 * Clase para el challege AVL
 */
public class ChallegeAVLClass {

    AVLTree J1 = new AVLTree();
    AVLTree J2 = new AVLTree();
    Integer count1 = 0;
    Integer count2 = 0;

    /**
     * Metodo para llevar los arboles de cada jugar a tiempo real con todas sus operaciones
     * @param jugador  jugador al que le pertenece el arbol
     * @param valor Numero que desea insertar al arbol
     */
    public void ChallegeAVL( int jugador,int valor){
        switch (jugador){
            case 1:
                if (count1==5){
                    J1.root = null;
                    System.out.println("#######  WIN  #######");

                }else{
                    if(valor ==0){
                        J1.root = null;
                        count1 =0;
                    }else{

                        J1.root = J1.insert(J1.root,valor);
                        System.out.println("Arbol J1");
                        System.out.println("\n");
                        J1.prettyPrint();
                        System.out.println("\n");
                        J1.inOrder();
                        System.out.println("\n");
                        count1++;
                    }

                }
                break;

            case 2:
                if (count2==5){
                    J2.root = null;
                    System.out.println("#######  WIN  #######");

                }else{
                    if(valor ==0){
                        J2.root = null;
                        count2 =0;
                    }else{

                        J2.root = J2.insert(J2.root,valor);
                        System.out.println("Arbol J2");
                        System.out.println("\n");
                        J2.prettyPrint();
                        System.out.println("\n");
                        J2.inOrder();
                        System.out.println("\n");
                        count2++;
                    }
                }
                break;
        }

    }

}