/**
 * Optimized code for calculating the likelihood of an exclusive relationship.
 * Read the whole project at https://tarro.work/code/the-hannah-montana-problem
 */

/// Computes a factorial.
/// 
/// # Arguments
/// 
/// * `n` - A positive integer to calculate a factorial for
/// 
fn factorial(n: &u64) -> u64 {
    (1..=*n).product::<u64>()
}

/// Counts the number of ways of choosing `r` unordered outcomes from `n` possibilities.
/// 
/// # Arguments
/// 
/// * `n` - The population size
/// * `r` - The sample size
/// 
fn comb(n: &u64, r: &u64) -> u64 {
    (n - r + 1..=*n).product::<u64>() / factorial(r)
}

/// The probability that no samples of sizes `samples` share a value from a population of size `population`.
/// 
/// Is not optimized in any way.
/// 
/// # Arguments
/// 
/// * `samples`     - A vector of sample sizes
/// * `population`  - The population size
/// 
pub fn likelihood_of_an_exclusive_relationship_not_optimized(samples: &Vec<u64>, population: &u64) -> f64 {
    let mut p: f64 = 1.0;
    let mut sum: u64 = 0;
    for a in samples {
        p *= comb(&(population - sum), &a) as f64 / comb(population, a) as f64;
        sum += a;
    }
    1.0 - p
}

/// The probability that no samples of sizes `samples` share a value from a population of size `population`.
/// 
/// Uses an optimized formula.
/// 
/// # Arguments
/// 
/// * `samples`     - A vector of sample sizes
/// * `population`  - The population size
/// 
pub fn likelihood_of_an_exclusive_relationship_algebraically_optimized(samples: &Vec<u64>, population: &u64) -> f64 {
    let mut sum: u64 = 0;
    let mut denom: u64 = 1;
    let numer: u64;
    for a in samples {
        denom *= ((population - a + 1)..=*population).product::<u64>();
        sum += a;
    }
    numer = ((population - sum + 1)..=*population).product::<u64>();
    1.0 - (numer as f64 / denom as f64)
}

/// The probability that no samples of sizes `samples` share a value from a population of size `population`.
/// 
/// Uses an optimized formula and algorithm.
/// 
/// # Arguments
/// 
/// * `samples`     - A vector of sample sizes
/// * `population`  - The population size
/// 
pub fn likelihood_of_an_exclusive_relationship_completely_optimized(samples: &Vec<u64>, population: &u64) -> f64 {
    let mut sorted_samples: Vec<u64> = samples.to_vec();
    sorted_samples.sort();
    let mut sum: u64 = 0;

    let numer: u64;
    let mut denom: u64 = 1;

    let mut h: u64 = 1;
    let mut initial_x: u64;
    let mut initial_x_of_last_h: u64 = population + 1;

    for a in samples {
        initial_x = population - a + 1;
        h *= (initial_x..=initial_x_of_last_h - 1).product::<u64>();
        denom *= h;
        sum += a;

        initial_x_of_last_h = initial_x;
    }

    numer = h * (population - sum + 1..=initial_x_of_last_h - 1).product::<u64>();

    1.0 - (numer as f64 / denom as f64)
}

fn main() {
    let samples: Vec<u64> = vec![300, 2];
    let population: u64 = 1000;
    let result_no = likelihood_of_an_exclusive_relationship_not_optimized(&samples, &population);
    println!("no: {result_no}");
    let result_a = likelihood_of_an_exclusive_relationship_algebraically_optimized(&samples, &population);
    println!("a: {result_a}");
    let result_op = likelihood_of_an_exclusive_relationship_completely_optimized(&samples, &population);
    println!("op: {result_op}");
}