public class Tokens {
    /**
     *
     * @param cantidad
     *            Cantidad de tokens necesarios.
     * @return un arreglo de String con los tokes y su figura.
     */
    public static Integer[] GenerarTokensAleatorios(int cantidad) {
        Integer[] TokenAleatoriaJ1 = new Integer[cantidad];

        Integer[] TokensJ1 = { 9,5,7,3,12,10,17,18,28,25,23,20,30,34,36,39,45,42,44,41,51,56,58,54,63,61,65,
                67,74,77,70,72,86,83,81,85,97,99,92,96};

        for (int i = 0; i < cantidad; i++) {
            TokenAleatoriaJ1[i] = TokensJ1[(int) (Math.floor(Math.random() * ((TokensJ1.length - 1) - 0 + 1) + 0))];
        }
        return TokenAleatoriaJ1  ;
    }
    public static void  main(String[] args)
    {
        Integer[] TokensGeneradosJ1 = GenerarTokensAleatorios(16);
        for (int i = 0; i < TokensGeneradosJ1.length; i++) {

            Integer Token = TokensGeneradosJ1[i];
            System.out.println(Token);

        }
    }
}
