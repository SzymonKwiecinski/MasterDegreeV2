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
To model the given problem as a Mixed-Integer Programming (MIP) problem, we need to consider both the supply constraints and the demand constraints. The goal is to maximize the total profit over the next quarter. Here's how we can formulate this problem in LaTeX using a mathematical modeling approach:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for DEC Production Planning}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of system } i \text{ produced (floating point)} \\
\text{mem\_used}_i & : \text{Number of 256K memory boards used by system } i \\
\text{alt\_used}_i & : \text{Number of alternative memory boards used by system } i \\
\text{disk\_used}_i & : \text{Number of disk drives used by system } i
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{is\_workstation}_i & : \text{True if system } i \text{ is a workstation, otherwise False} \\
\text{price}_i & : \text{Price of system } i \\
\text{disk\_i} & : \text{Average number of disk drives per system } i \\
\text{mem\_i} & : \text{Average number of 256K memory boards per system } i \\
\text{max\_cpu} & : \text{Maximum available CPU units} \\
\text{min\_disk}, \text{max\_disk} & : \text{Range of available disk drives} \\
\text{min\_mem}, \text{max\_mem} & : \text{Range of available 256K memory boards} \\
\text{demand}_i & : \text{Maximum demand for system } i \\
\text{demand\_GP} & : \text{Maximum demand for GP systems} \\
\text{demand\_WS} & : \text{Maximum demand for WS systems} \\
\text{preorder}_i & : \text{Pre-orders that need to be fulfilled for system } i \\
\text{alt\_mem} & : \text{Available units of alternative memory boards} \\
\text{alt\_compatible}_i & : \text{True if alternative memory boards can be used in system } i
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \times x_i \right)
\]

\subsection*{Constraints}
\begin{align*}
\sum_{i=1}^{N} x_i & \leq \text{max\_cpu} \\
\sum_{i=1}^{N} \text{disk\_i} \times x_i & \geq \text{min\_disk} \\
\sum_{i=1}^{N} \text{disk\_i} \times x_i & \leq \text{max\_disk} \\
\sum_{i=1}^{N} \text{mem\_i} \times x_i & \geq \text{min\_mem} \\
\sum_{i=1}^{N} \text{mem\_i} \times x_i & \leq \text{max\_mem} \\
x_i & \leq \text{demand}_i, \quad \forall i = 1, \ldots, N \\
\sum_{i: \text{is\_workstation}_i = \text{false}} x_i & \leq \text{demand\_GP} \\
\sum_{i: \text{is\_workstation}_i = \text{true}} x_i & \leq \text{demand\_WS} \\
x_i & \geq \text{preorder}_i, \quad \forall i = 1, \ldots, N \\
\text{alt\_used}_i & \leq \text{alt\_mem}, \quad \forall i: \text{alt\_compatible}_i = \text{true} \\
\text{mem\_used}_i + \text{alt\_used}_i & = \text{mem\_i} \times x_i, \quad \forall i = 1, \ldots, N \\
\text{disk\_used}_i & = \text{disk\_i} \times x_i, \quad \forall i = 1, \ldots, N
\end{align*}

\end{document}
```

The above model captures the essence of the problem where DEC wants to maximize its profit by efficiently allocating resources (CPU, disk drives, and memory boards) to produce various computer systems. The constraints ensure that the production does not exceed resource limitations and demand specifications.

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

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of system } i \text{ produced (floating point)} \\
\text{mem\_used}_i & : \text{Number of 256K memory boards used by system } i \\
\text{alt\_used}_i & : \text{Number of alternative memory boards used by system } i \\
\text{disk\_used}_i & : \text{Number of disk drives used by system } i
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{is\_workstation}_i & : \text{True if system } i \text{ is a workstation, otherwise False} \\
\text{price}_i & : \text{Price of system } i \\
\text{disk\_i} & : \text{Average number of disk drives per system } i \\
\text{mem\_i} & : \text{Average number of 256K memory boards per system } i \\
\text{max\_cpu} & : \text{Maximum available CPU units} \\
\text{min\_disk}, \text{max\_disk} & : \text{Range of available disk drives} \\
\text{min\_mem}, \text{max\_mem} & : \text{Range of available 256K memory boards} \\
\text{demand}_i & : \text{Maximum demand for system } i \\
\text{demand\_GP} & : \text{Maximum demand for GP systems} \\
\text{demand\_WS} & : \text{Maximum demand for WS systems} \\
\text{preorder}_i & : \text{Pre-orders that need to be fulfilled for system } i \\
\text{alt\_mem} & : \text{Available units of alternative memory boards} \\
\text{alt\_compatible}_i & : \text{True if alternative memory boards can be used in system } i
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \times x_i \right)
\]

\subsection*{Constraints}
\begin{align*}
\sum_{i=1}^{N} x_i & \leq \text{max\_cpu} \\
\sum_{i=1}^{N} \text{disk\_i} \times x_i & \geq \text{min\_disk} \\
\sum_{i=1}^{N} \text{disk\_i} \times x_i & \leq \text{max\_disk} \\
\sum_{i=1}^{N} \text{mem\_i} \times x_i & \geq \text{min\_mem} \\
\sum_{i=1}^{N} \text{mem\_i} \times x_i & \leq \text{max\_mem} \\
x_i & \leq \text{demand}_i, \quad \forall i = 1, \ldots, N \\
\sum_{i: \text{is\_workstation}_i = \text{false}} x_i & \leq \text{demand\_GP} \\
\sum_{i: \text{is\_workstation}_i = \text{true}} x_i & \leq \text{demand\_WS} \\
x_i & \geq \text{preorder}_i, \quad \forall i = 1, \ldots, N \\
\text{alt\_used}_i & \leq \text{alt\_mem}, \quad \forall i: \text{alt\_compatible}_i = \text{true} \\
\text{mem\_used}_i + \text{alt\_used}_i & = \text{mem\_i} \times x_i, \quad \forall i = 1, \ldots, N \\
\text{disk\_used}_i & = \text{disk\_i} \times x_i, \quad \forall i = 1, \ldots, N
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

#### Create the linear programming problem
problem = pulp.LpProblem("DEC_Production_Planning", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory"

for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += x[i] <= data['AltMemory'], f"Alt_Memory_Constraint_{i}"

for i in range(data['N']):
    problem += x[i] == data['MemoryBoards'][i] * x[i], f"Memory_Used_{i}"

for i in range(data['N']):
    problem += x[i] == data['DiskDrives'][i] * x[i], f"Disk_Used_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

