# Python-Based Circuit Verification Tool

**December 2023 – November 2024**

Designed and developed a Python-based software tool to verify circuit design functionality using algorithms and statistical methods.  
Implements object-oriented programming (OOP) principles to create scalable, modular code for ease of future maintenance.  
Utilizes Git for version control and coordinated collaborative efforts in a team environment.

## Features

1. **Circuit Parsing**  
   - Reads a simple SPICE-like netlist with resistors, voltage sources, etc.  

2. **Analysis & Simulation**  
   - Basic DC operating point solution using Node Voltage Method.  
   - Connectivity and floating node checks.  
   - **Monte Carlo** simulation for resistor tolerances.  

3. **Verification**  
   - Checks circuit rules: presence of voltage sources, no floating nodes, etc.  

## Getting Started

### Prerequisites

- Python 3.8+  
- Recommended: a virtual environment

### Installation

1. **Clone the repository** (using Git):

   ```bash
   git clone https://github.com/YourUserName/EnhancedCircuitVerificationTool.git
   cd EnhancedCircuitVerificationTool

2. Install dependencies:

pip install -r requirements.txt

3.Run the main script:
python main.py examples/example_circuit.net

4.Run tests:
pytest tests/

