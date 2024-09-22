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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for DEC Production Decision}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $x_i$: the number of systems produced for system $i$ where $i = 1, \ldots, N$.
    \item $y_i$: the number of 256K memory boards used for system $i$.
    \item $z_i$: the number of alternative memory boards used for system $i$.
    \item $d_i$: the number of disk drives used for system $i$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: number of different systems.
    \item $is\_workstation[i]$: boolean indicating if system $i$ is a workstation.
    \item $price[i]$: price of system $i$ in dollars.
    \item $disk[i]$: average number of disk drives requested for system $i$.
    \item $mem[i]$: average number of 256K memory boards requested for system $i$.
    \item $max\_cpu$: maximum number of CPUs available.
    \item $min\_disk$: minimum disk drives available.
    \item $max\_disk$: maximum disk drives available.
    \item $min\_mem$: minimum 256K memory boards available.
    \item $max\_mem$: maximum 256K memory boards available.
    \item $demand[i]$: maximum demand for system $i$.
    \item $demand\_GP$: maximum demand for the GP family.
    \item $demand\_WS$: maximum demand for the WS family.
    \item $preorder[i]$: preorders for system $i$.
    \item $alt\_mem$: units of alternative memory boards available.
    \item $alt\_compatible[i]$: boolean indicating if alternative memory can be used in system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price[i] \cdot x_i) - \text{Costs}
\]

\subsection*{Constraints}
\begin{itemize}
    \item CPU Constraint:
    \[
    \sum_{i=1}^{N} x_i \leq max\_cpu
    \]

    \item Disk Drives Constraint:
    \[
    \sum_{i=1}^{N} disk[i] \cdot x_i \leq max\_disk \quad \text{and} \quad \sum_{i=1}^{N} disk[i] \cdot x_i \geq min\_disk
    \]

    \item Memory Boards Constraint:
    \[
    \sum_{i=1}^{N} mem[i] \cdot x_i \leq max\_mem \quad \text{and} \quad \sum_{i=1}^{N} mem[i] \cdot x_i \geq min\_mem
    \]

    \item Demand Constraints:
    \[
    x_i \leq demand[i] \quad \forall i
    \]
    \[
    \sum_{i \text{ such that } is\_workstation[i]} x_i \leq demand\_WS
    \]
    \[
    \sum_{i \text{ such that } \neg is\_workstation[i]} x_i \leq demand\_GP
    \]

    \item Preorder Constraints:
    \[
    x_i \geq preorder[i] \quad \forall i
    \]

    \item Alternative Memory Boards Usage Constraint (only for compatible systems):
    \[
    z_i \leq alt\_mem \quad \text{if } alt\_compatible[i] \text{ is true}
    \]

    \item 256K Boards Usage:
    \[
    y_i = mem[i] \cdot x_i \quad \forall i
    \]

    \item Disk Drives Usage:
    \[
    d_i = disk[i] \cdot x_i \quad \forall i
    \]

\end{itemize}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for DEC Production Decision}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $x_i$: the number of systems produced for system $i$ where $i = 1, \ldots, N$.
    \item $y_i$: the number of 256K memory boards used for system $i$.
    \item $z_i$: the number of alternative memory boards used for system $i$.
    \item $d_i$: the number of disk drives used for system $i$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: number of different systems.
    \item $is\_workstation[i]$: boolean indicating if system $i$ is a workstation.
    \item $price[i]$: price of system $i$ in dollars.
    \item $disk[i]$: average number of disk drives requested for system $i$.
    \item $mem[i]$: average number of 256K memory boards requested for system $i$.
    \item $max\_cpu$: maximum number of CPUs available.
    \item $min\_disk$: minimum disk drives available.
    \item $max\_disk$: maximum disk drives available.
    \item $min\_mem$: minimum 256K memory boards available.
    \item $max\_mem$: maximum 256K memory boards available.
    \item $demand[i]$: maximum demand for system $i$.
    \item $demand\_GP$: maximum demand for the GP family.
    \item $demand\_WS$: maximum demand for the WS family.
    \item $preorder[i]$: preorders for system $i$.
    \item $alt\_mem$: units of alternative memory boards available.
    \item $alt\_compatible[i]$: boolean indicating if alternative memory can be used in system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price[i] \cdot x_i) - \text{Costs}
\]

\subsection*{Constraints}
\begin{itemize}
    \item CPU Constraint:
    \[
    \sum_{i=1}^{N} x_i \leq max\_cpu
    \]

    \item Disk Drives Constraint:
    \[
    \sum_{i=1}^{N} disk[i] \cdot x_i \leq max\_disk \quad \text{and} \quad \sum_{i=1}^{N} disk[i] \cdot x_i \geq min\_disk
    \]

    \item Memory Boards Constraint:
    \[
    \sum_{i=1}^{N} mem[i] \cdot x_i \leq max\_mem \quad \text{and} \quad \sum_{i=1}^{N} mem[i] \cdot x_i \geq min\_mem
    \]

    \item Demand Constraints:
    \[
    x_i \leq demand[i] \quad \forall i
    \]
    \[
    \sum_{i \text{ such that } is\_workstation[i]} x_i \leq demand\_WS
    \]
    \[
    \sum_{i \text{ such that } \neg is\_workstation[i]} x_i \leq demand\_GP
    \]

    \item Preorder Constraints:
    \[
    x_i \geq preorder[i] \quad \forall i
    \]

    \item Alternative Memory Boards Usage Constraint (only for compatible systems):
    \[
    z_i \leq alt\_mem \quad \text{if } alt\_compatible[i] \text{ is true}
    \]

    \item 256K Boards Usage:
    \[
    y_i = mem[i] \cdot x_i \quad \forall i
    \]

    \item Disk Drives Usage:
    \[
    d_i = disk[i] \cdot x_i \quad \forall i
    \]

\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

#### Problem definition
problem = pulp.LpProblem("DEC_Production_Decision", pulp.LpMaximize)

#### Variables
N = data['N']
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts("z", range(N), lowBound=0, cat='Integer')

#### Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(N))
problem += profit

#### Constraints
#### CPU Constraint
problem += pulp.lpSum(x[i] for i in range(N)) <= data['MaxCpu']

#### Disk Drives Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) <= data['MaxDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) >= data['MinDisk']

#### Memory Boards Constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(N)) <= data['MaxMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(N)) >= data['MinMemory']

#### Demand Constraints
for i in range(N):
    problem += x[i] <= data['Demand'][i]

problem += pulp.lpSum(x[i] for i in range(N) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(N) if not data['IsWorkstation'][i]) <= data['DemandGP']

#### Preorder Constraints
for i in range(N):
    problem += x[i] >= data['Preorder'][i]

#### Alternative Memory Boards Usage Constraint
for i in range(N):
    if data['AltCompatible'][i]:
        problem += z[i] <= data['AltMemory']

#### 256K Boards Usage
for i in range(N):
    problem += y[i] == data['MemoryBoards'][i] * x[i]

#### Disk Drives Usage
for i in range(N):
    problem += pulp.LpVariable(f'd_{i}', lowBound=0, cat='Integer') == data['DiskDrives'][i] * x[i]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

