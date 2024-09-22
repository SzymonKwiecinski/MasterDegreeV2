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

\section*{Mathematical Model for DEC Computer Systems Production}

\subsection*{Variables}

Let \( x_i \) be the number of systems produced for system \( i \) where \( i = 1, 2, \ldots, N \).

Let \( y_i \) be the number of alternative memory boards used for system \( i \) where \( i = 1, 2, \ldots, N \).

\subsection*{Parameters}

\begin{itemize}
    \item \( \text{is\_workstation}[i] \): Boolean indicating if system \( i \) is a workstation (WS).
    \item \( \text{price}[i] \): Price of system \( i \) in dollars.
    \item \( \text{disk\_drives}[i] \): Average number of disk drives requested for system \( i \).
    \item \( \text{256K\_boards}[i] \): Average number of 256K memory boards used for system \( i \).
    \item \( \text{max\_cpu} \): Maximum available CPUs.
    \item \( \text{min\_disk} \): Minimum available disk drives.
    \item \( \text{max\_disk} \): Maximum available disk drives.
    \item \( \text{min\_mem} \): Minimum available 256K memory boards.
    \item \( \text{max\_mem} \): Maximum available 256K memory boards.
    \item \( \text{demand}[i] \): Maximum demand for system \( i \).
    \item \( \text{demand\_GP} \): Maximum demand for the whole GP family.
    \item \( \text{demand\_WS} \): Maximum demand for the whole WS family.
    \item \( \text{preorder}[i] \): Preorders for system \( i \).
    \item \( \text{alt\_mem} \): Available alternative memory boards.
    \item \( \text{alt\_compatible}[i] \): Boolean indicating if alternative memory can be used in system \( i \).
\end{itemize}

\subsection*{Objective Function}

Maximize the profit:

\[
\text{Profit} = \sum_{i=1}^{N} ( \text{price}[i] \cdot x_i - \text{cost\_of\_boards}[i] - \text{cost\_of\_disks}[i] )
\]

where:
\[
\text{cost\_of\_boards}[i] = \text{256K\_boards}[i] \cdot x_i + \text{alt\_mem} \cdot y_i
\]
\[
\text{cost\_of\_disks}[i] = \text{disk\_drives}[i] \cdot x_i
\]

\subsection*{Constraints}

\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} & \text{(CPU Constraint)} \\
    & \sum_{i=1}^{N} \text{disk\_drives}[i] \cdot x_i \leq \text{max\_disk} & \text{(Disk Drive Constraint)} \\
    & \sum_{i=1}^{N} \text{256K\_boards}[i] \cdot x_i + \sum_{i=1}^{N} y_i \cdot \text{alt\_compatible}[i] \leq \text{max\_mem} & \text{(Memory Board Constraint)} \\
    & x_i \geq \text{preorder}[i] & \text{(Preorder Fulfillment)} \\
    & x_i \leq \text{demand}[i] & \text{(Individual Demand)} \\
    & x_i \leq \text{demand\_GP} & \text{(GP Family Demand)} \text{ if } \text{is\_workstation}[i] = \text{false} \\
    & x_i \leq \text{demand\_WS} & \text{(WS Family Demand)} \text{ if } \text{is\_workstation}[i] = \text{true} \\
    & x_i \geq 0, \quad y_i \geq 0 \quad \forall i & \text{(Non-negativity)}
\end{align*}

\subsection*{Output}

The output will include:
\begin{itemize}
    \item A list of systems produced, detailing the number produced, total 256K boards used, total alternative boards used, and total disk drives used.
    \item The total profit calculated from the above model.
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

\section*{Mathematical Model for DEC Computer Systems Production}

\subsection*{Variables}

Let \( x_i \) be the number of systems produced for system \( i \) where \( i = 1, 2, \ldots, N \).

Let \( y_i \) be the number of alternative memory boards used for system \( i \) where \( i = 1, 2, \ldots, N \).

\subsection*{Parameters}

