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
To model this problem using Mixed Integer Programming (MIP), we will define decision variables for the number of systems produced, the usage of regular memory boards, and the usage of alternative memory boards. The objective is to maximize the total profit, subject to constraints on resource availability, preorder fulfillment, and demand limitations. Here's the mathematical formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $N$: Number of systems.
    \item $i$: Index for each system, $i = 1, \ldots, N$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{is\_workstation}_i$: Boolean, 1 if system $i$ is a workstation, 0 otherwise.
    \item $\text{price}_i$: Price of system $i$.
    \item \text{disk\_drives}_i$: Average disk drives required for system $i$.
    \item \text{mem}_i$: Average 256K memory boards required for system $i$.
    \item $\text{max\_cpu}$: Maximum number of CPUs available.
    \item $\text{min\_disk}$, $\text{max\_disk}$: Min and max disk drives available.
    \item $\text{min\_mem}$, $\text{max\_mem}$: Min and max 256K memory boards available.
    \item $\text{demand}_i$: Maximum demand for system $i$.
    \item $\text{demand\_GP}$: Maximum demand for GP family.
    \item $\text{demand\_WS}$: Maximum demand for WS family.
    \item $\text{preorder}_i$: Preorders for system $i$.
    \item $\text{alt\_mem}$: Alternate memory boards available.
    \item $\text{alt\_compatible}_i$: Boolean, 1 if system $i$ can use alternative memory board, 0 otherwise.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems $i$ produced (continuous variable).
    \item $m_i$: Number of 256K memory boards used for system $i$ (continuous variable).
    \item $a_i$: Number of alternative memory boards used for system $i$ (continuous variable).
    \item $d_i$: Number of disk drives used for system $i$ (continuous variable).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}
\begin{align}
    \sum_{i=1}^{N} x_i &\leq \text{max\_cpu} & \text{(CPU constraint)}\\
    \sum_{i=1}^{N} d_i &\leq \text{max\_disk} & \text{(Max disk constraint)}\\
    \sum_{i=1}^{N} d_i &\geq \text{min\_disk} & \text{(Min disk constraint)}\\
    \sum_{i=1}^{N} m_i &\leq \text{max\_mem} & \text{(Max 256K memory constraint)}\\
    \sum_{i=1}^{N} m_i &\geq \text{min\_mem} & \text{(Min 256K memory constraint)}\\
    \sum_{i=1}^{N} a_i &\leq \text{alt\_mem} & \text{(Alternative memory constraint)}\\
    m_i + a_i &= \text{mem}_i \cdot x_i, & \forall i \\
    d_i &= \text{disk\_drives}_i \cdot x_i, & \forall i \\
    x_i &\leq \text{demand}_i, & \forall i \\
    x_i &\geq \text{preorder}_i, & \forall i \\
    \sum_{i:\text{is\_workstation}_i = 0} x_i &\leq \text{demand\_GP} & \text{(GP system constraint)} \\
    \sum_{i:\text{is\_workstation}_i = 1} x_i &\leq \text{demand\_WS} & \text{(WS system constraint)} \\
    a_i &\leq \text{alt\_compatible}_i \cdot x_i, & \forall i
\end{align}

