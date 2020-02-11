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

from cases import circuit1, circuit2, pm_config1, pm_config2
from test import combine

results = {}

@ddt
class TestLevelZero(unittest.TestCase):
    results = []

    def __init__(self, test_name, passmanager_factory):
        super().__init__(test_name)
        self.passmanager_factory = passmanager_factory

    @classmethod
    def tearDownClass(cls):
        global results
        results = cls.results

    @classmethod
    def save_result(cls, test_name, **kwargs):
        cls.results.append({test_name: kwargs})

    @combine(circuit=[circuit1, circuit2], pm_config=[pm_config1, pm_config2])
    def test_depth(self, circuit, pm_config):
        ""
        depth = self.passmanager_factory(pm_config).run(circuit).depth()
        TestLevelZero.save_result('depth', circuit=circuit, config=pm_config, result=depth)

    @combine(circuit=[circuit1, circuit2], pm_config=[pm_config1, pm_config2])
    def test_time(self, circuit, pm_config):
        ""
        calls = []

        def callback(pass_, time, **_):
            out_dict = {'pass': str(pass_.__class__),
                        'time': time}
            calls.append(out_dict)

        self.passmanager_factory(pm_config).run(circuit, callback=callback)
        TestLevelZero.save_result('time', circuit=circuit, config=pm_config, result=calls)


def test(factory_function):
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestLevelZero)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(TestLevelZero(test_name, factory_function))

    test_result = unittest.TextTestRunner().run(suite)
    if not test_result.wasSuccessful():
        print(f'Tell someone that {one_entry_point} failed')
        return

    global results
    return results