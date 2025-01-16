# import numpy as np
# from .circuit_elements import Resistor, VoltageSource

# class DCSolver:
#     """
#     Very simple DC operating point solver for resistor + DC voltage source circuits.
#     - Node 0 is assumed to be ground (0 V).
#     - Uses the Node Voltage Method (ignores inductors/capacitors/other elements).
#     """

#     def __init__(self, circuit):
#         self.circuit = circuit
#         self.node_list = []
#         self.node_index = {}
#         # We will build the system of equations: G * V = I
#         # Where:
#         #   G is the conductance matrix
#         #   V is the vector of node voltages
#         #   I is the current injection vector

#     def run_dc_analysis(self):
#         # 1. Identify unique nodes (excluding ground "0" from the system)
#         all_nodes = sorted(list(self.circuit.get_all_nodes()))
#         if '0' in all_nodes:
#             all_nodes.remove('0')  # node 0 is reference, so we remove it from unknowns

#         self.node_list = all_nodes
#         self.node_index = {node: i for i, node in enumerate(self.node_list)}

#         # If there are no nodes (other than ground), nothing to solve
#         if not self.node_list:
#             return {'0': 0.0}  # trivial circuit

#         # 2. Initialize the conductance matrix G and current vector I
#         num_nodes = len(self.node_list)
#         G = np.zeros((num_nodes, num_nodes), dtype=float)
#         I = np.zeros(num_nodes, dtype=float)

#         # 3. Stamp Resistors and Voltage Sources into G, I
#         for elem in self.circuit.elements:
#             if isinstance(elem, Resistor):
#                 self._stamp_resistor(G, elem)
#             elif isinstance(elem, VoltageSource):
#                 self._stamp_voltage_source(G, I, elem)

#         # 4. Solve for node voltages
#         #    G * V = I  ->  V = inverse(G) * I
#         #    (or use np.linalg.solve)
#         V_solution = np.linalg.solve(G, I)

#         # 5. Build result dictionary: node_name -> voltage
#         results = {}
#         for node_name, idx in self.node_index.items():
#             results[node_name] = V_solution[idx]

#         # Ground node is always 0 V
#         results['0'] = 0.0

#         return results

#     def _stamp_resistor(self, G, resistor):
#         """
#         Stamp a resistor into the conductance matrix.
#         - If resistor is between node 'a' and node 'b', 
#           conductance = 1/R is added to G[a,a] and G[b,b].
#           -1/R is added to G[a,b] and G[b,a].
#         - If node is ground (0), only stamp one side.
#         """
#         n1, n2 = resistor.node1, resistor.node2
#         R = resistor.resistance
#         g = 1.0 / R  # conductance

#         if n1 != '0' and n2 != '0':
#             i1 = self.node_index[n1]
#             i2 = self.node_index[n2]
#             G[i1, i1] += g
#             G[i2, i2] += g
#             G[i1, i2] -= g
#             G[i2, i1] -= g

#         elif n1 == '0' and n2 != '0':
#             i2 = self.node_index[n2]
#             G[i2, i2] += g

#         elif n2 == '0' and n1 != '0':
#             i1 = self.node_index[n1]
#             G[i1, i1] += g

#         # If both nodes are ground (rare but possible), it does nothing to the circuit.

#     def _stamp_voltage_source(self, G, I, vsource):
#         """
#         Stamp an ideal DC voltage source using the Node Voltage Method:
#         - For node a and ground, Va = Vsource (or for node b and ground).
#         - This is effectively a "voltage = constant" constraint.
#         - We'll treat it by forcing that node's voltage in the matrix system:
#             Va = Vsource  -> We make the row for 'a' in G into [0...0 1 0...0],
#                              and the corresponding entry in I is Vsource.
#         - If the source is between two non-ground nodes, we do a simpler approach:
#             Va - Vb = Vsource (still can be done in Node Voltage, but 
#             typically requires an augmented matrix approach or 
#             supernode concept. We'll keep it simple and assume one side is ground.)
#         """
#         n1, n2 = vsource.node1, vsource.node2
#         Vval = vsource.voltage

