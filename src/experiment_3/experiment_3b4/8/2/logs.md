# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- Digital Equipment Corporation (DEC) has introduced new families of \var{N} computer systems with different memory, disk storage, and expansion capabilities.
- Each system \var{i} is either a general-purpose (GP) system or a workstation (WS) system.
- Each system \var{i} can have an integer number of disk drives, and on average \var{disk_i} units of disk drive per system are requested by customers for system \var{i}.
- System \var{i} uses \var{mem_i} units of 256K memory boards per system on average.
- System \var{i} has a price of \var{price_i} dollars.
- The in-house supplier of CPUs for DEC could provide at most \var{max_cpu} units, due to debugging problems.
- The supply of disk drives is uncertain and is estimated by the manufacturer to be in the range of \var{min_disk} to \var{max_disk} units.
- the supply of 256K memory boards is also limited in the range of \var{min_mem} to \var{max_mem} units.
- Maximum demand for system \var{i} in the next quarter is estimated to be \var{demand_i} units.
- Maximum demand for the whole GP family in the next quarter is estimated to be \var{demand_GP} units.
- Maximum demand for the whole WS family in the next quarter is estimated to be \var{demand_WS} units.
- Included in the projections, there are \var{preorder_i} orders for system \var{i} that have already been received and have to be fulfilled in the next quarter.
- To address the shortage of 256K memory boards, DEC has access to \var{alt_mem} units of an alternative memory board that can only be used in certain systems.
- you can assume the number of systems produced is a floating point number to make the problem easier to solve.

INPUT FORMAT:

{
    "is_workstation": [true/false for i in 1, ..., N],
    "price": [price_i for i in 1, ..., N],
    "disk_drives": [disk_i for i in 1, ..., N],
    "256K_boards": [mem_i for i in 1, ..., N],
    "max_cpu": max_cpu,
    "min_disk": min_disk,
    "max_disk": max_disk,
    "min_mem": min_mem,
    "max_mem": max_mem,
    "demand": [demand_i for i in 1, ..., N],
    "demand_GP": demand_GP,
    "demand_WS": demand_WS,
    "preorder": [preorder_i for i in 1, ..., N],
    "alt_mem": alt_mem,
    "alt_compatible": [true/false for i in 1, ..., N]
}



OBJECTIVE: How many of which system should DEC produce and using what memories and disks to maximize the profit for the next quarter?


OUTPUT INFO:
- A json file with "system_output" and "profit" as keys.
- "system_output" contains a list of different types of systems produced 
- for each system, \var{num_produced} is the number of systems produced, \var{total_256K_boards_used} is the number of 256K memory boards used, \var{total_alt_boards_used} is the number of alternative memory boards used, and \var{total_disk_drives_used} is the number of disk drives used in that system.
- "profit" is the total profit for the next quarter.

OUTPUT FORMAT:

{
    "system_output": [
        {
            "num_produced": x_i,
            "total_256K_boards_used": mem_used_i,
            "total_alt_boards_used": alt_used_i,
            "total_disk_drives_used": disk_used_i
        }
        for i in 1, ..., T
    ],
    "profit": profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
The problem is a Mixed Integer Programming (MIP) problem where DEC needs to determine the optimal production of N types of computer systems to maximize profit, considering constraints on CPUs, disk drives, memory boards, and pre-orders. Below is the mathematical model representation in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for DEC Production Planning}

\textbf{Decision Variables:}

Let \( x_i \) be the number of systems of type \( i \) to produce.

\textbf{Parameters:}

\begin{itemize}
    \item \( \text{price}_i \): Price of system \( i \)
    \item \( \text{disk}_i \): Average disk drives requested per system \( i \)
    \item \( \text{mem}_i \): Average 256K memory boards per system \( i \)
    \item \( \text{demand}_i \): Maximum demand for system \( i \)
    \item \( \text{preorder}_i \): Pre-orders for system \( i \)
    \item \( \text{max\_cpu} \): Maximum CPU units available
    \item \( \text{min\_disk} \), \( \text{max\_disk} \): Minimum and maximum supply of disk drives
    \item \( \text{min\_mem} \), \( \text{max\_mem} \): Minimum and maximum supply of 256K memory boards
    \item \( \text{demand\_GP} \): Maximum demand for GP systems
    \item \( \text{demand\_WS} \): Maximum demand for WS systems
    \item \( \text{alt\_mem} \): Units of alternative memory boards available
    \item \( \text{is\_workstation}[i] \): Boolean indicating if system \( i \) is a workstation
    \item \( \text{alt\_compatible}[i] \): Boolean indicating if system \( i \) can use alternative memory
\end{itemize}

\textbf{Objective:}

Maximize the profit:

\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\textbf{Constraints:}

1. CPU Constraint:
   \[
   \sum_{i=1}^{N} x_i \leq \text{max\_cpu}
   \]

2. Disk Drive Supply Constraint:
   \[
   \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk}_i \cdot x_i \leq \text{max\_disk}
   \]

3. Memory Boards Supply Constraint:
   \[
   \text{min\_mem} \leq \sum_{i=1}^{N} \text{mem}_i \cdot x_i \leq \text{max\_mem}
   \]

4. Demand Constraints for Each System:
   \[
   x_i \leq \text{demand}_i \quad \forall i
   \]

5. Pre-order Fulfillment:
   \[
   x_i \geq \text{preorder}_i \quad \forall i
   \]

