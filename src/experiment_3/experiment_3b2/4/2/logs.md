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

\section*{Mathematical Model}

Let \( N \) be the number of different computer systems DEC can produce. We will use the indices \( i = 1, \ldots, N \) to denote each system. Define the following parameters:

\begin{align*}
    & \text{is\_workstation}[i] : \text{Boolean, true if system } i \text{ is a workstation, false otherwise},\\
    & \text{price}[i] : \text{Selling price of system } i, \\
    & \text{disk\_drives}[i] : \text{Average number of disk drives requested for system } i, \\
    & \text{256K\_boards}[i] : \text{Average number of 256K memory boards used by system } i, \\
    & \text{max\_cpu} : \text{Maximum CPU units available}, \\
    & \text{min\_disk}, \text{ max\_disk} : \text{Range of available disk drives}, \\
    & \text{min\_mem}, \text{ max\_mem} : \text{Range of available 256K memory boards}, \\
    & \text{demand}[i] : \text{Maximum demand for system } i, \\
    & \text{demand\_GP} : \text{Maximum demand for GP systems}, \\
    & \text{demand\_WS} : \text{Maximum demand for WS systems}, \\
    & \text{preorder}[i] : \text{Preorders for system } i \text{ that must be fulfilled}, \\
    & \text{alt\_mem} : \text{Alternative memory units available}, \\
    & \text{alt\_compatible}[i] : \text{Boolean, true if alternative memory can be used in system } i.
\end{align*}

Define the decision variables:

\begin{align*}
    & x_i : \text{Number of system } i \text{ to produce}, \\
    & \text{mem\_used}_i : \text{Number of 256K memory boards used by system } i, \\
    & \text{alt\_used}_i : \text{Number of alternative memory boards used by system } i, \\
    & \text{disk\_used}_i : \text{Number of disk drives used by system } i.
\end{align*}

The objective function is to maximize the profit, which is given by:

\[
\max \sum_{i=1}^{N} \text{price}[i] \cdot x_i
\]

Subject to the following constraints:

\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu}, \quad \text{(CPU constraint)}\\
    & \sum_{i=1}^{N} \text{disk\_drives}[i] \cdot x_i \leq \text{max\_disk}, \quad \text{(Disk drive upper limit)} \\
    & \sum_{i=1}^{N} \text{disk\_drives}[i] \cdot x_i \geq \text{min\_disk}, \quad \text{(Disk drive lower limit)}\\
    & \sum_{i=1}^{N} \text{256K\_boards}[i] \cdot x_i \leq \text{max\_mem}, \quad \text{(Memory board upper limit)} \\
    & \sum_{i=1}^{N} \text{256K\_boards}[i] \cdot x_i \geq \text{min\_mem}, \quad \text{(Memory board lower limit)}\\
    & x_i \leq \text{demand}[i], \quad \forall i, \quad \text{(Individual system demand)} \\
    & \sum_{i \mid \text{not is\_workstation}[i]} x_i \leq \text{demand\_GP}, \quad \text{(GP demand)} \\
    & \sum_{i \mid \text{is\_workstation}[i]} x_i \leq \text{demand\_WS}, \quad \text{(WS demand)} \\
    & x_i \geq \text{preorder}[i], \quad \forall i, \quad \text{(Fulfill preorders)} \\
    & \text{mem\_used}_i = \text{256K\_boards}[i] \cdot x_i \\
    & \text{alt\_used}_i = \begin{cases} 
        \text{alt\_compatible}[i] \cdot y_i & \text{if } \text{alt\_compatible}[i] = \text{true} \\ 
        0 & \text{otherwise} 
    \end{cases} \\
    & \text{disk\_used}_i = \text{disk\_drives}[i] \cdot x_i, \quad \forall i
\end{align*}

Where the variables \( x_i, \text{mem\_used}_i, \text{alt\_used}_i, \text{disk\_used}_i \) are continuous and non-negative.

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

\section*{Mathematical Model}

Let \( N \) be the number of different computer systems DEC can produce. We will use the indices \( i = 1, \ldots, N \) to denote each system. Define the following parameters:

