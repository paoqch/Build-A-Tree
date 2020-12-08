/**
 * Clase Nodo del Arbol Splay
 */
class Node {
    int data; // holds the key
    Node parent; // pointer to the parent
    Node left; // pointer to left child
    Node right; // pointer to right child

    public Node(int data) {
        this.data = data;
        this.parent = null;
        this.left = null;
        this.right = null;

    }
}

/**
 * Clase del Arbol Splay
 */
public class SplayTree {
    public Node root;

    /**
     * Metodo de verificacion de que el arbol este vacio
     */
    public SplayTree() {
        root = null;
    }

    /**
     * Metodo de impresion del arbol
     * @param currPtr nodo que se va imprimir
     * @param indent variable para la identación
     * @param last para saber si es el ultimo
     */
    private void printHelper(Node currPtr, String indent, boolean last) {
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

            System.out.println(currPtr.data);

            printHelper(currPtr.left, indent, false);
            printHelper(currPtr.right, indent, true);
        }
    }


    /**
     * Metodo de Rotacion hacia la izquierda
     * @param x nodo a rotar
     */
    private void leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        if (y.left != null) {
            y.left.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == null) {
            this.root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    /**
     * Metodo de Rotacion hacia la derecha
     * @param x nodo a rotar
     */

    private void rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        if (y.right != null) {
            y.right.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == null) {
            this.root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }

    /**
     * Metodo de la operacion splaying
     * @param x nodo que se debe acomodar
     */
    private void splay(Node x) {
        while (x.parent != null) {
            if (x.parent.parent == null) {
                if (x == x.parent.left) {
                    // zig rotation
                    rightRotate(x.parent);
                } else {
                    // zag rotation
                    leftRotate(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // zig-zig rotation
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // zag-zag rotation
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // zig-zag rotation
                leftRotate(x.parent);
                rightRotate(x.parent);
            } else {
                // zag-zig rotation
                rightRotate(x.parent);
                leftRotate(x.parent);
            }
        }
    }

    /**
     * Metodo para unir 2 arboles
     * @param s primer arbol
     * @param t segundo arbol
     * @return
     */
    private Node join(Node s, Node t){
        if (s == null) {
            return t;
        }

        if (t == null) {
            return s;
        }
        Node x = maximum(s);
        splay(x);
        x.right = t;
        t.parent = x;
        return x;
    }


    /**
     * Metodo auxiliar que se realiza el recorrido en Inorden para imprimirlo
     * @param node arbol a recorrer
     */
    private void inOrderHelper(Node node) {
        if (node != null) {
            inOrderHelper(node.left);
            System.out.print(node.data + " ");
            inOrderHelper(node.right);
        }
    }

    // In-Order traversal
    // Left Subtree -> Node -> Right Subtree

    /**
     * Metodo que llama al metodo auxiliar del recorrido
     */
    public void inorder() {
        inOrderHelper(this.root);
    }


    /**
     * Metodo para encontrar el nodo maximo
     * @param node arbol
     * @return nodo maximo
     */
    public Node maximum(Node node) {
        while (node.right != null) {
            node = node.right;
        }
        return node;
    }

    // insert the key to the tree in its appropriate position

    /**
     * Metodo de insercion de  la llave en el árbol en su posición apropiada
     * @param root raiz
     * @param key llave a insertar
     */
    public void insert(Node root, int key) {
        Node node = new Node(key);
        Node y = null;
        Node x = this.root;

        while (x != null) {
            y = x;
            if (node.data < x.data) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        // y is parent of x
        node.parent = y;
        if (y == null) {
            this.root = node;
        } else if (node.data < y.data) {
            y.left = node;
        } else {
            y.right = node;
        }

        // splay node
        splay(node);
    }



    /**
     * Metodo para llamar el metodo printHelper
     */
    public void prettyPrint() {
        printHelper(this.root, "", true);
    }


}
