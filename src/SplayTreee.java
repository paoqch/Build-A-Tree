public class SplayTreee {
    static SplayNode newNode(int key)
    {
        SplayNode node = new SplayNode();
        node.key = key;
        node.left = node.right = null;
        return node;
    }

    static SplayNode rightRotate(SplayNode x){
        SplayNode y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    static SplayNode leftRotate(SplayNode x){
        SplayNode y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    static SplayNode search(SplayNode root,int key){
        return splay(root,key);
    }

    static SplayNode splay(SplayNode root, int key){
        if (root==null || root.key==key)
            return root;
        if (root.key>key){
            if (root.left==null)
                return root;
            //Zig-zig
            if (root.left.key>key){
                root.left.left = splay(root.left.left,key);
                root = rightRotate(root);

            }
            //Zig-zag
            else if (root.left.key<key){
                root.left.right = splay(root.left.right,key);
                if (root.left.right!=null){
                    root.left= leftRotate(root.left);
                }
            }

            return (root.left==null) ? root:rightRotate(root);
        } else {
            if (root.right==null)
                return root;
            //Right-left
            if (root.right.key > key){
                root.right.left = splay(root.right.left,key);

                if (root.right.left!=null)
                    root.right = rightRotate(root.right);
                //Right-right
            } else if (root.right.key < key){
                root.right.right = splay(root.right.right,key);
                root = leftRotate(root);
            }
            return (root.right==null)? root:leftRotate(root);
        }
    }
    static void preOrder(SplayNode root)
    {
        if (root != null)
        {
            System.out.print(root.key + " ");
            preOrder(root.left);
            preOrder(root.right);
        }
    }
    public static void main(String ars[]){
        SplayNode root = newNode(100);
        root.left = newNode(50);
        root.right = newNode(200);
        root.left.left = newNode(40);
        root.left.left.left = newNode(30);
        root.left.left.left.left = newNode(20);

        root = search(root, 20);
        System.out.println("Inordel traversal of the" +
                " modified Splay tree is \n");
        preOrder(root);
    }
}
