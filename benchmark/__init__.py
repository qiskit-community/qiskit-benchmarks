# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import unittest
from ddt import ddt
from collections import defaultdict
from testsuites.random.cases import circuit1, circuit2, pm_config1, pm_config2
from functools import reduce
from .utils import generate_cases, combine

results = {}

@ddt
class TestLevelZero(unittest.TestCase):
    results = defaultdict(dict)

    def __init__(self, test_name, passmanager_factory):
        super().__init__(test_name)
        self.passmanager_factory = passmanager_factory

    @classmethod
    def setUpClass(cls):
        cls.results = defaultdict(dict)

    @classmethod
    def tearDownClass(cls):
        global results
        results = cls.results

    @classmethod
    def save_result(cls, test_name, circuit, config, result):
        cls.results[f'{circuit.name}:{config.name}'][test_name] = result

    # @combine(circuit=[circuit1, circuit2], pm_config=[pm_config1, pm_config2])
    @combine(circuit=[circuit1], pm_config=[pm_config1])
    def test_depth(self, circuit, pm_config):
        ""
        depth = self.passmanager_factory(pm_config).run(circuit).depth()
        TestLevelZero.save_result('depth', circuit=circuit, config=pm_config, result=depth)

    # @combine(circuit=[circuit1, circuit2], pm_config=[pm_config1, pm_config2])
    @combine(circuit=[circuit1], pm_config=[pm_config1])
    def test_time(self, circuit, pm_config):
        ""
        calls = []

        def callback(pass_, time, **_):
            calls.append(time)

        self.passmanager_factory(pm_config).run(circuit, callback=callback)
        total = reduce(lambda a, b: a + b, calls)
        TestLevelZero.save_result('time', circuit=circuit, config=pm_config, result=total)


def test(factory_function):
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestLevelZero)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(TestLevelZero(test_name, factory_function))

    test_result = unittest.TextTestRunner().run(suite)
    if not test_result.wasSuccessful():
        print(f'Tell someone that {factory_function} failed')
        return

    global results
    return results