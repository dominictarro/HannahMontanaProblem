# HannahMontanaProblem

Formula, algorithm, and performance benchmarking for the likelihood of an exclusive relationship.

## Table of Contents

- [The Problem](#the-problem)
- [Benchmarking Trials](#benchmarking-trials)
  - [Parameters](#parameters)
  - [How to](#how-to)
  - [Output](#output)
  - [Trial Generation](#trial-generation)
- [Notebook](#notebook)

## The Problem

> A client provides you the guest lists of thousands of parties in the USA. He assures you that at these parties every attendee met every other attendee at least once. The client suspects that one guest, Hannah Montana, is not who she purports to be. In fact, he is convinced that Hannah Montana is another celebrity in disguise. His budget can afford a limited number of private investigations. It’s your job to find the celebrities most likely masquerading as Hannah Montana.

[Read More](https://www.tarro.work/code/the-hannah-montana-problem)

## Benchmarking Trials

### Parameters

- -T, --trials
  - The number of trials to generate for each population size
  - Integer
- -R, --rng
  - Range of population sizes (ends included) to generate trials for.
  - Two integers
  - Extras
    - Must be greater than or equal to 2
- -I, --iterations
  - Number of times to run each trial.
  - Integer
- -C, --cores
  - Number of CPUs to distribute trial execution across.
  - Integer
  - Extras
    - -1 uses all available CPUs, 0 executes serially
    - Must be less than or equal the number of CPUs
- --ascending
  - Performs trial execution by ascending population size. Defaults to descending
  - Boolean flag

### How To

1. Install the required packages

```bash
pip install -r requirements.txt
```

2. Check `main.py` parameters

```bash
python main.py benchmark --help
```

3. Run `main.py` with your desired [parameters](#parameters)

```bash
python main.py benchmark -R $start $stop -T $trials_per_pop -I $iterations_per_trial
```

### Output

Trial results are dumped into a LZMA compressed JSON file named like `year-month-day hour-minute.json.xz`. The document is structured like

```json
{
    "meta": {
        "begin": "ISO formatted timestamp",
        "end": "ISO formatted timestamp"
    },
    "params": {
        "trials_per_n": int,
        "iterations_per_trial": int,
        "_range": [int, int],
        "cores": int,
        "ascending": bool
    },
    "results": [
        ...
    ]
}
```

The trial results found in `results` are each structured like

```json
{
            "args": {
                "population": int,
                "sequence": [int, int, ...]
            },
            "index": int,
            "iterations": int,
            "results": [
                {
                    "algorithm": "likelihood_of_an_exclusive_relationship_not_optimized",
                    "result": float,
                    "runtime": float
                },
                {
                    "algorithm": "likelihood_of_an_exclusive_relationship_algebraically_optimized",
                    "result": float,
                    "runtime": float
                },
                {
                    "algorithm": "likelihood_of_an_exclusive_relationship_completely_optimized",
                    "result": float,
                    "runtime": float
                }
            ]
        }
```

Note that the `index` represents the trial index for the population size. `iterations` refers to the number of times the algorithm was run with the given arguments. `runtime` is the total seconds it took to run the algorithm, with `args`, `iterations` number of times. *`runtime` is **not** the average runtime per iteration*.

### Trial Generation

Trials are generated semi-randomly. The pseudo code looks like

```text
for each pop size
    for each trial index
        calculate maximum sample proportional to the trial index
    
        generate semi-random array of samples

        add pop size / array of samples to trials
```

Sample generation is done by [`utils.generate_sequence`](src/utils.py#:~:text=generate_sequence). Pseudo code looks like

```text
loop
    remove largest generated sample if
        sum of samples greater than pop size

    exit loop if
        2+ samples have been generated
        & random number is less than the sample sum / pop size

    generate a sample in range [1, max value]
    add generated to samples 
```

*Because the generation logic requires a minimum of 2 samples, $N$ must be greater than or equal to 3.*

## Notebook

The plots found in the [article](https://www.tarro.work/code/the-hannah-montana-problem) can be found in [Benchmarking.ipynb](./Benchmarking.ipynb). Additional analyses are stored in the [Analyses](/Analyses/) folder.
