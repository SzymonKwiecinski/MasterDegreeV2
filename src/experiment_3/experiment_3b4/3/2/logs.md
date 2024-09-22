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
To model this problem as a Mixed-Integer Programming (MIP) problem in LaTeX, we need to define the decision variables, the objective function, and the constraints based on the given information.

Let's define the decision variables:
- \( x_i \): Number of systems of type \( i \) produced, where \( i = 1, \ldots, N \).
- \( y_i \): Number of 256K memory boards used for system \( i \).
- \( z_i \): Number of alternative memory boards used for system \( i \).
- \( d_i \): Number of disk drives used for system \( i \).

Now the objective function and constraints in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}

\begin{align}
& \sum_{i=1}^{N} x_i \leq \text{max\_cpu} & \text{(CPU supply constraint)} \label{cpu_constraint} \\
& \sum_{i=1}^{N} d_i \geq \text{min\_disk} & \text{(Minimum disk supply constraint)} \label{min_disk_constraint} \\
& \sum_{i=1}^{N} d_i \leq \text{max\_disk} & \text{(Maximum disk supply constraint)} \label{max_disk_constraint} \\
& \sum_{i=1}^{N} y_i \geq \text{min\_mem} & \text{(Minimum 256K memory constraint)} \label{min_mem_constraint} \\
& \sum_{i=1}^{N} y_i \leq \text{max\_mem} & \text{(Maximum 256K memory constraint)} \label{max_mem_constraint} \\
& \sum_{i \in \text{GP}} x_i \leq \text{demand\_GP} & \text{(Demand for GP systems)} \label{gp_demand} \\
& \sum_{i \in \text{WS}} x_i \leq \text{demand\_WS} & \text{(Demand for WS systems)} \label{ws_demand} \\
& x_i \leq \text{demand}_i & \forall i \quad \text{(System-wise demand constraint)} \label{system_demand_constraint} \\
& x_i \geq \text{preorder}_i & \forall i \quad \text{(Preorder fulfillment constraint)} \label{preorder_constraint} \\
& y_i = \text{mem}_i \cdot x_i & \forall i \quad \text{(256K memory usage)} \label{memory_usage_constraint} \\
& d_i = \text{disk}_i \cdot x_i & \forall i \quad \text{(Disk drive usage)} \label{disk_usage_constraint} \\
& z_i = 0, \quad \text{if } \text{alt\_compatible}_i = \text{false} & \forall i \quad \text{(Alternative memory usage constraint)} \label{alt_mem_constraint} \\
& z_i \leq \text{alt\_mem} & \forall i \quad \text{(Limited alternative memory supply)} \label{alt_mem_supply} \\
& x_i, y_i, z_i, d_i \geq 0 & \forall i \quad \text{(Non-negativity constraint)} \label{nonnegativity_constraint}
\end{align}

\end{document}
```

This MIP model aims to determine the optimal number of each type of system to be produced to maximize profit while adhering to all constraints related to CPU, memory, disk drives, system demands, and preorders. The constraints ensure proper allocation and utilization of resources while meeting customer demands and operational limitations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}

\begin{align}
& \sum_{i=1}^{N} x_i \leq \text{max\_cpu} & \text{(CPU supply constraint)} \label{cpu_constraint} \\
& \sum_{i=1}^{N} d_i \geq \text{min\_disk} & \text{(Minimum disk supply constraint)} \label{min_disk_constraint} \\
& \sum_{i=1}^{N} d_i \leq \text{max\_disk} & \text{(Maximum disk supply constraint)} \label{max_disk_constraint} \\
& \sum_{i=1}^{N} y_i \geq \text{min\_mem} & \text{(Minimum 256K memory constraint)} \label{min_mem_constraint} \\
& \sum_{i=1}^{N} y_i \leq \text{max\_mem} & \text{(Maximum 256K memory constraint)} \label{max_mem_constraint} \\
& \sum_{i \in \text{GP}} x_i \leq \text{demand\_GP} & \text{(Demand for GP systems)} \label{gp_demand} \\
& \sum_{i \in \text{WS}} x_i \leq \text{demand\_WS} & \text{(Demand for WS systems)} \label{ws_demand} \\
& x_i \leq \text{demand}_i & \forall i \quad \text{(System-wise demand constraint)} \label{system_demand_constraint} \\
& x_i \geq \text{preorder}_i & \forall i \quad \text{(Preorder fulfillment constraint)} \label{preorder_constraint} \\
& y_i = \text{mem}_i \cdot x_i & \forall i \quad \text{(256K memory usage)} \label{memory_usage_constraint} \\
& d_i = \text{disk}_i \cdot x_i & \forall i \quad \text{(Disk drive usage)} \label{disk_usage_constraint} \\
& z_i = 0, \quad \text{if } \text{alt\_compatible}_i = \text{false} & \forall i \quad \text{(Alternative memory usage constraint)} \label{alt_mem_constraint} \\
& z_i \leq \text{alt\_mem} & \forall i \quad \text{(Limited alternative memory supply)} \label{alt_mem_supply} \\
& x_i, y_i, z_i, d_i \geq 0 & \forall i \quad \text{(Non-negativity constraint)} \label{nonnegativity_constraint}
\end{align}

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

#### Indices
N = data['N']
GP_indices = [i for i in range(N) if not data['IsWorkstation'][i]]
WS_indices = [i for i in range(N) if data['IsWorkstation'][i]]

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(N)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0) for i in range(N)]
z = [pulp.LpVariable(f'z_{i}', lowBound=0) for i in range(N)]
d = [pulp.LpVariable(f'd_{i}', lowBound=0) for i in range(N)]

#### Objective Function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(N)])
problem += profit

#### Constraints
problem += pulp.lpSum(x) <= data['MaxCpu'], "CPU Supply Constraint"
problem += pulp.lpSum(d) >= data['MinDisk'], "Min Disk Supply Constraint"
problem += pulp.lpSum(d) <= data['MaxDisk'], "Max Disk Supply Constraint"
problem += pulp.lpSum(y) >= data['MinMemory'], "Min Memory Constraint"
problem += pulp.lpSum(y) <= data['MaxMemory'], "Max Memory Constraint"
problem += pulp.lpSum([x[i] for i in GP_indices]) <= data['DemandGP'], "GP Demand"
problem += pulp.lpSum([x[i] for i in WS_indices]) <= data['DemandWS'], "WS Demand"

for i in range(N):
    problem += x[i] <= data['Demand'][i], f"System Demand Constraint {i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder Fulfillment {i}"
    problem += y[i] == data['MemoryBoards'][i] * x[i], f"Memory Usage {i}"
    problem += d[i] == data['DiskDrives'][i] * x[i], f"Disk Usage {i}"
    if data['AltCompatible'][i]:
        problem += z[i] <= data['AltMemory'], f"Alternative Memory Supply {i}"
    else:
        problem += z[i] == 0, f"Alternative Memory Usage Constraint {i}"

#### Solve
problem.solve()

#### Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

