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

\subsection*{Sets and Indices}
\begin{itemize}
    \item $i \in \{1, 2, ..., N\}$: Index for computer system models.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{price}_i$: Price of system $i$.
    \item \text{disk}_i$: Units of disk drive per system $i$.
    \item $\text{mem}_i$: Units of 256K memory boards per system $i$.
    \item $\text{max\_cpu}$: Maximum units of CPU available.
    \item $\text{min\_disk}$, $\text{max\_disk}$: Range for available disk drives.
    \item $\text{min\_mem}$, $\text{max\_mem}$: Range for available 256K memory boards.
    \item $\text{demand}_i$: Maximum demand for system $i$.
    \item $\text{demand\_GP}$: Maximum demand for GP family.
    \item $\text{demand\_WS}$: Maximum demand for WS family.
    \item $\text{preorder}_i$: Preorders for system $i$.
    \item $\text{alt\_mem}$: Alternative memory boards available.
    \item $\text{is\_workstation}_i$: Boolean indicator if system $i$ is a workstation.
    \item $\text{alt\_compatible}_i$: Boolean indicator if system $i$ can use alternative memory.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems of type $i$ to produce.
    \item $\text{disk\_used}_i$: Total disk drives used for system $i$.
    \item $\text{mem\_used}_i$: Total 256K memory boards used for system $i$.
    \item $\text{alt\_used}_i$: Total alternative memory boards used for system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} && \text{(CPU constraint)} \\
    & \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk}_i \cdot x_i \leq \text{max\_disk} && \text{(Disk drive supply constraint)} \\
    & \text{min\_mem} \leq \sum_{i=1}^{N} \text{mem}_i \cdot x_i \leq \text{max\_mem} && \text{(256K memory supply constraint)} \\
    & x_i \leq \text{demand}_i, \quad \forall i && \text{(Demand constraint for each system)} \\
    & \sum_{i: \neg \text{is\_workstation}_i} x_i \leq \text{demand\_GP} && \text{(GP demand constraint)} \\
    & \sum_{i: \text{is\_workstation}_i} x_i \leq \text{demand\_WS} && \text{(WS demand constraint)} \\
    & x_i \geq \text{preorder}_i, \quad \forall i && \text{(Preorder fulfillment constraint)} \\
    & \text{mem\_used}_i = \text{mem}_i \cdot x_i, \quad \forall i && \text{(256K memory usage equation)} \\
    & \text{alt\_used}_i = 0, \quad \forall i \text{ where } \neg \text{alt\_compatible}_i && \text{(Incompatible alternative memory use)} \\
    & \sum_{i} \text{alt\_used}_i \leq \text{alt\_mem} && \text{(Alternative memory supply constraint)} \\
    & x_i \geq 0, \quad \forall i && \text{(Non-negativity constraint)}
\end{align*}

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item $i \in \{1, 2, ..., N\}$: Index for computer system models.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{price}_i$: Price of system $i$.
    \item \text{disk}_i$: Units of disk drive per system $i$.
    \item $\text{mem}_i$: Units of 256K memory boards per system $i$.
    \item $\text{max\_cpu}$: Maximum units of CPU available.
    \item $\text{min\_disk}$, $\text{max\_disk}$: Range for available disk drives.
    \item $\text{min\_mem}$, $\text{max\_mem}$: Range for available 256K memory boards.
    \item $\text{demand}_i$: Maximum demand for system $i$.
    \item $\text{demand\_GP}$: Maximum demand for GP family.
    \item $\text{demand\_WS}$: Maximum demand for WS family.
    \item $\text{preorder}_i$: Preorders for system $i$.
    \item $\text{alt\_mem}$: Alternative memory boards available.
    \item $\text{is\_workstation}_i$: Boolean indicator if system $i$ is a workstation.
    \item $\text{alt\_compatible}_i$: Boolean indicator if system $i$ can use alternative memory.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems of type $i$ to produce.
    \item $\text{disk\_used}_i$: Total disk drives used for system $i$.
    \item $\text{mem\_used}_i$: Total 256K memory boards used for system $i$.
    \item $\text{alt\_used}_i$: Total alternative memory boards used for system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} && \text{(CPU constraint)} \\
    & \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk}_i \cdot x_i \leq \text{max\_disk} && \text{(Disk drive supply constraint)} \\
    & \text{min\_mem} \leq \sum_{i=1}^{N} \text{mem}_i \cdot x_i \leq \text{max\_mem} && \text{(256K memory supply constraint)} \\
    & x_i \leq \text{demand}_i, \quad \forall i && \text{(Demand constraint for each system)} \\
    & \sum_{i: \neg \text{is\_workstation}_i} x_i \leq \text{demand\_GP} && \text{(GP demand constraint)} \\
    & \sum_{i: \text{is\_workstation}_i} x_i \leq \text{demand\_WS} && \text{(WS demand constraint)} \\
    & x_i \geq \text{preorder}_i, \quad \forall i && \text{(Preorder fulfillment constraint)} \\
    & \text{mem\_used}_i = \text{mem}_i \cdot x_i, \quad \forall i && \text{(256K memory usage equation)} \\
    & \text{alt\_used}_i = 0, \quad \forall i \text{ where } \neg \text{alt\_compatible}_i && \text{(Incompatible alternative memory use)} \\
    & \sum_{i} \text{alt\_used}_i \leq \text{alt\_mem} && \text{(Alternative memory supply constraint)} \\
    & x_i \geq 0, \quad \forall i && \text{(Non-negativity constraint)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

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

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("System", range(1, data['N'] + 1), lowBound=0, cat='Continuous')
disk_used = pulp.LpVariable.dicts("DiskUsed", range(1, data['N'] + 1), lowBound=0, cat='Continuous')
mem_used = pulp.LpVariable.dicts("MemUsed", range(1, data['N'] + 1), lowBound=0, cat='Continuous')
alt_used = pulp.LpVariable.dicts("AltUsed", range(1, data['N'] + 1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['Price'][i-1] * x[i] for i in range(1, data['N'] + 1)), "Total_Profit"

#### Constraints
problem += (pulp.lpSum(x[i] for i in range(1, data['N'] + 1)) <= data['MaxCpu']), "CPU_Constraint"
problem += (data['MinDisk'] <= pulp.lpSum(data['DiskDrives'][i-1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxDisk']), "Disk_Constraint"
problem += (data['MinMemory'] <= pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxMemory']), "Memory_Constraint"

#### Demand constraints for each system
for i in range(1, data['N'] + 1):
    problem += (x[i] <= data['Demand'][i-1]), f"Demand_Constraint_{i}"

#### GP and WS demand constraints
problem += (pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if not data['IsWorkstation'][i-1]) <= data['DemandGP']), "GP_Demand_Constraint"
problem += (pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['IsWorkstation'][i-1]) <= data['DemandWS']), "WS_Demand_Constraint"

#### Preorder fulfillment constraints
for i in range(1, data['N'] + 1):
    problem += (x[i] >= data['Preorder'][i-1]), f"Preorder_Constraint_{i}"

#### Memory usage equations
for i in range(1, data['N'] + 1):
    problem += (mem_used[i] == data['MemoryBoards'][i-1] * x[i]), f"Memory_Usage_{i}"

#### Incompatible alternative memory use
for i in range(1, data['N'] + 1):
    if not data['AltCompatible'][i-1]:
        problem += (alt_used[i] == 0), f"Alt_Memory_Incompatible_{i}"

#### Alternative memory supply constraint
problem += (pulp.lpSum(alt_used[i] for i in range(1, data['N'] + 1)) <= data['AltMemory']), "Alt_Memory_Supply_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