\end{document}
```

This linear programming model considers resource constraints, preorder fulfilment, and demand satisfaction while seeking to maximize profit. The decision variables are continuous, which reflects the assumption that the production numbers can be fractional.

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
    \item $N$: Number of systems.
    \item $i$: Index for each system, $i = 1, \ldots, N$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{is\_workstation}_i$: Boolean, 1 if system $i$ is a workstation, 0 otherwise.
    \item $\text{price}_i$: Price of system $i$.
    \item \text{disk\_drives}_i$: Average disk drives required for system $i$.
    \item \text{mem}_i$: Average 256K memory boards required for system $i$.
    \item $\text{max\_cpu}$: Maximum number of CPUs available.
    \item $\text{min\_disk}$, $\text{max\_disk}$: Min and max disk drives available.
    \item $\text{min\_mem}$, $\text{max\_mem}$: Min and max 256K memory boards available.
    \item $\text{demand}_i$: Maximum demand for system $i$.
    \item $\text{demand\_GP}$: Maximum demand for GP family.
    \item $\text{demand\_WS}$: Maximum demand for WS family.
    \item $\text{preorder}_i$: Preorders for system $i$.
    \item $\text{alt\_mem}$: Alternate memory boards available.
    \item $\text{alt\_compatible}_i$: Boolean, 1 if system $i$ can use alternative memory board, 0 otherwise.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems $i$ produced (continuous variable).
    \item $m_i$: Number of 256K memory boards used for system $i$ (continuous variable).
    \item $a_i$: Number of alternative memory boards used for system $i$ (continuous variable).
    \item $d_i$: Number of disk drives used for system $i$ (continuous variable).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \cdot x_i
\]

\subsection*{Constraints}
\begin{align}
    \sum_{i=1}^{N} x_i &\leq \text{max\_cpu} & \text{(CPU constraint)}\\
    \sum_{i=1}^{N} d_i &\leq \text{max\_disk} & \text{(Max disk constraint)}\\
    \sum_{i=1}^{N} d_i &\geq \text{min\_disk} & \text{(Min disk constraint)}\\
    \sum_{i=1}^{N} m_i &\leq \text{max\_mem} & \text{(Max 256K memory constraint)}\\
    \sum_{i=1}^{N} m_i &\geq \text{min\_mem} & \text{(Min 256K memory constraint)}\\
    \sum_{i=1}^{N} a_i &\leq \text{alt\_mem} & \text{(Alternative memory constraint)}\\
    m_i + a_i &= \text{mem}_i \cdot x_i, & \forall i \\
    d_i &= \text{disk\_drives}_i \cdot x_i, & \forall i \\
    x_i &\leq \text{demand}_i, & \forall i \\
    x_i &\geq \text{preorder}_i, & \forall i \\
    \sum_{i:\text{is\_workstation}_i = 0} x_i &\leq \text{demand\_GP} & \text{(GP system constraint)} \\
    \sum_{i:\text{is\_workstation}_i = 1} x_i &\leq \text{demand\_WS} & \text{(WS system constraint)} \\
    a_i &\leq \text{alt\_compatible}_i \cdot x_i, & \forall i
\end{align}

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

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
m = [pulp.LpVariable(f"m_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
a = [pulp.LpVariable(f"a_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
d = [pulp.LpVariable(f"d_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

#### Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total Profit"

#### Constraints
#### CPU constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU Constraint"

#### Disk constraints
problem += pulp.lpSum(d[i] for i in range(data['N'])) <= data['MaxDisk'], "Max Disk Constraint"
problem += pulp.lpSum(d[i] for i in range(data['N'])) >= data['MinDisk'], "Min Disk Constraint"

#### Memory constraints
problem += pulp.lpSum(m[i] for i in range(data['N'])) <= data['MaxMemory'], "Max 256K Memory Constraint"
problem += pulp.lpSum(m[i] for i in range(data['N'])) >= data['MinMemory'], "Min 256K Memory Constraint"

#### Alternative memory constraint
problem += pulp.lpSum(a[i] for i in range(data['N'])) <= data['AltMemory'], "Alternative Memory Constraint"

#### Memory and disk drives requirements
for i in range(data['N']):
    problem += m[i] + a[i] == data['MemoryBoards'][i] * x[i], f"Memory Requirement for System {i}"
    problem += d[i] == data['DiskDrives'][i] * x[i], f"Disk Requirement for System {i}"

#### Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Max Demand for System {i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder Demand for System {i}"

#### GP and WS constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP System Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS System Constraint"

#### Alternative compatibility constraint
for i in range(data['N']):
    problem += a[i] <= data['AltCompatible'][i] * x[i], f"Alt Memory Compatibility for System {i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

