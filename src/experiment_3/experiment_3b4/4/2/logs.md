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
To model the given problem as a Mixed-Integer Programming (MIP) problem, we need to define decision variables, constraints, and an objective function in a mathematical form. Below is the formulation in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mixed-Integer Programming Model for DEC}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of different computer systems.
    \item $\text{price}_i$: Price of system $i$ in dollars.
    \item $\text{disk}_i$: Average number of disk drives requested for system $i$.
    \item $\text{mem}_i$: Average number of 256K memory boards used in system $i$.
    \item $\text{max\_cpu}$: Maximum number of CPUs available.
    \item $\text{min\_disk}$, $\text{max\_disk}$: Range of available disk drives.
    \item $\text{min\_mem}$, $\text{max\_mem}$: Range of available 256K memory boards.
    \item $\text{demand}_i$: Maximum demand for system $i$.
    \item $\text{demand\_GP}$: Maximum demand for the GP family.
    \item $\text{demand\_WS}$: Maximum demand for the WS family.
    \item $\text{preorder}_i$: Preorder for system $i$.
    \item $\text{alt\_mem}$: Units of alternative memory boards available.
    \item $\text{is\_workstation}_i$: Indicator if system $i$ is a workstation (\text{true}/\text{false}).
    \item $\text{alt\_compatible}_i$: Indicator if system $i$ can use alternative memory boards (\text{true}/\text{false}).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems of type $i$ to produce.
    \item $y_i$: Number of 256K memory boards used in system $i$.
    \item $z_i$: Number of alternative memory boards used in system $i$.
    \item $d_i$: Number of disk drives used in system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}
\begin{align}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} \quad &\text{(CPU constraint)}\\
    & \sum_{i=1}^{N} d_i \geq \text{min\_disk}, \quad \sum_{i=1}^{N} d_i \leq \text{max\_disk} \quad &\text{(Disk supply constraint)}\\
    & \sum_{i=1}^{N} y_i \geq \text{min\_mem}, \quad \sum_{i=1}^{N} y_i \leq \text{max\_mem} \quad &\text{(256K Memory supply constraint)}\\
    & \sum_{i=1}^{N} z_i \leq \text{alt\_mem} \quad &\text{(Alternative memory constraint)}\\
    & y_i + z_i \geq \text{mem}_i \cdot x_i \quad &\text{(Memory requirement per system)}\\
    & d_i \geq \text{disk}_i \cdot x_i \quad &\text{(Disk requirement per system)}\\
    & x_i \leq \text{demand}_i \quad &\text{(Individual system demand constraint)}\\
    & \sum_{i \text{ is GP}} x_i \leq \text{demand\_GP} \quad &\text{(GP family demand constraint)}\\
    & \sum_{i \text{ is WS}} x_i \leq \text{demand\_WS} \quad &\text{(WS family demand constraint)}\\
    & x_i \geq \text{preorder}_i \quad &\text{(Preorder fulfillment)}\\
    & z_i = 0 \quad \text{if } \text{alt\_compatible}_i \text{ is false} \quad &\text{(Alternative memory compatibility)}\\
    & x_i \geq 0, \quad y_i \geq 0, \quad z_i \geq 0, \quad d_i \geq 0 \quad &\text{(Non-negativity constraints)}
\end{align}

In this formulation, we maximize the total profit from selling the computer systems while satisfying constraints on resources, demands, and preorders. The constraints ensure that limited resources such as CPUs, memory boards, and disk drives are allocated efficiently, and orders are fulfilled as required.

