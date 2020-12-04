public class AVLNode {
    int key, height;
    AVLNode left, right;

    public AVLNode(int item){
        this.key = item;
        left = right= null;
        height = 1;
    }


}
