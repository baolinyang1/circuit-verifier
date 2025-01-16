import pytest
from circuit_verification.circuit_parser import CircuitParser
from circuit_verification.circuit_analysis import CircuitAnalysis

def test_circuit_analysis():
    parser = CircuitParser('examples/example_circuit.net')
    circuit = parser.parse()

    analysis = CircuitAnalysis(circuit)
    results = analysis.run_analysis()

    assert results['is_connected'] == True
    assert results['node_count'] >= 2
    assert results['resistor_count'] == 2
    assert results['voltage_source_count'] == 1
