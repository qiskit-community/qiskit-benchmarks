from qiskit import *
from qiskit.transpiler.pass_manager_config import PassManagerConfig
from qiskit.transpiler import CouplingMap

qr = QuantumRegister(3)
circuit1 = QuantumCircuit(qr, name='circuit1')
circuit1.h(qr)
circuit1.cx(qr[0], qr[1])
circuit1.h(qr[0])
circuit1.cx(qr[0], qr[1])

qr = QuantumRegister(3)
circuit2 = QuantumCircuit(qr, name='circuit2')
circuit2.h(qr)
circuit2.cx(qr[0], qr[1])
circuit2.h(qr[0])
circuit2.cx(qr[1], qr[0])

coupling1 = [[1, 0], [1, 2], [2, 3], [4, 3], [4, 10], [5, 4],
             [5, 6], [5, 9], [6, 8], [7, 8], [9, 8], [9, 10],
             [11, 3], [11, 10], [11, 12], [12, 2], [13, 1], [13, 12]]
coupling2 = [[1, 0], [1, 2], [2, 3], [4, 3]]

pm_config1 = PassManagerConfig(seed_transpiler=42, basis_gates=['u1', 'u2', 'u3', 'cx', 'id'],
                               coupling_map=CouplingMap(coupling1))
pm_config2 = PassManagerConfig(seed_transpiler=42, basis_gates=['u1', 'u2', 'u3', 'cx', 'id'],
                               coupling_map=CouplingMap(coupling2))

pm_config1.name = 'pm_config1'
pm_config2.name = 'pm_config2'


def get_case():
    return [(circuit1, pm_config1),
            (circuit2, pm_config2)]
