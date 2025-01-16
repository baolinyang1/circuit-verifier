class CircuitVerifier:
    """
    Performs circuit verification checks:
      - Presence of at least one voltage source
      - No floating nodes (if reference node is 0, ensure that the circuit is connected)
    """

    def __init__(self, circuit, dc_solution, analysis_results):
        self.circuit = circuit
        self.dc_solution = dc_solution
        self.analysis_results = analysis_results

    def verify(self):
        checks = {}
        checks['has_voltage_source'] = self.has_voltage_source()
        checks['is_fully_connected'] = self.analysis_results.get('is_connected', False)
        checks['no_floating_nodes'] = self.no_floating_nodes()
        return checks

    def has_voltage_source(self):
        return len(self.circuit.get_voltage_sources()) > 0

    def no_floating_nodes(self):
        """
        If the circuit is connected and node 0 is present, 
        we consider there to be no floating nodes.
        """
        return self.analysis_results.get('is_connected', False) and ('0' in self.circuit.get_all_nodes())
