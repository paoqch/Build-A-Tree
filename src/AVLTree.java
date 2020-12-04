public class AVLTree {

    //Define the root
    AVLNode root;

    //Height of a node
    int height(AVLNode node){
        if (node==null){
            return 0;
        }
        return node.height;
    }

    //Get balance of a node
    int getBalance(AVLNode node){
        if (node == null)
            return 0;
        return height(node.left) - height(node.right);
    }
    int max (int a, int b)
    {
        return Math.max(a, b);
    }

    AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;

        x.right = y;
        y.left = T2;

        y.height = max(height(y.left), height(y.right)) + 1;
        x.height = max(height(x.left), height(x.right)) + 1;

        return x;

    }
    AVLNode leftRotate (AVLNode x){
        AVLNode y  = x.right;
        AVLNode T2 = y.left;

        y.left = x;
        x.right = T2;

        x.height = max(height(x.left), height(x.right)) + 1;
        y.height = max(height(y.left), height(y.right)) + 1;

        return y ;
    }

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
    public void inOrden (AVLNode root){
        if (root != null){
            inOrden(root.left);
            System.out.println(root.key);
            inOrden(root.right);
        }
    }

    public static void  main(String[] args)
    {
        AVLTree tree = new AVLTree();

        tree.root = tree.insert(tree.root,10);
        tree.root = tree.insert(tree.root,20);
        tree.root = tree.insert(tree.root,30);
        tree.root = tree.insert(tree.root,40);
        tree.root = tree.insert(tree.root,50);
        tree.root = tree.insert(tree.root,25);

        tree.inOrden(tree.root);
        tree.root = null;
        System.out.println("Fin");



    }
}
