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

    // deleteRec() call
    void deleteKey(int key) { root = deleteRec(root, key); }

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
    void insert(int key) { root = insertRec(root, key); }

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

    public static void main(String[] args) {
        BinarySearchTree tree = new BinarySearchTree();

        tree.insert(50);
        tree.insert(30);
        tree.insert(20);
        tree.insert(40);
        tree.insert(70);
        tree.insert(60);
        tree.insert(80);

        System.out.println("Inorder traversal of the given tree");
        tree.inorder();
        tree.root = null;
        System.out.println("\nEnd");
        
    }
}