6. GP Systems Demand Constraint:
   \[
   \sum_{i, \text{not WS}} x_i \leq \text{demand\_GP}
   \]

7. WS Systems Demand Constraint:
   \[
   \sum_{i, \text{WS}} x_i \leq \text{demand\_WS}
   \]

8. Alternative Memory Utilization:
   \[
   \sum_{i, \text{alt\_compatible}[i]} (\text{mem}_i \cdot x_i - \text{mem}_i) \leq \text{alt\_mem}
   \]

\textbf{Note:}
- The alternative memory utilization constraint assumes that if a system is compatible to use the alternative memory, it will fully utilize the alternative memory before using 256K boards.

\textbf{Relaxation:}
The number of systems produced, \( x_i \), is considered as a continuous variable (floating point) for simplification.

\end{document}
```

This model outlines the decision variables, parameters, objective function, and constraints necessary to solve the given DEC production planning problem, ensuring the constraints on resources and demands are respected while maximizing the profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for DEC Production Planning}

\textbf{Decision Variables:}

Let \( x_i \) be the number of systems of type \( i \) to produce.

\textbf{Parameters:}

\begin{itemize}
    \item \( \text{price}_i \): Price of system \( i \)
    \item \( \text{disk}_i \): Average disk drives requested per system \( i \)
    \item \( \text{mem}_i \): Average 256K memory boards per system \( i \)
    \item \( \text{demand}_i \): Maximum demand for system \( i \)
    \item \( \text{preorder}_i \): Pre-orders for system \( i \)
    \item \( \text{max\_cpu} \): Maximum CPU units available
    \item \( \text{min\_disk} \), \( \text{max\_disk} \): Minimum and maximum supply of disk drives
    \item \( \text{min\_mem} \), \( \text{max\_mem} \): Minimum and maximum supply of 256K memory boards
    \item \( \text{demand\_GP} \): Maximum demand for GP systems
    \item \( \text{demand\_WS} \): Maximum demand for WS systems
    \item \( \text{alt\_mem} \): Units of alternative memory boards available
    \item \( \text{is\_workstation}[i] \): Boolean indicating if system \( i \) is a workstation
    \item \( \text{alt\_compatible}[i] \): Boolean indicating if system \( i \) can use alternative memory
\end{itemize}

\textbf{Objective:}

Maximize the profit:

\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\textbf{Constraints:}

1. CPU Constraint:
   \[
   \sum_{i=1}^{N} x_i \leq \text{max\_cpu}
   \]

2. Disk Drive Supply Constraint:
   \[
   \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk}_i \cdot x_i \leq \text{max\_disk}
   \]

3. Memory Boards Supply Constraint:
   \[
   \text{min\_mem} \leq \sum_{i=1}^{N} \text{mem}_i \cdot x_i \leq \text{max\_mem}
   \]

4. Demand Constraints for Each System:
   \[
   x_i \leq \text{demand}_i \quad \forall i
   \]

5. Pre-order Fulfillment:
   \[
   x_i \geq \text{preorder}_i \quad \forall i
   \]

6. GP Systems Demand Constraint:
   \[
   \sum_{i, \text{not WS}} x_i \leq \text{demand\_GP}
   \]

7. WS Systems Demand Constraint:
   \[
   \sum_{i, \text{WS}} x_i \leq \text{demand\_WS}
   \]

8. Alternative Memory Utilization:
   \[
   \sum_{i, \text{alt\_compatible}[i]} (\text{mem}_i \cdot x_i - \text{mem}_i) \leq \text{alt\_mem}
   \]

\textbf{Note:}
- The alternative memory utilization constraint assumes that if a system is compatible to use the alternative memory, it will fully utilize the alternative memory before using 256K boards.

\textbf{Relaxation:}
The number of systems produced, \( x_i \), is considered as a continuous variable (floating point) for simplification.

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'N': 5,
    'IsWorkstation': [False, False, False, True, True],
    'Price': [60000, 40000, 30000, 30000, 15000],
    'DiskDrives': [0.3, 1.7, 0, 1.4, 0],
    'MemoryBoards': [4, 2, 2, 2, 1],
    'Demand': [1800, 999999, 300, 999999, 999999],
    'Preorder': [0, 500, 0, 500, 400],
    'AltCompatible': [True, False, False, False, False],
    'MaxCpu': 7000,
    'MinDisk': 3000,
    'MaxDisk': 7000,
    'MinMemory': 8000,
    'MaxMemory': 16000,
    'DemandGP': 3800,
    'DemandWS': 3200,
    'AltMemory': 4000
}

#### Problem
problem = pulp.LpProblem("DEC_Production_Planning", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=data['Preorder'][i], cat='Continuous') for i in range(data['N'])]

#### Objective
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

#### Constraints

#### 1. CPU Constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

#### 2. Disk Drive Supply Constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

#### 3. Memory Boards Supply Constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory']

#### 4. Demand Constraints for Each System
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]

#### 5. Pre-order Fulfillment (Already addressed with lower bound in variable)

#### 6. GP Systems Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']

#### 7. WS Systems Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']

#### 8. Alternative Memory Utilization
problem += pulp.lpSum((data['MemoryBoards'][i] * x[i] - data['MemoryBoards'][i]) for i in range(data['N']) if data['AltCompatible'][i]) <= data['AltMemory']

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

