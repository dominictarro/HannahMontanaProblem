"""
Utility classes and methods for the project.

"""
import datetime
import random
from typing import Iterable, List, Optional


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_sequence(n: int, max_value: int) -> List[int]:
    """Generates a sequence of values that sum to less than `n`, with no value being greater than `max_value`."""
    result: List[int] = []
    while True:
        # Check if the sum of the sequence exceeds `n`
        seq_sum = sum(result)
        if seq_sum >= n:
            # Remove the largest value in result and try again
            m = max(result)
            result.pop(result.index(m))

        # Probability of terminating increases proportionate to the sum of the sequence
        probability_of_terminating: float = seq_sum / n
        r = random.uniform(0,1)
        # Ensure there are 2 or more values in the sequence before terminating
        if r < probability_of_terminating and len(result) >= 2:
            break
        
        # Generate a random value between 1 and the given maximum
        result.append(random.randint(1, max_value))
    return result

def generate_file_basename(ext: Optional[str] = None) -> str:
    """Generates a filename with the ."""
    basename = datetime.datetime.now().strftime(r'%Y-%m-%d %H-%M')
    if isinstance(ext, str):
        basename += ext
    return basename


def grammatical_list(strings: Iterable[str], conjunction: str = 'and', oxford_comma: bool = True) -> str:
    """Creates a grammatically formatted list.

    :param strings:         Elements of list
    :param conjunction:     Coordinating conjunction to use for the last element of the list
    :param oxford_comma:    Uses an Oxford comma, defaults to True and should always be True

    ```py
    grammatical_list(['dog', 'cat'])
    >>> "dog and cat"
    ```

    ```py
    grammatical_list(['dog', 'cat', 'mouse'])
    >>> "dog, cat, and mouse"
    ```
    """
    _strings = list(strings)
    if len(_strings) == 2:
        return f"{_strings[0]} {conjunction} {_strings[1]}"
    _strings.insert(-1, conjunction)
    if oxford_comma:
        return f"{', '.join(_strings[:-1])} {_strings[-1]}"
    else:
        return f"{', '.join(_strings[:-2])} {' '.join(_strings[-2:])}"
