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

\section*{Mathematical Model for DEC System Production}

\subsection*{Sets}
\begin{itemize}
    \item Let \( N \) = number of different computer systems.
    \item Let \( i \in \{1, 2, \ldots, N\} \) denote each computer system.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{is\_workstation}_i \): boolean indicating if system \( i \) is a workstation.
    \item \( \text{price}_i \): price of system \( i \) (in dollars).
    \item \( \text{disk\_drives}_i \): average number of disk drives requested by customers for system \( i \).
    \item \( \text{256K\_boards}_i \): average number of 256K memory boards used by system \( i \).
    \item \( \text{max\_cpu} \): maximum number of CPUs available.
    \item \( \text{min\_disk} \): minimum number of disk drives available.
    \item \( \text{max\_disk} \): maximum number of disk drives available.
    \item \( \text{min\_mem} \): minimum number of 256K memory boards available.
    \item \( \text{max\_mem} \): maximum number of 256K memory boards available.
    \item \( \text{demand}_i \): maximum demand for system \( i \).
    \item \( \text{demand\_GP} \): maximum demand for the whole GP family.
    \item \( \text{demand\_WS} \): maximum demand for the whole WS family.
    \item \( \text{preorder}_i \): preorder units for system \( i \).
    \item \( \text{alt\_mem} \): units of alternative memory board available.
    \item \( \text{alt\_compatible}_i \): boolean indicating if system \( i \) is compatible with alternative memory.
\end{itemize}

\subsection*{Decision Variables}
Let:
\[
x_i = \text{number of systems produced for system } i
\]
\[
y_i = \text{number of alternative memory boards used for system } i
\]

\subsection*{Objective Function}
Maximize profit:
\[
\text{Profit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \text{cost\_of\_components}
\]

\subsection*{Constraints}
\begin{itemize}
    \item \text{CPU constraint:}
    \[
    \sum_{i=1}^{N} x_i \leq \text{max\_cpu}
    \]

    \item \text{Disk drives constraint:}
    \[
    \sum_{i=1}^{N} \text{disk\_drives}_i \cdot x_i \leq \text{max\_disk}
    \]
    
    \item \text{Memory boards constraints:}
    \[
    \sum_{i=1}^{N} \text{256K\_boards}_i \cdot x_i + \sum_{i=1}^{N} y_i \leq \text{max\_mem}
    \]
    \[
    \sum_{i=1}^{N} y_i \leq \text{alt\_mem}  \quad \text{(if } \text{alt\_compatible}_i \text{ is true)}
    \]

    \item \text{Demand constraints:}
    \[
    x_i \geq \text{preorder}_i \quad \forall i
    \]
    \[
    \sum_{i \in \text{GP}} x_i \leq \text{demand\_GP}
    \]
    \[
    \sum_{i \in \text{WS}} x_i \leq \text{demand\_WS}
    \]
    \[
    x_i \leq \text{demand}_i \quad \forall i
    \]

    \item \text{Non-negativity:}
    \[
    x_i \geq 0 \quad \forall i
    \]
    \[
    y_i \geq 0 \quad \forall i \text{ if } \text{alt\_compatible}_i = \text{true}
    \]
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

\section*{Mathematical Model for DEC System Production}

\subsection*{Sets}
\begin{itemize}
    \item Let \( N \) = number of different computer systems.
    \item Let \( i \in \{1, 2, \ldots, N\} \) denote each computer system.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{is\_workstation}_i \): boolean indicating if system \( i \) is a workstation.
    \item \( \text{price}_i \): price of system \( i \) (in dollars).
    \item \( \text{disk\_drives}_i \): average number of disk drives requested by customers for system \( i \).
    \item \( \text{256K\_boards}_i \): average number of 256K memory boards used by system \( i \).
    \item \( \text{max\_cpu} \): maximum number of CPUs available.
    \item \( \text{min\_disk} \): minimum number of disk drives available.
    \item \( \text{max\_disk} \): maximum number of disk drives available.
    \item \( \text{min\_mem} \): minimum number of 256K memory boards available.
    \item \( \text{max\_mem} \): maximum number of 256K memory boards available.
    \item \( \text{demand}_i \): maximum demand for system \( i \).
    \item \( \text{demand\_GP} \): maximum demand for the whole GP family.
    \item \( \text{demand\_WS} \): maximum demand for the whole WS family.
    \item \( \text{preorder}_i \): preorder units for system \( i \).
    \item \( \text{alt\_mem} \): units of alternative memory board available.
    \item \( \text{alt\_compatible}_i \): boolean indicating if system \( i \) is compatible with alternative memory.
\end{itemize}

\subsection*{Decision Variables}
Let:
\[
x_i = \text{number of systems produced for system } i
\]
\[
y_i = \text{number of alternative memory boards used for system } i
\]

\subsection*{Objective Function}
Maximize profit:
\[
\text{Profit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \text{cost\_of\_components}
\]

\subsection*{Constraints}
\begin{itemize}
    \item \text{CPU constraint:}
    \[
    \sum_{i=1}^{N} x_i \leq \text{max\_cpu}
    \]

    \item \text{Disk drives constraint:}
    \[
    \sum_{i=1}^{N} \text{disk\_drives}_i \cdot x_i \leq \text{max\_disk}
    \]
    
    \item \text{Memory boards constraints:}
    \[
    \sum_{i=1}^{N} \text{256K\_boards}_i \cdot x_i + \sum_{i=1}^{N} y_i \leq \text{max\_mem}
    \]
    \[
    \sum_{i=1}^{N} y_i \leq \text{alt\_mem}  \quad \text{(if } \text{alt\_compatible}_i \text{ is true)}
    \]

    \item \text{Demand constraints:}
    \[
    x_i \geq \text{preorder}_i \quad \forall i
    \]
    \[
    \sum_{i \in \text{GP}} x_i \leq \text{demand\_GP}
    \]
    \[
    \sum_{i \in \text{WS}} x_i \leq \text{demand\_WS}
    \]
    \[
    x_i \leq \text{demand}_i \quad \forall i
    \]

    \item \text{Non-negativity:}
    \[
    x_i \geq 0 \quad \forall i
    \]
    \[
    y_i \geq 0 \quad \forall i \text{ if } \text{alt\_compatible}_i = \text{true}
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
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
problem = pulp.LpProblem("DEC_System_Production", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') if data['AltCompatible'][i] else 0 for i in range(data['N'])]

#### Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N']) if data['AltCompatible'][i]) <= data['MaxMemory'], "Memory_Constraint"
problem += pulp.lpSum(y[i] for i in range(data['N']) if data['AltCompatible'][i]) <= data['AltMemory'], "Alt_Memory_Constraint"

#### Demand constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

