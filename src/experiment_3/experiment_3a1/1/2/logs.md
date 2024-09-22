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

\section*{Mathematical Model for DEC Production Optimization}

\subsection*{Indices}
\begin{itemize}
    \item $i$: Index for systems, where $i = 1, 2, \ldots, N$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $is\_workstation_i$: Boolean indicating if system $i$ is a workstation
    \item $price_i$: Price of system $i$ in dollars
    \item $disk_i$: Average number of disk drives requested per system $i$
    \item $mem_i$: Average number of 256K memory boards requested per system $i$
    \item $max\_cpu$: Maximum available CPUs
    \item $min\_disk$: Minimum supply of disk drives
    \item $max\_disk$: Maximum supply of disk drives
    \item $min\_mem$: Minimum supply of 256K memory boards
    \item $max\_mem$: Maximum supply of 256K memory boards
    \item $demand_i$: Maximum demand for system $i$
    \item $demand\_GP$: Maximum demand for the whole GP family
    \item $demand\_WS$: Maximum demand for the whole WS family
    \item $preorder_i$: Preorders for system $i$
    \item $alt\_mem$: Units of alternative memory boards available
    \item $alt\_compatible_i$: Boolean indicating if system $i$ can use alternative memory
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems produced of type $i$
    \item $y_i$: Number of alternative memory boards used in system $i$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize} \quad \sum_{i=1}^{N} (price_i \cdot x_i) - \sum_{i=1}^{N} (c_{disk} \cdot disk_i \cdot x_i) - \sum_{i=1}^{N} (c_{mem} \cdot mem_i \cdot x_i) - \sum_{i=1}^{N} (c_{alt} \cdot y_i)
\]

Where:
- $c_{disk}$: Cost per disk drive
- $c_{mem}$: Cost per 256K memory board
- $c_{alt}$: Cost per alternative memory board

\subsection*{Constraints}

\begin{align}
\sum_{i=1}^{N} x_i & \leq max\_cpu \quad \text{(CPU constraint)} \\
\sum_{i=1}^{N} disk_i \cdot x_i & \geq min\_disk \quad \text{(Disk supply lower bound)} \\
\sum_{i=1}^{N} disk_i \cdot x_i & \leq max\_disk \quad \text{(Disk supply upper bound)} \\
\sum_{i=1}^{N} mem_i \cdot x_i & \geq min\_mem \quad \text{(Memory supply lower bound)} \\
\sum_{i=1}^{N} mem_i \cdot x_i & \leq max\_mem \quad \text{(Memory supply upper bound)} \\
x_i & \geq preorder_i \quad \text{(Preorder fulfillment)} \quad \forall i \\
\sum_{i: is\_workstation_i} x_i & \leq demand\_WS \quad \text{(Workstation demand)} \\
\sum_{i: \neg is\_workstation_i} x_i & \leq demand\_GP \quad \text{(General-purpose demand)} \\
y_i & \leq alt\_mem \quad \text{(Alternative memory usage limit)} \quad \forall i: alt\_compatible_i \\
\end{align}
\begin{align}
y_i & \leq mem_i \cdot x_i \quad \forall i: alt\_compatible_i \quad \text{(Alternative memory usage only if compatible)}
\end{align}

\subsection*{Output}
The output will be a JSON format with the system output and total profit:
\[
\text{Output} = \left\{ 
\begin{array}{ll}
\text{"system\_output"}: \left[ \right. & \text{for each system } i \\
    \{ x_i, mem_i \cdot x_i, y_i, disk_i \cdot x_i \} & \\
\text{for } i = 1, \ldots, N & \left. \right] \\
\text{"profit"}: \text{Total profit} &
\end{array}
\right\}
\]

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

\section*{Mathematical Model for DEC Production Optimization}

