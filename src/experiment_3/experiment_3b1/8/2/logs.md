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

\section*{Mathematical Model for DEC Production Problem}

\subsection*{Indices}
\begin{itemize}
    \item $i$: index for the different computer systems, where $i = 1, \dots, N$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $is\_workstation[i]$: boolean indicating if system $i$ is a workstation
    \item $price[i]$: price of system $i$
    \item $disk[i]$: average number of disk drives requested for system $i$
    \item $mem[i]$: average number of 256K memory boards requested for system $i$
    \item $max\_cpu$: maximum number of CPUs available
    \item $min\_disk$: minimum supply of disk drives
    \item $max\_disk$: maximum supply of disk drives
    \item $min\_mem$: minimum supply of 256K memory boards
    \item $max\_mem$: maximum supply of 256K memory boards
    \item $demand[i]$: maximum demand for system $i$
    \item $demand\_GP$: maximum demand for the GP family
    \item $demand\_WS$: maximum demand for the WS family
    \item $preorder[i]$: number of preorders for system $i$
    \item $alt\_mem$: units of alternative memory boards available
    \item $alt\_compatible[i]$: boolean indicating if system $i$ can use alternative memory
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x[i]$: number of systems of type $i$ produced (real number)
    \item $y[i]$: number of alternative memory boards used for system $i$ (integer)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price[i] \cdot x[i]) - \text{Costs}
\]

\subsection*{Constraints}
\begin{align*}
    \text{CPU Constraint:} & \quad \sum_{i=1}^{N} x[i] \leq max\_cpu \\
    \text{Disk Drives Constraint:} & \quad \sum_{i=1}^{N} disk[i] \cdot x[i] \in [min\_disk, max\_disk] \\
    \text{Memory Boards Constraint:} & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] + \sum_{i=1}^{N} y[i] \leq max\_mem \\
    \text{Min Memory Constraint:} & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] + \sum_{i=1}^{N} y[i] \geq min\_mem \\
    \text{Demand Constraints:} & \quad x[i] \geq preorder[i] \quad \forall i \\
    & \quad \sum_{i : is\_workstation[i]} x[i] \leq demand\_WS \\
    & \quad \sum_{i : !is\_workstation[i]} x[i] \leq demand\_GP \\
    \text{Alternative Memory Usage:} & \quad y[i] \leq alt\_mem \cdot alt\_compatible[i] \quad \forall i \\
    \text{Non-negativity:} & \quad x[i] \geq 0, \quad y[i] \geq 0 \text{ integer } \quad \forall i
\end{align*}

\subsection*{Output}
The output will be a JSON object structured as follows:
\begin{verbatim}
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
    "profit": Total_Profit
}
\end{verbatim}

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

\section*{Mathematical Model for DEC Production Problem}

\subsection*{Indices}
\begin{itemize}
    \item $i$: index for the different computer systems, where $i = 1, \dots, N$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $is\_workstation[i]$: boolean indicating if system $i$ is a workstation
    \item $price[i]$: price of system $i$
    \item $disk[i]$: average number of disk drives requested for system $i$
    \item $mem[i]$: average number of 256K memory boards requested for system $i$
    \item $max\_cpu$: maximum number of CPUs available
    \item $min\_disk$: minimum supply of disk drives
    \item $max\_disk$: maximum supply of disk drives
    \item $min\_mem$: minimum supply of 256K memory boards
    \item $max\_mem$: maximum supply of 256K memory boards
    \item $demand[i]$: maximum demand for system $i$
    \item $demand\_GP$: maximum demand for the GP family
    \item $demand\_WS$: maximum demand for the WS family
    \item $preorder[i]$: number of preorders for system $i$
    \item $alt\_mem$: units of alternative memory boards available
    \item $alt\_compatible[i]$: boolean indicating if system $i$ can use alternative memory
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x[i]$: number of systems of type $i$ produced (real number)
    \item $y[i]$: number of alternative memory boards used for system $i$ (integer)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price[i] \cdot x[i]) - \text{Costs}
\]

\subsection*{Constraints}
\begin{align*}
    \text{CPU Constraint:} & \quad \sum_{i=1}^{N} x[i] \leq max\_cpu \\
    \text{Disk Drives Constraint:} & \quad \sum_{i=1}^{N} disk[i] \cdot x[i] \in [min\_disk, max\_disk] \\
    \text{Memory Boards Constraint:} & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] + \sum_{i=1}^{N} y[i] \leq max\_mem \\
    \text{Min Memory Constraint:} & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] + \sum_{i=1}^{N} y[i] \geq min\_mem \\
    \text{Demand Constraints:} & \quad x[i] \geq preorder[i] \quad \forall i \\
    & \quad \sum_{i : is\_workstation[i]} x[i] \leq demand\_WS \\
    & \quad \sum_{i : !is\_workstation[i]} x[i] \leq demand\_GP \\
    \text{Alternative Memory Usage:} & \quad y[i] \leq alt\_mem \cdot alt\_compatible[i] \quad \forall i \\
    \text{Non-negativity:} & \quad x[i] \geq 0, \quad y[i] \geq 0 \text{ integer } \quad \forall i
\end{align*}

\subsection*{Output}
The output will be a JSON object structured as follows:
\begin{verbatim}
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
    "profit": Total_Profit
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
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

#### Create the problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0, cat='Integer')

#### Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Boards_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"

for i in range(data['N']):
    problem += y[i] <= data['AltMemory'] * data['AltCompatible'][i], f"Alt_Memory_Usage_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output
output = {
    "system_output": [
        {
            "num_produced": x[i].varValue,
            "total_256K_boards_used": data['MemoryBoards'][i] * x[i].varValue,
            "total_alt_boards_used": y[i].varValue,
            "total_disk_drives_used": data['DiskDrives'][i] * x[i].varValue
        }
        for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

