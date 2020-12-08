public class Tokens {
    /**
     *
     * @param cantidad
     *            Cantidad de tokens necesarios.
     * @return un arreglo de String con los tokes y su figura.
     */
    public static String[] GenerarTokensAleatorios(int cantidad) {
        String[] TokenAleatoriaJ1 = new String[cantidad];

        String[] TokensJ1 = {"circulo","triangulo","cuadrado", "rombo"};

        for (int i = 0; i < cantidad; i++) {
            TokenAleatoriaJ1[i] = TokensJ1[(int) (Math.floor(Math.random() * ((TokensJ1.length - 1) - 0 + 1) + 0))];
        }
        return TokenAleatoriaJ1  ;
    }

}
