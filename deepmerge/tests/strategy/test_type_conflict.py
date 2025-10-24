import pytest
from typing import Dict

from deepmerge.strategy.type_conflict import TypeConflictStrategies

EMPTY_DICT: Dict = {}

CONTENT_AS_LIST = [{"key": "val"}]


def test_merge_if_not_empty():
    strategy = TypeConflictStrategies.strategy_override_if_not_empty(
        {}, [], EMPTY_DICT, CONTENT_AS_LIST
    )
    assert strategy == CONTENT_AS_LIST

    strategy = TypeConflictStrategies.strategy_override_if_not_empty(
        {}, [], CONTENT_AS_LIST, EMPTY_DICT
    )
    assert strategy == CONTENT_AS_LIST

    strategy = TypeConflictStrategies.strategy_override_if_not_empty({}, [], CONTENT_AS_LIST, None)
    assert strategy == CONTENT_AS_LIST


def test_strategy_raise():
    with pytest.raises(TypeError, match="Type conflict at : cannot merge dict with list"):
        TypeConflictStrategies.strategy_raise({}, [], EMPTY_DICT, CONTENT_AS_LIST)

    with pytest.raises(TypeError, match="Type conflict at key: cannot merge str with int"):
        TypeConflictStrategies.strategy_raise({}, ["key"], "string", 123)

    with pytest.raises(
        TypeError, match="Type conflict at users\\.0\\.name: cannot merge int with str"
    ):
        TypeConflictStrategies.strategy_raise({}, ["users", 0, "name"], 42, "John")
