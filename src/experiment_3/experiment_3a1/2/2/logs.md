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

\subsection*{Sets}
\begin{itemize}
    \item $N$: Number of computer systems
    \item $i$: Index for each system, $i = 1, \ldots, N$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $is\_workstation_i \in \{0, 1\}$: Indicator for if system $i$ is a workstation
    \item $price_i$: Price of system $i$ in dollars
    \item $disk_i$: Average number of disk drives requested by customers for system $i$
    \item $mem_i$: Average number of 256K memory boards requested by customers for system $i$
    \item $max\_cpu$: Maximum number of CPUs available
    \item $min\_disk$: Minimum supply of disk drives
    \item $max\_disk$: Maximum supply of disk drives
    \item $min\_mem$: Minimum supply of 256K memory boards
    \item $max\_mem$: Maximum supply of 256K memory boards
    \item $demand_i$: Maximum demand for system $i$
    \item $demand\_GP$: Maximum demand for the whole GP family
    \item $demand\_WS$: Maximum demand for the whole WS family
    \item $preorder_i$: Preorders received for system $i$
    \item $alt\_mem$: Available alternative memory boards
    \item $alt\_compatible_i \in \{0, 1\}$: Indicator if alternative memory can be used in system $i$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems $i$ to produce
    \item $alt\_used_i$: Number of alternative memory boards used in system $i$
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{Costs}
\]

\subsection*{Constraints}
1. CPU constraint:
\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drive supply limit:
\[
\sum_{i=1}^{N} disk_i \cdot x_i \geq min\_disk
\]
\[
\sum_{i=1}^{N} disk_i \cdot x_i \leq max\_disk
\]

3. Memory board supply limit:
\[
\sum_{i=1}^{N} mem_i \cdot x_i + \sum_{i=1}^{N} alt\_used_i \leq max\_mem
\]
\[
\sum_{i=1}^{N} mem_i \cdot x_i + \sum_{i=1}^{N} alt\_used_i \geq min\_mem
\]

4. Demand constraints for each system:
\[
x_i \leq demand_i \quad \forall i
\]

5. Demand constraints for GP and WS:
\[
\sum_{i: is\_workstation_i=0} x_i \leq demand\_GP
\]
\[
\sum_{i: is\_workstation_i=1} x_i \leq demand\_WS
\]

6. Preorder fulfillment:
\[
x_i \geq preorder_i \quad \forall i
\]

7. Alternative memory board usage:
\[
alt\_used_i \leq alt\_mem \cdot alt\_compatible_i \quad \forall i
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

\section*{Mathematical Model for DEC Production Problem}

\subsection*{Sets}
\begin{itemize}
    \item $N$: Number of computer systems
    \item $i$: Index for each system, $i = 1, \ldots, N$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $is\_workstation_i \in \{0, 1\}$: Indicator for if system $i$ is a workstation
    \item $price_i$: Price of system $i$ in dollars
    \item $disk_i$: Average number of disk drives requested by customers for system $i$
    \item $mem_i$: Average number of 256K memory boards requested by customers for system $i$
    \item $max\_cpu$: Maximum number of CPUs available
    \item $min\_disk$: Minimum supply of disk drives
    \item $max\_disk$: Maximum supply of disk drives
    \item $min\_mem$: Minimum supply of 256K memory boards
    \item $max\_mem$: Maximum supply of 256K memory boards
    \item $demand_i$: Maximum demand for system $i$
    \item $demand\_GP$: Maximum demand for the whole GP family
    \item $demand\_WS$: Maximum demand for the whole WS family
    \item $preorder_i$: Preorders received for system $i$
    \item $alt\_mem$: Available alternative memory boards
    \item $alt\_compatible_i \in \{0, 1\}$: Indicator if alternative memory can be used in system $i$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of systems $i$ to produce
    \item $alt\_used_i$: Number of alternative memory boards used in system $i$
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{Costs}
\]

\subsection*{Constraints}
1. CPU constraint:
\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drive supply limit:
\[
\sum_{i=1}^{N} disk_i \cdot x_i \geq min\_disk
\]
\[
\sum_{i=1}^{N} disk_i \cdot x_i \leq max\_disk
\]

3. Memory board supply limit:
\[
\sum_{i=1}^{N} mem_i \cdot x_i + \sum_{i=1}^{N} alt\_used_i \leq max\_mem
\]
\[
\sum_{i=1}^{N} mem_i \cdot x_i + \sum_{i=1}^{N} alt\_used_i \geq min\_mem
\]

4. Demand constraints for each system:
\[
x_i \leq demand_i \quad \forall i
\]

5. Demand constraints for GP and WS:
\[
\sum_{i: is\_workstation_i=0} x_i \leq demand\_GP
\]
\[
\sum_{i: is\_workstation_i=1} x_i \leq demand\_WS
\]

6. Preorder fulfillment:
\[
x_i \geq preorder_i \quad \forall i
\]

7. Alternative memory board usage:
\[
alt\_used_i \leq alt\_mem \cdot alt\_compatible_i \quad \forall i
\]

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

#### Create the problem instance
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0, cat='Integer')

#### Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"

#### Demand constraints for each system
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

#### Demand constraints for GP and WS
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"

#### Preorder fulfillment
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_{i}"

#### Alternative memory board usage
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += alt_used[i] <= data['AltMemory'], f"Alt_Memory_Usage_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

