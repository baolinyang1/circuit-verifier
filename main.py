# import sys
# from circuit_simulator.circuit_parser import CircuitParser
# from circuit_simulator.circuit_simulation import DCSolver

# def main(netlist_path: str):
#     print(f"Reading netlist from: {netlist_path}")

#     # 1. Parse the netlist into a circuit object
#     parser = CircuitParser(netlist_path)
#     circuit = parser.parse()

#     # 2. Perform a DC operating point simulation
#     solver = DCSolver(circuit)
#     node_voltages = solver.run_dc_analysis()

#     # 3. Print results
#     print("\n--- DC Operating Point Simulation Results ---")
#     for node, voltage in node_voltages.items():
#         print(f"Node {node}: {voltage:.4f} V")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python main.py <path_to_netlist>")
#         sys.exit(1)

#     netlist_file = sys.argv[1]
#     main(netlist_file)
import sys
from circuit_verification.circuit_parser import CircuitParser
from circuit_verification.circuit_simulation import DCSolver
from circuit_verification.circuit_analysis import CircuitAnalysis
from circuit_verification.circuit_verifier import CircuitVerifier

def main(netlist_path: str):
    # Step 1: Parse the circuit
    parser = CircuitParser(netlist_path)
    circuit = parser.parse()

    # Step 2: Basic DC simulation
    solver = DCSolver(circuit)
    node_voltages = solver.run_dc_analysis()

    # Step 3: Perform connectivity & Monte Carlo analyses
    analysis = CircuitAnalysis(circuit)
    analysis_results = analysis.run_analysis()

    # For demonstration: a quick Monte Carlo on resistor tolerances
    # (e.g., ±5% random variation, 10 runs).
    mc_results = analysis.run_monte_carlo(runs=10, tolerance=0.05)

    # Step 4: Verification checks
    verifier = CircuitVerifier(circuit, node_voltages, analysis_results)
    verification_results = verifier.verify()

    # Print results
    print("\n--- DC Operating Point ---")
    for node, voltage in node_voltages.items():
        print(f"Node {node}: {voltage:.4f} V")

    print("\n--- Analysis Results ---")
    for key, val in analysis_results.items():
        print(f"{key}: {val}")

    print("\n--- Verification Results ---")
    for key, val in verification_results.items():
        print(f"{key}: {val}")

    print("\n--- Monte Carlo Results (Resistor Tolerances) ---")
    for i, (run_voltages, run_values) in enumerate(mc_results):
        print(f"Run #{i+1}: Resistor Values = {run_values}, Node Voltages = {run_voltages}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_netlist>")
        sys.exit(1)

    netlist_file = sys.argv[1]
    main(netlist_file)
