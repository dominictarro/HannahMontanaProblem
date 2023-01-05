/**
 * Optimized code for calculating the likelihood of an exclusive relationship.
 * Read the whole project at https://tarro.work/code/the-hannah-montana-problem
 */


/**
 * Calculates the factorial of a number.
 * 
 * @param n 
 * @returns 
 */
function factorial(n: number): number {
    var result: number = 1;
    for (var x = n; x > 1; x--) {
        result *= x;
    }
    return result;
}

/**
 * Counts the number of ways of choosing `r` unordered outcomes from `n` possibilities.
 * 
 * @param n Population size
 * @param r Sample size
 * @returns 
 */
function comb(n: number, r: number): number {
    return factorial(n) / (factorial(r) * factorial(n-r));
}

/**
 * The probability that no samples of sizes `A` share a value from a population of size `N`.
 * 
 * Is not optimized in any way.
 * 
 * @param A Array of sample sizes
 * @param N Population size
 */
function likelihoodOfAnExclusiveRelationshipNotOptimized(A: number[], N: number): number {
    var p: number = 1.0;
    var sum: number = 0.0;

    for (let a of A) {
        p *= comb(N - sum, a) / comb(N, a);
        sum += a;
    }
    return 1.0 - p;
}

/**
 * The probability that no samples of sizes `A` share a value from a population of size `N`.
 * 
 * Uses an optimized formula.
 * 
 * @param A Array of sample sizes
 * @param N Population size
 */
function likelihoodOfAnExclusiveRelationshipAlgebraicallyOptimized(A: number[], N: number): number {
    var sum: number = 0.0;
    var numer: number = 1;
    var denom: number = 1;

    for (let a of A) {
        // This multiplication is comparable to the H function
        for (let x = N - a + 1; x <= N; x++) {
            denom *= x;
        }
        sum += a;
    }
    // This multiplication is comparable to the H function
    for (let x = N - sum + 1; x <= N; x++) {
        numer *= x;
    }
    return 1.0 - numer / denom;
}

/**
 * The probability that no samples of sizes `A` share a value from a population of size `N`.
 * 
 * Uses an optimized formula.
 * 
 * @param A Array of sample sizes
 * @param N Population size
 */
function likelihoodOfAnExclusiveRelationshipCompletelyOptimized(A: number[], N: number): number {
    var sortedA: number[] = A.sort();
    var sum: number = 0.0;
    var numer: number = 1;
    var denom: number = 1;

    // Denominator computations
    var h: number = 1;
    var initial_x: number = 1;
    var initial_x_of_last_h: number = N + 1;

    for (let a of sortedA) {
        initial_x = N - a + 1;
        // Calculating h up to the last x used in an h calculation
        for (let x = initial_x; x < initial_x_of_last_h; x++) {
            h *= x;
        }
        denom *= h;
        sum += a;

        // Update memory
        initial_x_of_last_h = initial_x;
    }

    // Numerator Computations
    // Calculating h up to the last x used in an h calculation
    for (let x = N - sum + 1; x < initial_x_of_last_h; x++) {
        numer *= x;
    }
    numer *= h;
    return 1.0 - numer / denom;
}
