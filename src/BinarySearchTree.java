public class BinarySearchTree {
    // Class containing left and right child
    class Node {
        int key;
        Node left, right;

        public Node(int item) {
            key = item;
            left = right = null;
        }
    }
    // Root of BST
    Node root;

    // Constructor
    BinarySearchTree() {

        root = null;
    }
    //Print tree method
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

            System.out.println(currPtr.key);

            printHelper(currPtr.left, indent, false);
            printHelper(currPtr.right, indent, true);
        }
    }

    // deleteRec() call
    void deleteKey(int key) {
        root = deleteRec(root, key);
    }

    //Delete an existing key in BST
    Node deleteRec(Node root, int key) {
        //If the tree is empty
        if (root == null)
            return root;

        if (key < root.key)
            root.left = deleteRec(root.left, key);
        else if (key > root.key)
            root.right = deleteRec(root.right, key);


        else {
            // node with only one child or no child
            if (root.left == null)
                return root.right;
            else if (root.right == null)
                return root.left;

            // Get the inorder
            root.key = minValue(root.right);

            // Delete the inorder successor
            root.right = deleteRec(root.right, root.key);
        }

        return root;
    }

    int minValue(Node root) {
        int minv = root.key;
        while (root.left != null) {
            minv = root.left.key;
            root = root.left;
        }
        return minv;
    }

    // insertRec() call
    Node insert(Node root, int key) {
        this.root = insertRec(this.root, key);
        return null;
    }

    //Insert a new key in BST
    Node insertRec(Node root, int key)
    {

        //If the tree is empty, return a new node
        if (root == null) {
            root = new Node(key);
            return root;
        }

        if (key < root.key)
            root.left = insertRec(root.left, key);
        else if (key > root.key)
            root.right = insertRec(root.right, key);

        return root;
    }

    // InorderRec() call
    void inorder() { inorderRec(root); }

    // Inorder traversal of BST
    void inorderRec(Node root)
    {
        if (root != null) {
            inorderRec(root.left);
            System.out.print(root.key + " ");
            inorderRec(root.right);
        }
    }
    //printHelper method call
    public void prettyPrint() {
        printHelper(this.root, "", true);
    }
}

