# class Circuit:
#     """ Holds circuit elements (resistors, voltage sources, etc.). """

#     def __init__(self):
#         self.elements = []

#     def add_element(self, element):
#         self.elements.append(element)

#     def get_all_nodes(self):
#         """ Return a set of all unique node names. """
#         nodes = set()
#         for elem in self.elements:
#             nodes.add(elem.node1)
#             nodes.add(elem.node2)
#         return nodes

#     def __repr__(self):
#         return f"Circuit({self.elements})"


# class CircuitElement:
#     """ Base class for any circuit element. """
#     def __init__(self, name, node1, node2):
#         self.name = name
#         self.node1 = node1
#         self.node2 = node2

#     def __repr__(self):
#         return f"{self.name}({self.node1}, {self.node2})"


# class Resistor(CircuitElement):
#     def __init__(self, name, node1, node2, resistance):
#         super().__init__(name, node1, node2)
#         self.resistance = resistance

#     def __repr__(self):
#         return f"{self.name}(R={self.resistance}Ω, nodes=({self.node1}, {self.node2}))"


# class VoltageSource(CircuitElement):
#     def __init__(self, name, node1, node2, voltage):
#         super().__init__(name, node1, node2)
#         self.voltage = voltage

#     def __repr__(self):
#         return f"{self.name}(V={self.voltage}V, nodes=({self.node1}, {self.node2}))"
class Circuit:
    """ Holds circuit elements (resistors, voltage sources, etc.). """

    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def get_all_nodes(self):
        """ Return a set of all unique node names. """
        nodes = set()
        for elem in self.elements:
            nodes.add(elem.node1)
            nodes.add(elem.node2)
        return nodes

    def get_resistors(self):
        """ Return a list of Resistor objects """
        return [e for e in self.elements if isinstance(e, Resistor)]

    def get_voltage_sources(self):
        """ Return a list of VoltageSource objects """
        return [e for e in self.elements if isinstance(e, VoltageSource)]

    def __repr__(self):
        return f"Circuit({self.elements})"


class CircuitElement:
    """ Base class for any circuit element. """
    def __init__(self, name, node1, node2):
        self.name = name
        self.node1 = node1
        self.node2 = node2

    def __repr__(self):
        return f"{self.name}({self.node1}, {self.node2})"


class Resistor(CircuitElement):
    def __init__(self, name, node1, node2, resistance):
        super().__init__(name, node1, node2)
        self.resistance = resistance

    def __repr__(self):
        return f"{self.name}(R={self.resistance}Ω, nodes=({self.node1}, {self.node2}))"


class VoltageSource(CircuitElement):
    def __init__(self, name, node1, node2, voltage):
        super().__init__(name, node1, node2)
        self.voltage = voltage

    def __repr__(self):
        return f"{self.name}(V={self.voltage}V, nodes=({self.node1}, {self.node2}))"
