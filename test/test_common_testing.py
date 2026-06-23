#!/usr/bin/env python3
"""Unit testing module for function compare_common"""

import json
from eda_common import Schema
from common_testing import compare_common
MICROPYTHON = False
try:
    from common_testing import SchemaJSONEncoder
except ImportError:
    MICROPYTHON = True


def test_compare_common_1():
    """Unit test to check function compare_common"""
    data_1 = 1
    data_2 = 1
    assert compare_common(data_1, data_2) is True


def test_compare_common_2():
    """Unit test to check function compare_common"""
    data_1 = 'test-string'
    data_2 = 'test-string'
    assert compare_common(data_1, data_2) is True


def test_compare_common_3():
    """Unit test to check function compare_common"""
    data_1 = [1, 2, 3]
    data_2 = [3, 2, 1]
    assert compare_common(data_1, data_2) is True


def test_compare_common_4():
    """Unit test to check function compare_common"""
    data_1 = {
        'test-key1': 'test-value1',
        'test-key2': 'test-value2'
    }
    data_2 = {
        'test-key2': 'test-value2',
        'test-key1': 'test-value1'
    }
    assert compare_common(data_1, data_2) is True


def test_compare_common_5():
    """Unit test to check function compare_common"""
    data_1 = [
        1,
        'test-string1',
        [
            2,
            'test-string2',
            [
                3,
                'test-string3'
            ]
        ],
        {
            'test-key1': [
                4,
                'test-string4'
            ],
            'test-key2': {
                'test-key3': json.dumps({
                    'test-key4': 'test-value4',
                    'test-key5': 'test-value5'
                })
            }
        }
    ]
    data_2 = [
        {
            'test-key2': {
                'test-key3': json.dumps({
                    'test-key5': 'test-value5',
                    'test-key4': 'test-value4'
                })
            },
            'test-key1': [
                'test-string4',
                4
            ]
        },
        [
            [
                'test-string3',
                3
            ],
            'test-string2',
            2,
        ],
        'test-string1',
        1
    ]
    assert compare_common(data_1, data_2) is True


def test_compare_common_6():
    """Unit test to check function compare_common"""
    if MICROPYTHON is False:
        data_1 = json.dumps({
            'test-key1': 1,
            'test-key2': 'test-value2',
            'test-key3': Schema('test-group', 'test-version', 'test-kind')
        }, cls=SchemaJSONEncoder)
        data_2 = json.dumps({
            'test-key3': Schema('test-group', 'test-version', 'test-kind'),
            'test-key1': 1,
            'test-key2': 'test-value2'
        }, cls=SchemaJSONEncoder)
        assert compare_common(data_1, data_2) is True


def test_compare_common_7():
    """Unit test to check function compare_common"""
    data_1 = json.dumps([
        1,
        'test-string1',
        [
            2,
            'test-string2',
            [
                3,
                'test-string3'
            ]
        ],
        {
            'test-key1': [
                4,
                'test-string4'
            ],
            'test-key2': {
                'test-key3': json.dumps({
                    'test-key4': 'test-value4',
                    'test-key5': 'test-value5'
                })
            }
        }
    ])
    data_2 = json.dumps([
        {
            'test-key2': {
                'test-key3': json.dumps({
                    'test-key5': 'test-value5',
                    'test-key4': 'test-value4'
                })
            },
            'test-key1': [
                'test-string4',
                4
            ]
        },
        [
            [
                'test-string3',
                3
            ],
            'test-string2',
            2,
        ],
        'test-string1',
        1
    ])
    assert compare_common(data_1, data_2) is True


def main():
    """Main function"""
    test_compare_common_1()
    test_compare_common_2()
    test_compare_common_3()
    test_compare_common_4()
    test_compare_common_5()
    test_compare_common_6()
    test_compare_common_7()


if __name__ == '__main__':
    main()
