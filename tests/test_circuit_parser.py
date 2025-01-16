import pytest
from circuit_verification.circuit_parser import CircuitParser

def test_circuit_parser():
    parser = CircuitParser('examples/example_circuit.net')
    circuit = parser.parse()
    assert len(circuit.elements) == 3, "Should have 1 voltage source and 2 resistors."
