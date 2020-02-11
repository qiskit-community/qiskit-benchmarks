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

from qiskit.transpiler.preset_passmanagers import level_0_pass_manager
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.pass_manager_config import PassManagerConfig
from qiskit.transpiler import CouplingMap
from cases import circuit1, circuit2, pm_config1, pm_config2
from test import combine
from json import dumps, JSONEncoder


class ResultEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuantumCircuit):
            return obj.name
        if isinstance(obj, PassManagerConfig):
            return obj.__dict__
        if isinstance(obj, CouplingMap):
            return obj.get_edges()
        return JSONEncoder.default(self, obj)


@ddt
class TestLevelZero(unittest.TestCase):
    results = []

    @classmethod
    def tearDownClass(cls):
        print(dumps(cls.results, indent=4, cls=ResultEncoder))

    @classmethod
    def save_result(cls, test_name, **kwargs):
        cls.results.append({test_name: kwargs})

    @combine(circuit=[circuit1, circuit2], pm_config=[pm_config1, pm_config2])
    def test_depth(self, circuit, pm_config):
        ""
        depth = level_0_pass_manager(pm_config).run(circuit).depth()
        TestLevelZero.save_result('depth', circuit=circuit, config=pm_config, result=depth)

    @combine(circuit=[circuit1, circuit2], pm_config=[pm_config1, pm_config2])
    def test_time(self, circuit, pm_config):
        ""
        calls = []

        def callback(pass_, time, **_):
            out_dict = {'pass': str(pass_.__class__),
                        'time': time}
            calls.append(out_dict)

        level_0_pass_manager(pm_config).run(circuit, callback=callback)
        TestLevelZero.save_result('time', circuit=circuit, config=pm_config, result=calls)


if __name__ == '__main__':
    result = unittest.main(verbosity=1)