\subsection*{Indices}
\begin{itemize}
    \item $i$: Index for systems, where $i = 1, 2, \ldots, N$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $is\_workstation_i$: Boolean indicating if system $i$ is a workstation
    \item $price_i$: Price of system $i$ in dollars
    \item $disk_i$: Average number of disk drives requested per system $i$
    \item $mem_i$: Average number of 256K memory boards requested per system $i$
    \item $max\_cpu$: Maximum available CPUs
    \item $min\_disk$: Minimum supply of disk drives
    \item $max\_disk$: Maximum supply of disk drives
    \item $min\_mem$: Minimum supply of 256K memory boards
    \item $max\_mem$: Maximum supply of 256K memory boards
    \item $demand_i$: Maximum demand for system $i$
    \item $demand\_GP$: Maximum demand for the whole GP family
    \item $demand\_WS$: Maximum demand for the whole WS family
    \item $preorder_i$: Preorders for system $i$
    \item $alt\_mem$: Units of alternative memory boards available
    \item $alt\_compatible_i$: Boolean indicating if system $i$ can use alternative memory
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems produced of type $i$
    \item $y_i$: Number of alternative memory boards used in system $i$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize} \quad \sum_{i=1}^{N} (price_i \cdot x_i) - \sum_{i=1}^{N} (c_{disk} \cdot disk_i \cdot x_i) - \sum_{i=1}^{N} (c_{mem} \cdot mem_i \cdot x_i) - \sum_{i=1}^{N} (c_{alt} \cdot y_i)
\]

Where:
- $c_{disk}$: Cost per disk drive
- $c_{mem}$: Cost per 256K memory board
- $c_{alt}$: Cost per alternative memory board

\subsection*{Constraints}

\begin{align}
\sum_{i=1}^{N} x_i & \leq max\_cpu \quad \text{(CPU constraint)} \\
\sum_{i=1}^{N} disk_i \cdot x_i & \geq min\_disk \quad \text{(Disk supply lower bound)} \\
\sum_{i=1}^{N} disk_i \cdot x_i & \leq max\_disk \quad \text{(Disk supply upper bound)} \\
\sum_{i=1}^{N} mem_i \cdot x_i & \geq min\_mem \quad \text{(Memory supply lower bound)} \\
\sum_{i=1}^{N} mem_i \cdot x_i & \leq max\_mem \quad \text{(Memory supply upper bound)} \\
x_i & \geq preorder_i \quad \text{(Preorder fulfillment)} \quad \forall i \\
\sum_{i: is\_workstation_i} x_i & \leq demand\_WS \quad \text{(Workstation demand)} \\
\sum_{i: \neg is\_workstation_i} x_i & \leq demand\_GP \quad \text{(General-purpose demand)} \\
y_i & \leq alt\_mem \quad \text{(Alternative memory usage limit)} \quad \forall i: alt\_compatible_i \\
\end{align}
\begin{align}
y_i & \leq mem_i \cdot x_i \quad \forall i: alt\_compatible_i \quad \text{(Alternative memory usage only if compatible)}
\end{align}

\subsection*{Output}
The output will be a JSON format with the system output and total profit:
\[
\text{Output} = \left\{ 
\begin{array}{ll}
\text{"system\_output"}: \left[ \right. & \text{for each system } i \\
    \{ x_i, mem_i \cdot x_i, y_i, disk_i \cdot x_i \} & \\
\text{for } i = 1, \ldots, N & \left. \right] \\
\text{"profit"}: \text{Total profit} &
\end{array}
\right\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data setup
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

#### Problem definition
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0, cat='Integer')

#### Objective Function
c_disk = 50  #### hypothetical cost per disk drive
c_mem = 100  #### hypothetical cost per memory board
c_alt = 200  #### hypothetical cost per alternative memory board

problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
            pulp.lpSum(c_disk * data['DiskDrives'][i] * x[i] for i in range(data['N'])) - \
            pulp.lpSum(c_mem * data['MemoryBoards'][i] * x[i] for i in range(data['N'])) - \
            pulp.lpSum(c_alt * y[i] for i in range(data['N']))

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Disk_Supply_Lower_Bound"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Supply_Upper_Bound"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Memory_Supply_Lower_Bound"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Supply_Upper_Bound"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "General_Purpose_Demand"

for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += y[i] <= data['AltMemory'], f"Alternative_Memory_Usage_Limit_{i}"
        problem += y[i] <= data['MemoryBoards'][i] * x[i], f"Alternative_Memory_Usage_Only_If_Compatible_{i}"

#### Solve the problem
problem.solve()

#### Prepare output
output = {
    "system_output": [
        {
            "Produced": x[i].varValue,
            "MemoryUsed": data['MemoryBoards'][i] * x[i].varValue,
            "AltMemoryUsed": y[i].varValue,
            "DiskUsed": data['DiskDrives'][i] * x[i].varValue
        } for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

#### Output result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

