/**
 * Clase del Arbol AVL
 */
public class AVLTree {

    //Define the root
    AVLNode root;

    //Height of a node

    /**
     * Metodo para saber la altura de un nodo
     * @param node arbol a averiguar
     * @return la altura del nodo
     */
    int height(AVLNode node){
        if (node==null){
            return 0;
        }
        return node.height;
    }

    //Get balance of a node

    /**
     * Metodo para balancear el arbol al insertar una nodo
     * @param node arbol para balancear
     * @return diferencia entre las alturas del nodo izquierdo y el derecho
     */
    int getBalance(AVLNode node){
        if (node == null)
            return 0;
        return height(node.left) - height(node.right);
    }

    /**
     * Metodo para determinar el valor maximo
     * @param a valor
     * @param b valor
     * @return el nodo maximo
     */
    int max (int a, int b)
    {
        return Math.max(a, b);
    }

    /**
     * Metodo para rotar a la derecha de los nodos
     * @param y nodos involucrados
     * @return nodos rotados
     */
    AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;

        x.right = y;
        y.left = T2;

        y.height = max(height(y.left), height(y.right)) + 1;
        x.height = max(height(x.left), height(x.right)) + 1;

        return x;
    }

    /**
     * Metodo para rotar a la izquierda de los nodos
     * @param x nodos involucrados
     * @return nodos rotados
     */
    AVLNode leftRotate (AVLNode x){
        AVLNode y  = x.right;
        AVLNode T2 = y.left;

        y.left = x;
        x.right = T2;

        x.height = max(height(x.left), height(x.right)) + 1;
        y.height = max(height(y.left), height(y.right)) + 1;

        return y ;
    }

    /**
     * Metodo para insertar un valor al árbol
     * @param node arbol al que se le agregar
     * @param key valor
     * @return return el arbol
     */
    AVLNode insert(AVLNode node,int key ) {
        if (node == null) {
            return new AVLNode(key);
        }
        if (key < node.key)
            node.left = insert(node.left, key);
        else if (key > node.key)
            node.right = insert(node.right, key);
        else
            return node;

        node.height = 1 + max(height(node.left), height(node.right));

        int balance = getBalance(node);

        //Left left
        if (balance > 1 && key < node.left.key)
            return rightRotate(node);

        //Right right
        if (balance < -1 && key > node.right.key)
            return leftRotate(node);

        //Left right
        if (balance > 1 && key >node.left.key){
            node.left = leftRotate(node.left);
            return rightRotate(node);

        }
        //Right left
        if (balance < -1 && key < node.right.key)
        {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }
        return node;
    }

    /**
     * Metodo imprimir el recorrido inorden
     */
    public void inOrder() { inorderRec(root); }

    /**
     * Metodo auxiliar para recorrer el arbol inorden
     * @param root raíz del node
     */
    public void inorderRec(AVLNode root)
    {
        if (root != null) {
            inorderRec(root.left);
            System.out.print(root.key + " ");
            inorderRec(root.right);
        }
    }

    /**
     * Metodo para imprimir el arbol
     * @param currPtr arbol
     * @param indent indentacion
     * @param last saber si el ultimo
     */
    private void printHelper(AVLNode currPtr, String indent, boolean last) {
        // print the tree structure on the screen
        if (currPtr != null) {
            System.out.print(indent);
            if (last) {
                System.out.print("R----");
                indent += "     ";
            } else {
                System.out.print("L----");
                indent += "|    ";
            }

            System.out.println(currPtr.key);

            printHelper(currPtr.left, indent, false);
            printHelper(currPtr.right, indent, true);
        }
    }

    /**
     * Metodo para llamar el metodo printHelper
     */
    public void prettyPrint() {
        printHelper(root, "", true);
    }
}
