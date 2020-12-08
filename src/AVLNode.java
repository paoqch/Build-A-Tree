/**
 * Clase Nodo del Arbol AVL
 */
public class AVLNode {
    int key, height;
    AVLNode left, right;

    /**
     * Metodo para saber que tipo de nodo se ingresará
     * @param item número a ingresar
     */
    public AVLNode(int item){
        this.key = item;
        left = right= null;
        height = 1;
    }


}