\end{document}
```

This LaTeX code accurately represents the Mixed-Integer Linear Programming problem, capturing all the details from the problem description.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mixed-Integer Programming Model for DEC}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of different computer systems.
    \item $\text{price}_i$: Price of system $i$ in dollars.
    \item $\text{disk}_i$: Average number of disk drives requested for system $i$.
    \item $\text{mem}_i$: Average number of 256K memory boards used in system $i$.
    \item $\text{max\_cpu}$: Maximum number of CPUs available.
    \item $\text{min\_disk}$, $\text{max\_disk}$: Range of available disk drives.
    \item $\text{min\_mem}$, $\text{max\_mem}$: Range of available 256K memory boards.
    \item $\text{demand}_i$: Maximum demand for system $i$.
    \item $\text{demand\_GP}$: Maximum demand for the GP family.
    \item $\text{demand\_WS}$: Maximum demand for the WS family.
    \item $\text{preorder}_i$: Preorder for system $i$.
    \item $\text{alt\_mem}$: Units of alternative memory boards available.
    \item $\text{is\_workstation}_i$: Indicator if system $i$ is a workstation (\text{true}/\text{false}).
    \item $\text{alt\_compatible}_i$: Indicator if system $i$ can use alternative memory boards (\text{true}/\text{false}).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems of type $i$ to produce.
    \item $y_i$: Number of 256K memory boards used in system $i$.
    \item $z_i$: Number of alternative memory boards used in system $i$.
    \item $d_i$: Number of disk drives used in system $i$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}
\begin{align}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} \quad &\text{(CPU constraint)}\\
    & \sum_{i=1}^{N} d_i \geq \text{min\_disk}, \quad \sum_{i=1}^{N} d_i \leq \text{max\_disk} \quad &\text{(Disk supply constraint)}\\
    & \sum_{i=1}^{N} y_i \geq \text{min\_mem}, \quad \sum_{i=1}^{N} y_i \leq \text{max\_mem} \quad &\text{(256K Memory supply constraint)}\\
    & \sum_{i=1}^{N} z_i \leq \text{alt\_mem} \quad &\text{(Alternative memory constraint)}\\
    & y_i + z_i \geq \text{mem}_i \cdot x_i \quad &\text{(Memory requirement per system)}\\
    & d_i \geq \text{disk}_i \cdot x_i \quad &\text{(Disk requirement per system)}\\
    & x_i \leq \text{demand}_i \quad &\text{(Individual system demand constraint)}\\
    & \sum_{i \text{ is GP}} x_i \leq \text{demand\_GP} \quad &\text{(GP family demand constraint)}\\
    & \sum_{i \text{ is WS}} x_i \leq \text{demand\_WS} \quad &\text{(WS family demand constraint)}\\
    & x_i \geq \text{preorder}_i \quad &\text{(Preorder fulfillment)}\\
    & z_i = 0 \quad \text{if } \text{alt\_compatible}_i \text{ is false} \quad &\text{(Alternative memory compatibility)}\\
    & x_i \geq 0, \quad y_i \geq 0, \quad z_i \geq 0, \quad d_i \geq 0 \quad &\text{(Non-negativity constraints)}
\end{align}

In this formulation, we maximize the total profit from selling the computer systems while satisfying constraints on resources, demands, and preorders. The constraints ensure that limited resources such as CPUs, memory boards, and disk drives are allocated efficiently, and orders are fulfilled as required.

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
GP_indices = [i for i in range(N) if not data['IsWorkstation'][i]]
WS_indices = [i for i in range(N) if data['IsWorkstation'][i]]

#### Problem
problem = pulp.LpProblem("Mixed_Integer_Programming_for_DEC", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') for i in range(N)]
z = [pulp.LpVariable(f'z_{i}', lowBound=0, cat='Continuous') for i in range(N)]
d = [pulp.LpVariable(f'd_{i}', lowBound=0, cat='Continuous') for i in range(N)]

#### Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(N))

#### Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= data['MaxCpu'], "CPU_constraint"
problem += pulp.lpSum(d[i] for i in range(N)) >= data['MinDisk'], "Min_Disk_supply_constraint"
problem += pulp.lpSum(d[i] for i in range(N)) <= data['MaxDisk'], "Max_Disk_supply_constraint"
problem += pulp.lpSum(y[i] for i in range(N)) >= data['MinMemory'], "Min_256K_Memory_supply_constraint"
problem += pulp.lpSum(y[i] for i in range(N)) <= data['MaxMemory'], "Max_256K_Memory_supply_constraint"
problem += pulp.lpSum(z[i] for i in range(N)) <= data['AltMemory'], "Alternative_memory_constraint"

for i in range(N):
    problem += y[i] + z[i] >= data['MemoryBoards'][i] * x[i], f"Memory_requirement_system_{i}"
    problem += d[i] >= data['DiskDrives'][i] * x[i], f"Disk_requirement_system_{i}"
    problem += x[i] <= data['Demand'][i], f"Individual_system_demand_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_fulfillment_{i}"
    if not data['AltCompatible'][i]:
        problem += z[i] == 0, f"Alternative_memory_compatibility_{i}"

problem += pulp.lpSum(x[i] for i in GP_indices) <= data['DemandGP'], "GP_family_demand_constraint"
problem += pulp.lpSum(x[i] for i in WS_indices) <= data['DemandWS'], "WS_family_demand_constraint"

#### Solve Problem
problem.solve()

#### Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


