import pytest
from circuit_verification.circuit_parser import CircuitParser
from circuit_verification.circuit_analysis import CircuitAnalysis
from circuit_verification.circuit_simulation import DCSolver
from circuit_verification.circuit_verifier import CircuitVerifier

def test_circuit_verifier():
    parser = CircuitParser('examples/example_circuit.net')
    circuit = parser.parse()

    solver = DCSolver(circuit)
    node_voltages = solver.run_dc_analysis()

    analysis = CircuitAnalysis(circuit)
    analysis_results = analysis.run_analysis()

    verifier = CircuitVerifier(circuit, node_voltages, analysis_results)
    check_results = verifier.verify()

    assert check_results['has_voltage_source'] is True
    assert check_results['is_fully_connected'] is True
    assert check_results['no_floating_nodes'] is True
