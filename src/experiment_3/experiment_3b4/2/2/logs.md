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
To model this problem, we need to maximize the profit while adhering to the constraints related to the production capabilities, resource availability, and demand. We'll create a Mixed Integer Programming (MIP) model. Here's the LaTeX representation of the mathematical model for the given problem:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Objective}

Maximize the total profit:

\[
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \times x_i \right)
\]

where \(x_i\) is the number of system \(i\) produced.

\section*{Constraints}

\begin{align}
    \sum_{i=1}^{N} \text{disk}_i \times x_i &\leq \text{max\_disk} \label{eq:disk_max_avail} \\
    \sum_{i=1}^{N} \text{disk}_i \times x_i &\geq \text{min\_disk} \label{eq:disk_min_avail} \\
    \sum_{i=1}^{N} \text{mem}_i \times x_i &\leq \text{max\_mem} \label{eq:mem_max_avail} \\
    \sum_{i=1}^{N} \text{mem}_i \times x_i &\geq \text{min\_mem} \label{eq:mem_min_avail} \\
    \sum_{i=1}^{N} x_i &\leq \text{max\_cpu} \label{eq:cpu_max_avail} \\
    x_i &\leq \text{demand}_i \quad \forall i \label{eq:demand_individual} \\
    \sum_{i \in \text{GP}} x_i &\leq \text{demand\_GP} \label{eq:demand_GP} \\
    \sum_{i \in \text{WS}} x_i &\leq \text{demand\_WS} \label{eq:demand_WS} \\
    x_i &\geq \text{preorder}_i \quad \forall i \label{eq:preorders} \\
    \sum_{i: \text{alt\_compatible}[i]} \text{alt\_mem} \times y_i &\leq \text{alt\_mem} \label{eq:alt_mem_avail} \\
    x_i &= z_i + y_i \quad \forall i \label{eq:mem_type_split} \\
    z_i &\geq 0 \quad \forall i \label{eq:256K_mem_nonneg} \\
    y_i &\geq 0 \quad \forall i \label{eq:alt_mem_nonneg}
\end{align}

Where:
- \(x_i\) is the number of system \(i\) produced.
- \(z_i\) is the number of 256K memory boards used in system \(i\).
- \(y_i\) is the number of alternative boards used in system \(i\).
- \(\text{GP}\) and \(\text{WS}\) are sets of indices of general-purpose and workstation systems respectively.
- \(\text{alt\_compatible}[i]\) is true if the system \(i\) can use alternative memory.

\end{document}
```

This MIP model aims to maximize profits with constraints that ensure production doesn't exceed available resources or predicted demand. Each \(x_i\) represents a decision variable for how many of each system to produce, and \(z_i\) and \(y_i\) represent the allocation of memory resources, ensuring that systems use either standard or alternative memory boards where applicable.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Objective}

Maximize the total profit:

\[
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \times x_i \right)
\]

where \(x_i\) is the number of system \(i\) produced.

\section*{Constraints}

\begin{align}
    \sum_{i=1}^{N} \text{disk}_i \times x_i &\leq \text{max\_disk} \label{eq:disk_max_avail} \\
    \sum_{i=1}^{N} \text{disk}_i \times x_i &\geq \text{min\_disk} \label{eq:disk_min_avail} \\
    \sum_{i=1}^{N} \text{mem}_i \times x_i &\leq \text{max\_mem} \label{eq:mem_max_avail} \\
    \sum_{i=1}^{N} \text{mem}_i \times x_i &\geq \text{min\_mem} \label{eq:mem_min_avail} \\
    \sum_{i=1}^{N} x_i &\leq \text{max\_cpu} \label{eq:cpu_max_avail} \\
    x_i &\leq \text{demand}_i \quad \forall i \label{eq:demand_individual} \\
    \sum_{i \in \text{GP}} x_i &\leq \text{demand\_GP} \label{eq:demand_GP} \\
    \sum_{i \in \text{WS}} x_i &\leq \text{demand\_WS} \label{eq:demand_WS} \\
    x_i &\geq \text{preorder}_i \quad \forall i \label{eq:preorders} \\
    \sum_{i: \text{alt\_compatible}[i]} \text{alt\_mem} \times y_i &\leq \text{alt\_mem} \label{eq:alt_mem_avail} \\
    x_i &= z_i + y_i \quad \forall i \label{eq:mem_type_split} \\
    z_i &\geq 0 \quad \forall i \label{eq:256K_mem_nonneg} \\
    y_i &\geq 0 \quad \forall i \label{eq:alt_mem_nonneg}
\end{align}

Where:
- \(x_i\) is the number of system \(i\) produced.
- \(z_i\) is the number of 256K memory boards used in system \(i\).
- \(y_i\) is the number of alternative boards used in system \(i\).
- \(\text{GP}\) and \(\text{WS}\) are sets of indices of general-purpose and workstation systems respectively.
- \(\text{alt\_compatible}[i]\) is true if the system \(i\) can use alternative memory.

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from input
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

#### Number of systems
N = data['N']

#### Sets of systems
GP = [i for i, is_ws in enumerate(data['IsWorkstation']) if not is_ws]
WS = [i for i, is_ws in enumerate(data['IsWorkstation']) if is_ws]

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts("z", range(N), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')

#### Initialize the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

#### Objective function
problem += pulp.lpSum([data['Price'][i] * x[i] for i in range(N)]), "Total_Profit"

#### Constraints
#### Disk constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(N)]) <= data['MaxDisk'], "Disk_Max"
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(N)]) >= data['MinDisk'], "Disk_Min"

#### Memory constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(N)]) <= data['MaxMemory'], "Memory_Max"
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(N)]) >= data['MinMemory'], "Memory_Min"

#### CPU constraint
problem += pulp.lpSum([x[i] for i in range(N)]) <= data['MaxCpu'], "CPU_Max"

#### Demand constraints
for i in range(N):
    problem += x[i] <= data['Demand'][i], f"Demand_Individual_{i}"

#### Group demand constraints
problem += pulp.lpSum([x[i] for i in GP]) <= data['DemandGP'], "Demand_GP"
problem += pulp.lpSum([x[i] for i in WS]) <= data['DemandWS'], "Demand_WS"

#### Preorder constraints
for i in range(N):
    problem += x[i] >= data['Preorder'][i], f"Preorder_{i}"

#### Alternative memory constraint
problem += pulp.lpSum([data['AltCompatible'][i] * y[i] for i in range(N)]) <= data['AltMemory'], "Alt_Memory"

#### Memory type split constraints
for i in range(N):
    problem += x[i] == z[i] + y[i], f"Mem_Type_Split_{i}"

#### Solve the problem
problem.solve()

#### Print the total profit
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

