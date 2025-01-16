import numpy as np
import random

class CircuitAnalysis:
    """
    Provides analysis routines: connectivity checks, 
    Monte Carlo for resistor tolerance, etc.
    """

    def __init__(self, circuit):
        self.circuit = circuit

    def run_analysis(self):
        """
        Runs general checks on the circuit (e.g., connectivity).
        Returns a dict of analysis results (e.g. 'is_connected': bool, etc.).
        """
        results = {}
        results['is_connected'] = self.check_connectivity()
        results['node_count'] = len(self.circuit.get_all_nodes())
        results['resistor_count'] = len(self.circuit.get_resistors())
        results['voltage_source_count'] = len(self.circuit.get_voltage_sources())
        return results

    def check_connectivity(self):
        """
        Simple connectivity check:
        - If there's at least one element connecting the circuit, we do an adjacency search.
        """
        all_nodes = list(self.circuit.get_all_nodes())
        if not all_nodes:
            return True  # no nodes => trivially "connected"

        adjacency = {node: set() for node in all_nodes}
        for elem in self.circuit.elements:
            adjacency[elem.node1].add(elem.node2)
            adjacency[elem.node2].add(elem.node1)

        visited = set()

        def dfs(start):
            stack = [start]
            while stack:
                curr = stack.pop()
                if curr not in visited:
                    visited.add(curr)
                    stack.extend(adjacency[curr] - visited)

        # Start from first node
        dfs(all_nodes[0])
        return len(visited) == len(all_nodes)

    def run_monte_carlo(self, runs=10, tolerance=0.05):
        """
        Demonstrates a simple Monte Carlo approach where each resistor 
        is varied ±tolerance around its nominal value. For each run:
        1) randomize resistor values
        2) run DC simulation
        3) store results
        """
        from .circuit_simulation import DCSolver  # import here to avoid circular deps
        results = []

        # Original resistor values (to restore after simulation)
        original_values = [r.resistance for r in self.circuit.get_resistors()]

        for _ in range(runs):
            # Randomize resistor values within ±tolerance
            for resistor in self.circuit.get_resistors():
                nominal = resistor.resistance
                # random factor between (1 - tolerance) and (1 + tolerance)
                factor = 1 + random.uniform(-tolerance, tolerance)
                resistor.resistance = nominal * factor

            # Solve
            solver = DCSolver(self.circuit)
            node_voltages = solver.run_dc_analysis()

            # Capture the changed resistor values + node voltages
            current_values = {r.name: r.resistance for r in self.circuit.get_resistors()}
            results.append((node_voltages, current_values))

        # Restore original values
        for resistor, orig_val in zip(self.circuit.get_resistors(), original_values):
            resistor.resistance = orig_val

        return results
