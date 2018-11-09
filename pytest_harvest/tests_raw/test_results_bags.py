# META
# {'passed': 6, 'skipped': 0, 'failed': 0}
# END META
from collections import OrderedDict
from random import random
import pytest

from pytest_harvest import create_results_bag_fixture


def my_algorithm(param, data):
    # let's return a random accuracy !
    return random()


@pytest.fixture(params=['A', 'B', 'C'])
def dataset(request):
    return "my dataset #%s" % request.param


@pytest.mark.parametrize("algo_param", [1, 2], ids=str)
def test_my_app_bench(algo_param, dataset, results_bag):
    """
    This test applies the algorithm with various parameters (`algo_param`)
    on various datasets (`dataset`). Accuracies are stored in a results
    bag (`results_bag`)
    """
    # apply the algorithm with param `algo_param` on dataset `dataset`
    accuracy = my_algorithm(algo_param, dataset)

    # store it in the results bag
    results_bag.accuracy = accuracy


# the result bag
# note: depending on your pytest version, the name used by pytest might be
# the variable name (left) or the one you provide in the 'name' argument so
# make sure they are identical!
results_bag = create_results_bag_fixture('store', name="results_bag")


@pytest.fixture(scope='session', autouse=True)
def store(request):
    # setup: init the store
    store = OrderedDict()
    yield store
    # teardown: here you can collect all
    assert len(store['results_bag']) == 6
    print(dict(store['results_bag']))