#         # For simplicity, assume at least one side is ground:
#         if n1 == '0' and n2 != '0':
#             # node n2 is set to +Vval
#             i2 = self.node_index[n2]
#             # Zero out row i2
#             for j in range(len(G[i2])):
#                 G[i2, j] = 0.0
#             G[i2, i2] = 1.0
#             I[i2] = Vval

#         elif n2 == '0' and n1 != '0':
#             # node n1 is set to +Vval
#             i1 = self.node_index[n1]
#             # Zero out row i1
#             for j in range(len(G[i1])):
#                 G[i1, j] = 0.0
#             G[i1, i1] = 1.0
#             I[i1] = Vval

#         else:
#             # If neither side is ground, a more complex approach is needed (supernode).
#             # We keep it simple and raise a warning / partial implementation.
#             print(f"Warning: Voltage source '{vsource.name}' is between two non-ground nodes. "
#                   f"This simple solver only supports one side to ground. Treating it as a no-op.")
import numpy as np
from .circuit_elements import Resistor, VoltageSource

class DCSolver:
    """
    Very simple DC operating point solver using Node Voltage Method:
      - Resistors only (no inductors/capacitors).
      - Voltage sources must have at least one side to ground.
    """

    def __init__(self, circuit):
        self.circuit = circuit
        self.node_list = []
        self.node_index = {}

    def run_dc_analysis(self):
        """ Returns a dict of node_name -> voltage """
        all_nodes = sorted(list(self.circuit.get_all_nodes()))
        # Remove ground node '0' from unknown nodes
        if '0' in all_nodes:
            all_nodes.remove('0')

        self.node_list = all_nodes
        self.node_index = {node: i for i, node in enumerate(self.node_list)}

        if not self.node_list:
            # trivial circuit with only ground
            return {'0': 0.0}

        n = len(self.node_list)
        G = np.zeros((n, n), dtype=float)
        I = np.zeros(n, dtype=float)

        # Stamp each element
        for elem in self.circuit.elements:
            if isinstance(elem, Resistor):
                self._stamp_resistor(G, elem)
            elif isinstance(elem, VoltageSource):
                self._stamp_voltage_source(G, I, elem)

        # Solve G * V = I
        V_solution = np.linalg.solve(G, I)

        # Build final dictionary
        node_voltages = {}
        for node_name, idx in self.node_index.items():
            node_voltages[node_name] = V_solution[idx]
        node_voltages['0'] = 0.0

        return node_voltages

    def _stamp_resistor(self, G, resistor):
        """ Stamp resistor into conductance matrix. """
        n1, n2 = resistor.node1, resistor.node2
        R = resistor.resistance
        g = 1.0 / R

        if n1 != '0' and n2 != '0':
            i1 = self.node_index[n1]
            i2 = self.node_index[n2]
            G[i1, i1] += g
            G[i2, i2] += g
            G[i1, i2] -= g
            G[i2, i1] -= g
        elif n1 == '0' and n2 != '0':
            i2 = self.node_index[n2]
            G[i2, i2] += g
        elif n2 == '0' and n1 != '0':
            i1 = self.node_index[n1]
            G[i1, i1] += g
        # if both are ground, do nothing

    def _stamp_voltage_source(self, G, I, vsource):
        """ 
        Stamp an ideal DC voltage source. 
        For simplicity, if one side is ground, we fix that node's voltage.
        If neither side is ground, we warn (would need supernode logic).
        """
        n1, n2 = vsource.node1, vsource.node2
        Vval = vsource.voltage

        if n1 == '0' and n2 != '0':
            i2 = self.node_index[n2]
            # zero out row
            G[i2, :] = 0.0
            G[i2, i2] = 1.0
            I[i2] = Vval
        elif n2 == '0' and n1 != '0':
            i1 = self.node_index[n1]
            # zero out row
            G[i1, :] = 0.0
            G[i1, i1] = 1.0
            I[i1] = Vval
        else:
            # No ground reference in a simple solver => need advanced approach
            print(f"Warning: Voltage source {vsource.name} is between two non-ground nodes. "
                  f"Simple solver does not handle this fully.")
