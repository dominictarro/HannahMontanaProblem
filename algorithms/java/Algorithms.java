/*
 * Optimized code for calculating the likelihood of an exclusive relationship.
 * Read the whole project at https://tarro.work/code/the-hannah-montana-problem
 * 
 */
package algorithms.java;
import java.math.BigInteger;
import java.math.BigDecimal;
import java.math.MathContext;
import java.util.Arrays;


class Algorithms {

    private Algorithms(){}

    /**
     * Counts the number of ways of choosing `r` unordered outcomes from `n` possibilities.
     * 
     * @param n Population size
     * @param r Sample size
     * @return Number of combinations of size `r` from population of size `n`
     */
    static BigInteger comb(final int n, final int r) {
        BigInteger ret = BigInteger.ONE;
        for (int x = 0; x < r; x++) {
            ret = ret.multiply(BigInteger.valueOf(n - x))
                     .divide(BigInteger.valueOf(x + 1));
        }
        return ret;
    }
 
    /**
     * The probability that no samples of sizes `A` share a value from a population of size `N`.
     * 
     * Is not optimized in any way.
     * 
     * @param A Sample sizes
     * @param N Population size
     * @return Likelihood of an exclusive relationship
     */
    public static double likelihoodOfAnExclusiveRelationshipNotOptimized(final Integer[] A, final Integer N) {
        double p = 1.0d;

        int j;
        Integer sumToCurrent;
        BigInteger numer;
        BigInteger denom;
        // Set precision to 15
        MathContext mc = new MathContext(15);

        for (int i = 0; i < A.length; i++) {
            // Take sum of values up to a_i
            sumToCurrent = 0;
            for (j = 0; j < i; j++) {
                sumToCurrent += A[j];
            }
            // Calculate 
            numer = comb(N - sumToCurrent, A[i]);
            denom = comb(N, A[i]);
            p *= new BigDecimal(numer)
                .divide(new BigDecimal(denom), mc)
                .doubleValue();
            }

        return 1.0d - p;
    }

    /**
     * The probability that no samples of sizes `A` share a value from a population of size `N`.
     * 
     * Uses an optimized formula.
     * 
     * @param A Sample sizes
     * @param N Population size
     * @return Likelihood of an exclusive relationship
     */
    public static double likelihoodOfAnExclusiveRelationshipAlgebraicallyOptimized(final Integer[] A, final Integer N) {
        int sum = 0;
        double p;

        BigInteger numer = BigInteger.ONE;
        BigInteger denom = BigInteger.ONE;
        // Set precision to 15
        MathContext mc = new MathContext(15);

        for (Integer a : A) {
            // This multiplication is comparable to the H function
            for (int a_j = N - a + 1; a_j < N + 1; a_j++) {
                denom = denom.multiply(BigInteger.valueOf(a_j));
            }
            sum += a;
        }

        // This multiplication is comparable to the H function
        for (int a_j = N - sum + 1; a_j < N + 1; a_j++) {
            numer = numer.multiply(BigInteger.valueOf(a_j));
        }

        p = new BigDecimal(numer)
            .divide(new BigDecimal(denom), mc)
            .doubleValue();
        return 1.0d - p;
    }

    /**
     * The probability that no samples of sizes `A` share a value from a population of size `N`.
     * 
     * Uses an optimized formula.
     * 
     * @param A Sample sizes
     * @param N Population size
     * @return Likelihood of an exclusive relationship
     */
    public static double likelihoodOfAnExclusiveRelationshipCompletelyOptimized(final Integer[] A, final Integer N) {
        Integer[] sortedA = A.clone();
        Arrays.sort(sortedA);

        int initialX;
        int initialXofLastH = N + 1;
        int sum = 0;
        double p;

        BigInteger numer;
        BigInteger denom = BigInteger.ONE;
        BigInteger h = BigInteger.ONE;
        // Set precision to 15
        MathContext mc = new MathContext(15);

        for (int a : sortedA) {
            initialX = N - a + 1;
            // Calculating h up to the last x used in an h calculation
            for (int a_j = initialX; a_j < initialXofLastH; a_j++) {
                h = h.multiply(BigInteger.valueOf(a_j));
            }
            denom = denom.multiply(h);
            sum += a;

            // Update memory
            initialXofLastH = initialX;
        }

        // Numerator Computations
        numer = h;
        // Calculating h up to the last x used in an h calculation
        for (int a_j = N - sum + 1; a_j < initialXofLastH; a_j++) {
            numer = numer.multiply(BigInteger.valueOf(a_j));
        }
        p = new BigDecimal(numer)
            .divide(new BigDecimal(denom), mc)
            .doubleValue();
        return 1.0d - p;
    }
}