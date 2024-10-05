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

\section*{Mixed Integer Programming Model for DEC Computer Systems Production}

\textbf{Sets:}
\begin{itemize}
    \item $N$: Set of computer systems indexed by $i = 1, \ldots, N$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $is\_workstation_i \in \{0, 1\}$: Indicates if system $i$ is a workstation (1) or general-purpose (0).
    \item $price_i$: Price of system $i$ in dollars.
    \item $disk_i$: Average disk drives requested per system $i$.
    \item $mem_i$: Average 256K memory boards requested per system $i$.
    \item $max\_cpu$: Maximum available CPU units.
    \item $min\_disk$: Minimum available disk drives.
    \item $max\_disk$: Maximum available disk drives.
    \item $min\_mem$: Minimum available 256K memory boards.
    \item $max\_mem$: Maximum available 256K memory boards.
    \item $demand_i$: Maximum demand for system $i$.
    \item $demand\_GP$: Maximum demand for the general-purpose family.
    \item $demand\_WS$: Maximum demand for the workstation family.
    \item $preorder_i$: Preorders received for system $i$.
    \item $alt\_mem$: Available alternative memory boards.
    \item $alt\_compatible_i \in \{0, 1\}$: Indicates if system $i$ can use alternative memory.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Number of system $i$ produced (continuous).
    \item $y_i$: Number of alternative memory boards used for system $i$ (integer).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{Costs}
\]

\textbf{Subject to:}
\begin{align*}
    & \sum_{i=1}^{N} x_i \leq max\_cpu & \text{(CPU constraint)} \\
    & \sum_{i=1}^{N} disk_i \cdot x_i \leq max\_disk & \text{(Disk drive constraint)} \\
    & \sum_{i=1}^{N} mem_i \cdot x_i + y_i \leq max\_mem & \text{(Memory constraint)} \\
    & \sum_{i=1}^{N} x_i \geq \sum_{i=1}^{N} preorder_i & \text{(Preorder fulfillment)} \\
    & x_i \leq demand_i & \forall i \in N & \text{(Demand constraint for each system)} \\
    & \sum_{i \text{ s.t. } is\_workstation_i} x_i \leq demand\_WS & \text{(Workstation demand)} \\
    & \sum_{i \text{ s.t. } is\_workstation_i=0} x_i \leq demand\_GP & \text{(GP demand)} \\
    & y_i \leq alt\_mem & \forall i \text{ where } alt\_compatible_i=1 & \text{(Alternative memory board allocation)} \\
    & x_i \geq preorder_i & \forall i \in N & \text{(Minimum production for preorders)} \\
    & x_i \geq 0 & \forall i \in N & \text{(Non-negativity)} \\
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item $system\_output$: List of produced systems with their respective board and drive usage.
    \item $profit$: Total profit for the next quarter.
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

\section*{Mixed Integer Programming Model for DEC Computer Systems Production}

\textbf{Sets:}
\begin{itemize}
    \item $N$: Set of computer systems indexed by $i = 1, \ldots, N$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $is\_workstation_i \in \{0, 1\}$: Indicates if system $i$ is a workstation (1) or general-purpose (0).
    \item $price_i$: Price of system $i$ in dollars.
    \item $disk_i$: Average disk drives requested per system $i$.
    \item $mem_i$: Average 256K memory boards requested per system $i$.
    \item $max\_cpu$: Maximum available CPU units.
    \item $min\_disk$: Minimum available disk drives.
    \item $max\_disk$: Maximum available disk drives.
    \item $min\_mem$: Minimum available 256K memory boards.
    \item $max\_mem$: Maximum available 256K memory boards.
    \item $demand_i$: Maximum demand for system $i$.
    \item $demand\_GP$: Maximum demand for the general-purpose family.
    \item $demand\_WS$: Maximum demand for the workstation family.
    \item $preorder_i$: Preorders received for system $i$.
    \item $alt\_mem$: Available alternative memory boards.
    \item $alt\_compatible_i \in \{0, 1\}$: Indicates if system $i$ can use alternative memory.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: Number of system $i$ produced (continuous).
    \item $y_i$: Number of alternative memory boards used for system $i$ (integer).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{Costs}
\]

\textbf{Subject to:}
\begin{align*}
    & \sum_{i=1}^{N} x_i \leq max\_cpu & \text{(CPU constraint)} \\
    & \sum_{i=1}^{N} disk_i \cdot x_i \leq max\_disk & \text{(Disk drive constraint)} \\
    & \sum_{i=1}^{N} mem_i \cdot x_i + y_i \leq max\_mem & \text{(Memory constraint)} \\
    & \sum_{i=1}^{N} x_i \geq \sum_{i=1}^{N} preorder_i & \text{(Preorder fulfillment)} \\
    & x_i \leq demand_i & \forall i \in N & \text{(Demand constraint for each system)} \\
    & \sum_{i \text{ s.t. } is\_workstation_i} x_i \leq demand\_WS & \text{(Workstation demand)} \\
    & \sum_{i \text{ s.t. } is\_workstation_i=0} x_i \leq demand\_GP & \text{(GP demand)} \\
    & y_i \leq alt\_mem & \forall i \text{ where } alt\_compatible_i=1 & \text{(Alternative memory board allocation)} \\
    & x_i \geq preorder_i & \forall i \in N & \text{(Minimum production for preorders)} \\
    & x_i \geq 0 & \forall i \in N & \text{(Non-negativity)} \\
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item $system\_output$: List of produced systems with their respective board and drive usage.
    \item $profit$: Total profit for the next quarter.
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

#### Indices
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

#### Problem
problem = pulp.LpProblem("DEC_Production", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat=pulp.LpContinuous)
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat=pulp.LpInteger)

#### Objective function
problem += pulp.lpSum([price[i] * x[i] for i in range(N)])

#### Constraints
problem += pulp.lpSum([x[i] for i in range(N)]) <= max_cpu
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk
problem += pulp.lpSum([memory_boards[i] * x[i] + y[i] for i in range(N)]) <= max_memory
problem += pulp.lpSum([x[i] for i in range(N)]) >= pulp.lpSum([preorder[i] for i in range(N)])

for i in range(N):
    problem += x[i] <= demand[i]
    problem += x[i] >= preorder[i]
    if alt_compatible[i]:
        problem += y[i] <= alt_memory

problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_ws
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_gp

#### Solve
problem.solve()

#### Output
system_output = [(i, x[i].varValue, y[i].varValue) for i in range(N)]
profit = pulp.value(problem.objective)

print("System Output:", system_output)
print(f"Profit (Objective Value): <OBJ>{profit}</OBJ>")
```

