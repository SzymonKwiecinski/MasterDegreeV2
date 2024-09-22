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

\textbf{Indices:}
\begin{itemize}
    \item $i \in \{1, 2, \ldots, N\}$: index for the computer systems
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $is\_workstation[i]$: boolean indicating if system $i$ is a workstation
    \item $price[i]$: price of system $i$
    \item $disk\_drives[i]$: average disk drives requested for system $i$
    \item $mem[i]$: average 256K memory boards requested for system $i$
    \item $max\_cpu$: maximum number of CPUs available
    \item $min\_disk$: minimum available disk drives
    \item $max\_disk$: maximum available disk drives
    \item $min\_mem$: minimum available 256K memory boards
    \item $max\_mem$: maximum available 256K memory boards
    \item $demand[i]$: maximum demand for system $i$
    \item $demand\_GP$: maximum demand for the GP family
    \item $demand\_WS$: maximum demand for the WS family
    \item $preorder[i]$: preorders for system $i$
    \item $alt\_mem$: available alternative memory boards
    \item $alt\_compatible[i]$: boolean indicating if system $i$ can use alternative memory
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: number of systems produced of type $i$ (continuous)
    \item $y_i$: number of alternative memory boards used for system $i$ (integer)
\end{itemize}

\textbf{Objective Function:}
\begin{align}
    \text{Maximize } Z = \sum_{i=1}^{N} (price[i] \cdot x_i) - \text{Cost}(x_i, y_i)
\end{align}

\textbf{Constraints:}
\begin{align}
    \sum_{i=1}^{N} x_i & \leq max\_cpu \quad \text{(CPU constraint)} \\
    \sum_{i=1}^{N} disk\_drives[i] \cdot x_i & \geq min\_disk \quad \text{(minimum disk drives)} \\
    \sum_{i=1}^{N} disk\_drives[i] \cdot x_i & \leq max\_disk \quad \text{(maximum disk drives)} \\
    \sum_{i=1}^{N} mem[i] \cdot x_i + \sum_{i=1}^{N} y_i & \geq min\_mem \quad \text{(minimum memory boards)} \\
    \sum_{i=1}^{N} mem[i] \cdot x_i + \sum_{i=1}^{N} y_i & \leq max\_mem \quad \text{(maximum memory boards)} \\
    x_i & \geq preorder[i] \quad \forall i \quad \text{(meet preorders)} \\
    x_i & \leq demand[i] \quad \forall i \quad \text{(meet demand)} \\
    \sum_{i: is\_workstation[i]} x_i & \leq demand\_WS \quad \text{(workstation demand)} \\
    \sum_{i: \neg is\_workstation[i]} x_i & \leq demand\_GP \quad \text{(general-purpose demand)} \\
    y_i & \leq alt\_mem \cdot alt\_compatible[i] \quad \forall i \quad \text{(alternative memory constraint)}
\end{align}

\textbf{Output:}
The output will consist of a JSON object with:
\begin{itemize}
    \item "system\_output": containing a list of produced systems with details
    \item "profit": the total profit calculated from the objective function
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

\section*{Mathematical Model}

\textbf{Indices:}
\begin{itemize}
    \item $i \in \{1, 2, \ldots, N\}$: index for the computer systems
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $is\_workstation[i]$: boolean indicating if system $i$ is a workstation
    \item $price[i]$: price of system $i$
    \item $disk\_drives[i]$: average disk drives requested for system $i$
    \item $mem[i]$: average 256K memory boards requested for system $i$
    \item $max\_cpu$: maximum number of CPUs available
    \item $min\_disk$: minimum available disk drives
    \item $max\_disk$: maximum available disk drives
    \item $min\_mem$: minimum available 256K memory boards
    \item $max\_mem$: maximum available 256K memory boards
    \item $demand[i]$: maximum demand for system $i$
    \item $demand\_GP$: maximum demand for the GP family
    \item $demand\_WS$: maximum demand for the WS family
    \item $preorder[i]$: preorders for system $i$
    \item $alt\_mem$: available alternative memory boards
    \item $alt\_compatible[i]$: boolean indicating if system $i$ can use alternative memory
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: number of systems produced of type $i$ (continuous)
    \item $y_i$: number of alternative memory boards used for system $i$ (integer)
\end{itemize}

\textbf{Objective Function:}
\begin{align}
    \text{Maximize } Z = \sum_{i=1}^{N} (price[i] \cdot x_i) - \text{Cost}(x_i, y_i)
\end{align}

\textbf{Constraints:}
\begin{align}
    \sum_{i=1}^{N} x_i & \leq max\_cpu \quad \text{(CPU constraint)} \\
    \sum_{i=1}^{N} disk\_drives[i] \cdot x_i & \geq min\_disk \quad \text{(minimum disk drives)} \\
    \sum_{i=1}^{N} disk\_drives[i] \cdot x_i & \leq max\_disk \quad \text{(maximum disk drives)} \\
    \sum_{i=1}^{N} mem[i] \cdot x_i + \sum_{i=1}^{N} y_i & \geq min\_mem \quad \text{(minimum memory boards)} \\
    \sum_{i=1}^{N} mem[i] \cdot x_i + \sum_{i=1}^{N} y_i & \leq max\_mem \quad \text{(maximum memory boards)} \\
    x_i & \geq preorder[i] \quad \forall i \quad \text{(meet preorders)} \\
    x_i & \leq demand[i] \quad \forall i \quad \text{(meet demand)} \\
    \sum_{i: is\_workstation[i]} x_i & \leq demand\_WS \quad \text{(workstation demand)} \\
    \sum_{i: \neg is\_workstation[i]} x_i & \leq demand\_GP \quad \text{(general-purpose demand)} \\
    y_i & \leq alt\_mem \cdot alt\_compatible[i] \quad \forall i \quad \text{(alternative memory constraint)}
\end{align}

\textbf{Output:}
The output will consist of a JSON object with:
\begin{itemize}
    \item "system\_output": containing a list of produced systems with details
    \item "profit": the total profit calculated from the objective function
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from provided JSON
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

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
mem = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_memory = data['AltMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
alt_compatible = data['AltCompatible']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  #### number of systems produced (continuous)
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')  #### number of alternative memory boards used (integer)

#### Objective Function
profit_expression = pulp.lpSum(price[i] * x[i] for i in range(N)) - pulp.lpSum(y[i] for i in range(N))
problem += profit_expression

#### Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu, "CPU_constraint"
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) >= min_disk, "Min_disk_drives"
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) <= max_disk, "Max_disk_drives"
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) + pulp.lpSum(y[i] for i in range(N)) >= min_mem, "Min_memory_boards"
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) + pulp.lpSum(y[i] for i in range(N)) <= max_mem, "Max_memory_boards"
for i in range(N):
    problem += x[i] >= preorder[i], f"Preorder_constraint_{i}"
    problem += x[i] <= demand[i], f"Demand_constraint_{i}"
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_WS, "Workstation_demand"
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_GP, "General_purpose_demand"
for i in range(N):
    problem += y[i] <= alt_memory * alt_compatible[i], f"Alt_memory_constraint_{i}"

#### Solve the problem
problem.solve()

#### Output the results
system_output = [{"system_id": i, "produced": pulp.value(x[i]), "alt_memory_used": pulp.value(y[i])} for i in range(N)]
profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{profit}</OBJ>')
```