\begin{align*}
    & \text{is\_workstation}[i] : \text{Boolean, true if system } i \text{ is a workstation, false otherwise},\\
    & \text{price}[i] : \text{Selling price of system } i, \\
    & \text{disk\_drives}[i] : \text{Average number of disk drives requested for system } i, \\
    & \text{256K\_boards}[i] : \text{Average number of 256K memory boards used by system } i, \\
    & \text{max\_cpu} : \text{Maximum CPU units available}, \\
    & \text{min\_disk}, \text{ max\_disk} : \text{Range of available disk drives}, \\
    & \text{min\_mem}, \text{ max\_mem} : \text{Range of available 256K memory boards}, \\
    & \text{demand}[i] : \text{Maximum demand for system } i, \\
    & \text{demand\_GP} : \text{Maximum demand for GP systems}, \\
    & \text{demand\_WS} : \text{Maximum demand for WS systems}, \\
    & \text{preorder}[i] : \text{Preorders for system } i \text{ that must be fulfilled}, \\
    & \text{alt\_mem} : \text{Alternative memory units available}, \\
    & \text{alt\_compatible}[i] : \text{Boolean, true if alternative memory can be used in system } i.
\end{align*}

Define the decision variables:

\begin{align*}
    & x_i : \text{Number of system } i \text{ to produce}, \\
    & \text{mem\_used}_i : \text{Number of 256K memory boards used by system } i, \\
    & \text{alt\_used}_i : \text{Number of alternative memory boards used by system } i, \\
    & \text{disk\_used}_i : \text{Number of disk drives used by system } i.
\end{align*}

The objective function is to maximize the profit, which is given by:

\[
\max \sum_{i=1}^{N} \text{price}[i] \cdot x_i
\]

Subject to the following constraints:

\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu}, \quad \text{(CPU constraint)}\\
    & \sum_{i=1}^{N} \text{disk\_drives}[i] \cdot x_i \leq \text{max\_disk}, \quad \text{(Disk drive upper limit)} \\
    & \sum_{i=1}^{N} \text{disk\_drives}[i] \cdot x_i \geq \text{min\_disk}, \quad \text{(Disk drive lower limit)}\\
    & \sum_{i=1}^{N} \text{256K\_boards}[i] \cdot x_i \leq \text{max\_mem}, \quad \text{(Memory board upper limit)} \\
    & \sum_{i=1}^{N} \text{256K\_boards}[i] \cdot x_i \geq \text{min\_mem}, \quad \text{(Memory board lower limit)}\\
    & x_i \leq \text{demand}[i], \quad \forall i, \quad \text{(Individual system demand)} \\
    & \sum_{i \mid \text{not is\_workstation}[i]} x_i \leq \text{demand\_GP}, \quad \text{(GP demand)} \\
    & \sum_{i \mid \text{is\_workstation}[i]} x_i \leq \text{demand\_WS}, \quad \text{(WS demand)} \\
    & x_i \geq \text{preorder}[i], \quad \forall i, \quad \text{(Fulfill preorders)} \\
    & \text{mem\_used}_i = \text{256K\_boards}[i] \cdot x_i \\
    & \text{alt\_used}_i = \begin{cases} 
        \text{alt\_compatible}[i] \cdot y_i & \text{if } \text{alt\_compatible}[i] = \text{true} \\ 
        0 & \text{otherwise} 
    \end{cases} \\
    & \text{disk\_used}_i = \text{disk\_drives}[i] \cdot x_i, \quad \forall i
\end{align*}

Where the variables \( x_i, \text{mem\_used}_i, \text{alt\_used}_i, \text{disk\_used}_i \) are continuous and non-negative.

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
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

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  #### Number of systems to produce

#### Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_upper_limit"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Disk_lower_limit"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_upper_limit"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Memory_lower_limit"

#### Individual system demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_constraint_{i}"

#### GP and WS demand constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_demand"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS_demand"

#### Preorder constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_constraint_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value at the end
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

