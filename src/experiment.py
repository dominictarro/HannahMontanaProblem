"""
Experiment execution methods.
"""
import multiprocessing.pool as mp
import timeit
import traceback
from dataclasses import dataclass
from typing import Callable, Generator, Iterable, Tuple

import tqdm

from .algorithms import (
        likelihood_of_an_exclusive_relationship_not_optimized,
        likelihood_of_an_exclusive_relationship_algebraically_optimized,
        likelihood_of_an_exclusive_relationship_completely_optimized
)
from .utils import generate_sequence


Algorithm = Callable[[Iterable[int], int], float]
ALGORITHMS: Tuple[Algorithm] = (
    likelihood_of_an_exclusive_relationship_not_optimized,
    likelihood_of_an_exclusive_relationship_algebraically_optimized,
    likelihood_of_an_exclusive_relationship_completely_optimized
)


@dataclass
class Experiment:
    trials_per_n: int
    iterations_per_trial: int
    _range: Tuple[int, int]
    cores: int
    ascending: bool = True

    @property
    def total_algotrials(self) -> int:
        """Count of `AlgorithmTrial` in `self`."""
        return len(ALGORITHMS) * self.total_trials

    @property
    def total_populations(self) -> int:
        """Count of populations to be tested."""
        return max(self._range[1] - self._range[0] + 1, 0)

    @property
    def total_trials(self) -> int:
        """Count of `Trial` in `self`."""
        return self.total_populations * self.trials_per_n

    def _generate_populations(self) -> Generator[int, None, None]:
        if self.ascending:
            _range = range(self._range[0], self._range[1] + 1)
        else:
            _range = range(self._range[1], self._range[0] - 1, -1)

        pbar: tqdm.tqdm = tqdm.tqdm(
            _range,
            desc="Populations",
            colour="blue",
            total=self.total_populations,
            position=1
        )
        for n in pbar:
            yield n

    def _generate_trials(self, n: int) -> Generator[dict, None, None]:
        for i in range(self.trials_per_n):
            trial = trial_context_factory(
                experiment=self,
                index=i + 1,
                population=n
            )
            yield trial

    def trials(self) -> Generator[dict, None, None]:
        for n in self._generate_populations():
            yield from self._generate_trials(n)

    def serial(self) -> Generator[dict, None, None]:
        for algotrial in self.trials():
            yield execute_trial(algotrial)

    def parallel(self) -> Generator[dict, None, None]:
        with mp.Pool(processes=self.cores) as pool:
            generator = pool.imap_unordered(
                func=execute_trial,
                iterable=self.trials(),
                chunksize=min(50, self.total_trials)
            )
            yield from generator

    def run(self) -> Generator[dict, None, None]:
        if self.cores in (0, 1):
            generator = self.serial()
        else:
            generator = self.parallel()

        pbar = tqdm.tqdm(
            generator,
            desc="Trials",
            position=0,
            colour='green',
            total=self.total_trials)

        yield from pbar


def execute_trial(context: dict) -> dict:
    trial_result = dict(
        args=dict(
            population=context['population'],
            sequence=context['sequence'],
        ),
        index=context['index'],
        iterations=context['iterations_per_trial'],
        results=list()
    )
    for algorithm in ALGORITHMS:
        # Generate a namespace shared with timeit.timeit
        result = dict(
                algorithm=algorithm.__name__)
        namespace = dict(
            algorithm=algorithm,
            population=context['population'],
            result=result,
            sequence=context['sequence']
        )
        try:
            stmt = f"""result['result'] = algorithm(sequence, population)"""
            result['runtime'] = timeit.timeit(
                stmt,
                number=context['iterations_per_trial'],
                globals=namespace
            )
        except Exception:
            result['runtime'] = None
            result['result'] = None
            result['error'] = traceback.format_exc()
        finally:
            trial_result['results'].append(result)
    return trial_result


def trial_context_factory(experiment: Experiment, index: int, population: int) -> dict:
    """Creates a trial context dictionary.

    :param experiment:  Experiment the trial is initialized under
    :param index:       Trial index number (First is 1)
    :param population:  Population size
    :return:            Trial dictionary
    """
    max_value = int(population * index / experiment.trials_per_n)
    if max_value <= 1:
        max_value = 2

    ctx = dict(
        index=index,
        iterations_per_trial=experiment.iterations_per_trial,
        population=population,
        sequence=generate_sequence(population, max_value),
        trials_per_n=experiment.trials_per_n,
    )
    return ctx