\begin{itemize}
    \item \( \text{is\_workstation}[i] \): Boolean indicating if system \( i \) is a workstation (WS).
    \item \( \text{price}[i] \): Price of system \( i \) in dollars.
    \item \( \text{disk\_drives}[i] \): Average number of disk drives requested for system \( i \).
    \item \( \text{256K\_boards}[i] \): Average number of 256K memory boards used for system \( i \).
    \item \( \text{max\_cpu} \): Maximum available CPUs.
    \item \( \text{min\_disk} \): Minimum available disk drives.
    \item \( \text{max\_disk} \): Maximum available disk drives.
    \item \( \text{min\_mem} \): Minimum available 256K memory boards.
    \item \( \text{max\_mem} \): Maximum available 256K memory boards.
    \item \( \text{demand}[i] \): Maximum demand for system \( i \).
    \item \( \text{demand\_GP} \): Maximum demand for the whole GP family.
    \item \( \text{demand\_WS} \): Maximum demand for the whole WS family.
    \item \( \text{preorder}[i] \): Preorders for system \( i \).
    \item \( \text{alt\_mem} \): Available alternative memory boards.
    \item \( \text{alt\_compatible}[i] \): Boolean indicating if alternative memory can be used in system \( i \).
\end{itemize}

\subsection*{Objective Function}

Maximize the profit:

\[
\text{Profit} = \sum_{i=1}^{N} ( \text{price}[i] \cdot x_i - \text{cost\_of\_boards}[i] - \text{cost\_of\_disks}[i] )
\]

where:
\[
\text{cost\_of\_boards}[i] = \text{256K\_boards}[i] \cdot x_i + \text{alt\_mem} \cdot y_i
\]
\[
\text{cost\_of\_disks}[i] = \text{disk\_drives}[i] \cdot x_i
\]

\subsection*{Constraints}

\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} & \text{(CPU Constraint)} \\
    & \sum_{i=1}^{N} \text{disk\_drives}[i] \cdot x_i \leq \text{max\_disk} & \text{(Disk Drive Constraint)} \\
    & \sum_{i=1}^{N} \text{256K\_boards}[i] \cdot x_i + \sum_{i=1}^{N} y_i \cdot \text{alt\_compatible}[i] \leq \text{max\_mem} & \text{(Memory Board Constraint)} \\
    & x_i \geq \text{preorder}[i] & \text{(Preorder Fulfillment)} \\
    & x_i \leq \text{demand}[i] & \text{(Individual Demand)} \\
    & x_i \leq \text{demand\_GP} & \text{(GP Family Demand)} \text{ if } \text{is\_workstation}[i] = \text{false} \\
    & x_i \leq \text{demand\_WS} & \text{(WS Family Demand)} \text{ if } \text{is\_workstation}[i] = \text{true} \\
    & x_i \geq 0, \quad y_i \geq 0 \quad \forall i & \text{(Non-negativity)}
\end{align*}

\subsection*{Output}

The output will include:
\begin{itemize}
    \item A list of systems produced, detailing the number produced, total 256K boards used, total alternative boards used, and total disk drives used.
    \item The total profit calculated from the above model.
\end{itemize}

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

#### Variables
N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_compatible = data['AltCompatible']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_memory = data['MinMemory']
max_memory = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_memory = data['AltMemory']

#### Create a Linear Programming Problem
problem = pulp.LpProblem("DEC_Computer_Production", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') for i in range(N)]

#### Objective Function
cost_of_boards = [memory_boards[i] * x[i] + alt_memory * y[i] for i in range(N)]
cost_of_disks = [disk_drives[i] * x[i] for i in range(N)]
profit = pulp.lpSum([price[i] * x[i] - cost_of_boards[i] - cost_of_disks[i] for i in range(N)])
problem += profit

#### Constraints
#### CPU Constraint
problem += pulp.lpSum(x) <= max_cpu

#### Disk Drive Constraint
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk

#### Memory Board Constraint
problem += pulp.lpSum([memory_boards[i] * x[i] for i in range(N)]) + pulp.lpSum([y[i] * alt_compatible[i] for i in range(N)]) <= max_memory

#### Preorder Fulfillment and Individual Demand
for i in range(N):
    problem += x[i] >= preorder[i]
    problem += x[i] <= demand[i]

#### GP and WS Family Demand
for i in range(N):
    if not is_workstation[i]:
        problem += x[i] <= demand_gp
    else:
        problem += x[i] <= demand_ws

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


