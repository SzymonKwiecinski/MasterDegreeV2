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

\title{Mixed Integer Programming Model for DEC Computer Systems Production}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of computer systems.
    \item $is\_workstation[i]$: Boolean indicating if system $i$ is a workstation (true) or general-purpose (false).
    \item $price[i]$: Price of system $i$ in dollars.
    \item $disk[i]$: Average number of disk drives requested by customers for system $i$.
    \item $mem[i]$: Average number of 256K memory boards used by system $i$.
    \item $max\_cpu$: Maximum number of CPUs available.
    \item $min\_disk$: Minimum number of disk drives available.
    \item $max\_disk$: Maximum number of disk drives available.
    \item $min\_mem$: Minimum number of 256K memory boards available.
    \item $max\_mem$: Maximum number of 256K memory boards available.
    \item $demand[i]$: Maximum demand for system $i$ in the next quarter.
    \item $demand\_GP$: Maximum demand for all general-purpose systems.
    \item $demand\_WS$: Maximum demand for all workstation systems.
    \item $preorder[i]$: Preorders for system $i$ that must be fulfilled.
    \item $alt\_mem$: Available alternative memory boards.
    \item $alt\_compatible[i]$: Boolean indicating if system $i$ can use alternative memory boards.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x[i]$: Number of systems produced of type $i$, where $i = 1, \ldots, N$.
    \item $y[i]$: Number of alternative memory boards used for system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
Z = \sum_{i=1}^{N} (price[i] \cdot x[i]) - \text{costs of memory and disks}
\]

\subsection*{Constraints}
\begin{align}
    \sum_{i=1}^{N} x[i] & \leq max\_cpu \quad \text{(CPU constraint)} \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \geq min\_disk \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \leq max\_disk \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \geq min\_mem \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \leq max\_mem \\
    x[i] & \leq demand[i] \quad \forall i \\
    \sum_{i \text{ s.t. } is\_workstation[i]=true} x[i] & \leq demand\_WS \\
    \sum_{i \text{ s.t. } is\_workstation[i]=false} x[i] & \leq demand\_GP \\
    x[i] & \geq preorder[i] \quad \forall i \\
    y[i] & \leq alt\_mem \quad \text{(Alternative memory constraint)}
\end{align}

\subsection*{Output Format}
\texttt{
\{
    "system\_output": [
        {
            "num\_produced": x[i],
            "total\_256K\_boards\_used": mem[i] \cdot x[i],
            "total\_alt\_boards\_used": y[i],
            "total\_disk\_drives\_used": disk[i] \cdot x[i]
        }
        \text{ for } i = 1, \ldots, T
    ],
    "profit": Z
\}
}

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

\title{Mixed Integer Programming Model for DEC Computer Systems Production}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of computer systems.
    \item $is\_workstation[i]$: Boolean indicating if system $i$ is a workstation (true) or general-purpose (false).
    \item $price[i]$: Price of system $i$ in dollars.
    \item $disk[i]$: Average number of disk drives requested by customers for system $i$.
    \item $mem[i]$: Average number of 256K memory boards used by system $i$.
    \item $max\_cpu$: Maximum number of CPUs available.
    \item $min\_disk$: Minimum number of disk drives available.
    \item $max\_disk$: Maximum number of disk drives available.
    \item $min\_mem$: Minimum number of 256K memory boards available.
    \item $max\_mem$: Maximum number of 256K memory boards available.
    \item $demand[i]$: Maximum demand for system $i$ in the next quarter.
    \item $demand\_GP$: Maximum demand for all general-purpose systems.
    \item $demand\_WS$: Maximum demand for all workstation systems.
    \item $preorder[i]$: Preorders for system $i$ that must be fulfilled.
    \item $alt\_mem$: Available alternative memory boards.
    \item $alt\_compatible[i]$: Boolean indicating if system $i$ can use alternative memory boards.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x[i]$: Number of systems produced of type $i$, where $i = 1, \ldots, N$.
    \item $y[i]$: Number of alternative memory boards used for system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
Z = \sum_{i=1}^{N} (price[i] \cdot x[i]) - \text{costs of memory and disks}
\]

\subsection*{Constraints}
\begin{align}
    \sum_{i=1}^{N} x[i] & \leq max\_cpu \quad \text{(CPU constraint)} \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \geq min\_disk \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \leq max\_disk \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \geq min\_mem \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \leq max\_mem \\
    x[i] & \leq demand[i] \quad \forall i \\
    \sum_{i \text{ s.t. } is\_workstation[i]=true} x[i] & \leq demand\_WS \\
    \sum_{i \text{ s.t. } is\_workstation[i]=false} x[i] & \leq demand\_GP \\
    x[i] & \geq preorder[i] \quad \forall i \\
    y[i] & \leq alt\_mem \quad \text{(Alternative memory constraint)}
\end{align}

\subsection*{Output Format}
\texttt{
\{
    "system\_output": [
        {
            "num\_produced": x[i],
            "total\_256K\_boards\_used": mem[i] \cdot x[i],
            "total\_alt\_boards\_used": y[i],
            "total\_disk\_drives\_used": disk[i] \cdot x[i]
        }
        \text{ for } i = 1, \ldots, T
    ],
    "profit": Z
\}
}

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

#### Create the problem
problem = pulp.LpProblem("DEC_Computer_Systems_Production", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0, cat='Integer')

#### Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - pulp.lpSum(
    (data['DiskDrives'][i] * x[i] + data['MemoryBoards'][i] * y[i]) for i in range(data['N'])
)
problem += profit, "Total_Profit"

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"

for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"
    
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "General_Purpose_Demand_Constraint"
problem += pulp.lpSum(y[i] for i in range(data['N'])) <= data['AltMemory'], "Alternative_Memory_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
output = {
    "system_output": [
        {
            "num_produced": int(x[i].varValue),
            "total_256K_boards_used": int(data['MemoryBoards'][i] * x[i].varValue),
            "total_alt_boards_used": int(y[i].varValue),
            "total_disk_drives_used": int(data['DiskDrives'][i] * x[i].varValue)
        } for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

