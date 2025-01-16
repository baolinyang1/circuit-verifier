# import re
# from .circuit_elements import Circuit, Resistor, VoltageSource

# class CircuitParser:
#     """
#     Reads a simple netlist (R, V only) and builds a Circuit object.
#     Example lines:
#       V1 1 0 DC 5
#       R1 1 2 1000
#       .END
#     """

#     def __init__(self, filepath):
#         self.filepath = filepath

#     def parse(self) -> Circuit:
#         circuit = Circuit()

#         with open(self.filepath, 'r') as f:
#             for line in f:
#                 line = line.strip()
#                 if not line or line.startswith('*'):
#                     # Skip comments/empty lines
#                     continue
#                 if line.upper() == '.END':
#                     # End of netlist
#                     break

#                 tokens = line.split()

#                 # Example tokens for resistor: ["R1", "1", "2", "1000"]
#                 # Example tokens for voltage source: ["V1", "1", "0", "DC", "5"]
#                 element_name = tokens[0].upper()
#                 if element_name.startswith('R'):
#                     # Resistor
#                     # e.g. R1 1 2 1000
#                     node1 = tokens[1]
#                     node2 = tokens[2]
#                     resistance = float(tokens[3])
#                     circuit.add_element(Resistor(name=element_name, node1=node1, node2=node2, resistance=resistance))

#                 elif element_name.startswith('V'):
#                     # Voltage Source (DC)
#                     # e.g. V1 1 0 DC 5
#                     node1 = tokens[1]
#                     node2 = tokens[2]

#                     # We'll assume "DC" next, then the voltage value
#                     if tokens[3].upper() == "DC":
#                         voltage_value = float(tokens[4])
#                     else:
#                         # If netlist doesn't follow the pattern exactly, 
#                         # you might need more robust parsing
#                         voltage_value = float(tokens[3])

#                     circuit.add_element(VoltageSource(name=element_name,
#                                                       node1=node1,
#                                                       node2=node2,
#                                                       voltage=voltage_value))
#                 else:
#                     # Unsupported element for this simple example
#                     print(f"Warning: Skipping unsupported element '{element_name}'")

#         return circuit
import re
from .circuit_elements import Circuit, Resistor, VoltageSource

class CircuitParser:
    """
    Reads a simple netlist (R, V only) and builds a Circuit object.
    Example lines:
      V1 1 0 DC 5
      R1 1 2 1000
      .END
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self) -> Circuit:
        circuit = Circuit()

        with open(self.filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Ignore comments and empty lines
                if not line or line.startswith('*'):
                    continue
                if line.upper() == '.END':
                    break

                tokens = line.split()
                element_name = tokens[0].upper()

                if element_name.startswith('R'):
                    # R1 1 2 1000
                    node1 = tokens[1]
                    node2 = tokens[2]
                    resistance = float(tokens[3])
                    circuit.add_element(
                        Resistor(name=element_name, node1=node1, node2=node2, resistance=resistance)
                    )

                elif element_name.startswith('V'):
                    # V1 1 0 DC 5
                    node1 = tokens[1]
                    node2 = tokens[2]
                    # Next token might be DC + value, or something else
                    if tokens[3].upper() == 'DC':
                        voltage_value = float(tokens[4])
                    else:
                        voltage_value = float(tokens[3])

                    circuit.add_element(
                        VoltageSource(name=element_name, node1=node1, node2=node2, voltage=voltage_value)
                    )

                else:
                    # Unsupported element for this example
                    print(f"Warning: Skipping unsupported element '{element_name}'")

        return circuit
