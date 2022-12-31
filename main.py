"""
Entrypoint for the experiment.
"""
import datetime
import json
import lzma
import multiprocessing
import os
from dataclasses import asdict
from typing import Tuple

import click

from src.config import RESULT_HOME
from src.experiment import Experiment, ALGORITHMS
from src.utils import generate_file_basename, grammatical_list


@click.group()
def cli():
    ...


def cores_input_callback(ctx: click.Context, param: click.Parameter, value: int) -> int:
    """`click` callback for validating the `cores` option.
    """
    if value == 0:
        return 1
    if value < 0:
        return multiprocessing.cpu_count()
    if value > multiprocessing.cpu_count():
        raise click.exceptions.BadArgumentUsage(param.name, message=f"Cores must be in range [-1, {multiprocessing.cpu_count()}]")
    return value


def range_input_callback(ctx: click.Context, param: click.Parameter, value: Tuple[int, int]) -> Tuple[int, int]:
    """`click` callback for validating the `rng` option.
    """
    if value[0] > value[1]:
        value = value[1], value[0]
    if any(v < 2 for v in value):
        raise click.exceptions.BadArgumentUsage(param.name, message=f"Testable populations must be in range [2, inf.)")
    return value


@cli.command(help=f"Runs the benchmarking experiment for the {grammatical_list((method.__name__ for method in ALGORITHMS))} algorithms.")
@click.option('--trials', '-T', type=int, default=30, help="Number of trials to generate for each population.")
@click.option(
    '--rng', '-R',
    type=int,
    callback=range_input_callback,
    default=(10, 100),
    nargs=2,
    help="Range of population sizes (ends included) to generate trials for.")
@click.option('--iterations', '-I', type=int, default=30, help="Number of times to run each trial.")
@click.option(
    '--cores', '-C',
    type=int,
    callback=cores_input_callback,
    default=-1,
    help="Number of CPUs to use. -1 uses all on machine and 0 uses 1.")
@click.option('--ascending', is_flag=True, help="Test population sizes in ascending order. Descending by default.")
def benchmark(trials: int, rng: Tuple[int, int], iterations: int, cores: int, ascending: bool = True):
    if rng[0] > rng[1]:
        rng = rng[1], rng[0]

    exp = Experiment(
        trials_per_n=trials,
        iterations_per_trial=iterations,
        _range=rng,
        cores=cores,
        ascending=ascending)
    
    result = dict(
        meta=dict(begin=datetime.datetime.now().isoformat()),
        params=asdict(exp),
    )
    try:
        result['results'] = list(exp.run())
    finally:
        result['meta']['end'] = datetime.datetime.now().isoformat()
        filename: str = generate_file_basename(ext='.json')
        filepath: str = os.path.join(RESULT_HOME, filename)
        with lzma.LZMAFile(filepath + '.xz', mode='w', format=lzma.FORMAT_XZ) as fo:
            fo.write(json.dumps(result).encode('utf-8'))


if __name__ == '__main__':
    cli()
