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

\subsection*{Parameters}

\begin{itemize}
    \item \(N\): Number of computer systems.
    \item \(is\_workstation_i\): Boolean indicating if system \(i\) is a workstation (WS).
    \item \(price_i\): Price of system \(i\).
    \item \(disk_i\): Average number of disk drives required for system \(i\).
    \item \(mem_i\): Number of 256K memory boards required for system \(i\).
    \item \(max\_cpu\): Maximum number of CPUs available for production.
    \item \(min\_disk\): Minimum supply of disk drives.
    \item \(max\_disk\): Maximum supply of disk drives.
    \item \(min\_mem\): Minimum supply of 256K memory boards.
    \item \(max\_mem\): Maximum supply of 256K memory boards.
    \item \(demand_i\): Maximum demand for system \(i\).
    \item \(demand\_GP\): Maximum demand for the GP family.
    \item \(demand\_WS\): Maximum demand for the WS family.
    \item \(preorder_i\): Preorders for system \(i\) that must be fulfilled.
    \item \(alt\_mem\): Number of alternative memory boards available.
    \item \(alt\_compatible_i\): Boolean indicating if system \(i\) can use alternative memory boards.
\end{itemize}

\subsection*{Decision Variables}

Let \(x_i\) be the number of system \(i\) produced. Define:
\begin{itemize}
    \item \(y_i\): Number of 256K memory boards used for system \(i\).
    \item \(z_i\): Number of alternative memory boards used for system \(i\).
    \item \(d_i\): Number of disk drives used for system \(i\).
\end{itemize}

\subsection*{Objective Function}

Maximize the profit:
\[
\text{Maximize } Z = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{cost\_of\_boards} - \text{cost\_of\_drives}
\]

\subsection*{Constraints}

1. CPU constraint:
\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drives constraints:
\[
\sum_{i=1}^{N} d_i \cdot x_i \in [min\_disk, max\_disk]
\]

3. Memory constraints:
\[
\sum_{i=1}^{N} mem_i \cdot x_i + z_i \leq max\_mem
\]
\[
z_i \leq alt\_mem \text{ for } alt\_compatible_i = \text{true}
\]

4. Demand constraints for systems:
\[
preorder_i + x_i \leq demand_i \quad \forall i
\]

5. GP Family Demand Constraint:
\[
\sum_{i: is\_workstation_i = \text{false}} x_i \leq demand\_GP
\]

6. WS Family Demand Constraint:
\[
\sum_{i: is\_workstation_i = \text{true}} x_i \leq demand\_WS
\]

\subsection*{Output}

The output will be given in a JSON format:
\[
\{
    "system\_output": [
        \{
            "num\_produced": x_i,
            "total\_256K\_boards\_used": mem\_used_i,
            "total\_alt\_boards\_used": alt\_used_i,
            "total\_disk\_drives\_used": disk\_used_i
        \} \text{ for } i = 1, \ldots, T
    ],
    "profit": Z
\}
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

\subsection*{Parameters}

\begin{itemize}
    \item \(N\): Number of computer systems.
    \item \(is\_workstation_i\): Boolean indicating if system \(i\) is a workstation (WS).
    \item \(price_i\): Price of system \(i\).
    \item \(disk_i\): Average number of disk drives required for system \(i\).
    \item \(mem_i\): Number of 256K memory boards required for system \(i\).
    \item \(max\_cpu\): Maximum number of CPUs available for production.
    \item \(min\_disk\): Minimum supply of disk drives.
    \item \(max\_disk\): Maximum supply of disk drives.
    \item \(min\_mem\): Minimum supply of 256K memory boards.
    \item \(max\_mem\): Maximum supply of 256K memory boards.
    \item \(demand_i\): Maximum demand for system \(i\).
    \item \(demand\_GP\): Maximum demand for the GP family.
    \item \(demand\_WS\): Maximum demand for the WS family.
    \item \(preorder_i\): Preorders for system \(i\) that must be fulfilled.
    \item \(alt\_mem\): Number of alternative memory boards available.
    \item \(alt\_compatible_i\): Boolean indicating if system \(i\) can use alternative memory boards.
\end{itemize}

\subsection*{Decision Variables}

Let \(x_i\) be the number of system \(i\) produced. Define:
\begin{itemize}
    \item \(y_i\): Number of 256K memory boards used for system \(i\).
    \item \(z_i\): Number of alternative memory boards used for system \(i\).
    \item \(d_i\): Number of disk drives used for system \(i\).
\end{itemize}

\subsection*{Objective Function}

Maximize the profit:
\[
\text{Maximize } Z = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{cost\_of\_boards} - \text{cost\_of\_drives}
\]

\subsection*{Constraints}

1. CPU constraint:
\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drives constraints:
\[
\sum_{i=1}^{N} d_i \cdot x_i \in [min\_disk, max\_disk]
\]

3. Memory constraints:
\[
\sum_{i=1}^{N} mem_i \cdot x_i + z_i \leq max\_mem
\]
\[
z_i \leq alt\_mem \text{ for } alt\_compatible_i = \text{true}
\]

4. Demand constraints for systems:
\[
preorder_i + x_i \leq demand_i \quad \forall i
\]

5. GP Family Demand Constraint:
\[
\sum_{i: is\_workstation_i = \text{false}} x_i \leq demand\_GP
\]

6. WS Family Demand Constraint:
\[
\sum_{i: is\_workstation_i = \text{true}} x_i \leq demand\_WS
\]

\subsection*{Output}

The output will be given in a JSON format:
\[
\{
    "system\_output": [
        \{
            "num\_produced": x_i,
            "total\_256K\_boards\_used": mem\_used_i,
            "total\_alt\_boards\_used": alt\_used_i,
            "total\_disk\_drives\_used": disk\_used_i
        \} \text{ for } i = 1, \ldots, T
    ],
    "profit": Z
\}
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
max_mem = data['MaxMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
alt_mem = data['AltMemory']

#### Define the problem
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

#### Decision variables
x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(N)]
y_vars = [pulp.LpVariable(f"y_{i}", lowBound=0, cat='Integer') for i in range(N)]
z_vars = [pulp.LpVariable(f"z_{i}", lowBound=0, cat='Integer') for i in range(N)]
d_vars = [pulp.LpVariable(f"d_{i}", lowBound=0) for i in range(N)]

#### Objective function
problem += pulp.lpSum([price[i] * x_vars[i] for i in range(N)]), "Total_Profit"

#### Constraints
#### CPU constraint
problem += pulp.lpSum([x_vars[i] for i in range(N)]) <= max_cpu, "CPU_Constraint"

#### Disk drives constraints
problem += pulp.lpSum([disk_drives[i] * x_vars[i] for i in range(N)]) >= min_disk, "Min_Disk_Constraint"
problem += pulp.lpSum([disk_drives[i] * x_vars[i] for i in range(N)]) <= max_disk, "Max_Disk_Constraint"

#### Memory constraints
problem += pulp.lpSum([memory_boards[i] * x_vars[i] + z_vars[i] for i in range(N)]) <= max_mem, "Max_Memory_Constraint"

for i in range(N):
    if alt_compatible[i]:
        problem += z_vars[i] <= alt_mem, f"Alt_Memory_Constraint_{i}"

#### Demand constraints for systems
for i in range(N):
    problem += preorder[i] + x_vars[i] <= demand[i], f"Demand_Constraint_{i}"

#### GP Family Demand Constraint
problem += pulp.lpSum([x_vars[i] for i in range(N) if not is_workstation[i]]) <= demand_GP, "GP_Family_Demand"

#### WS Family Demand Constraint
problem += pulp.lpSum([x_vars[i] for i in range(N) if is_workstation[i]]) <= demand_WS, "WS_Family_Demand"

#### Solve the problem
problem.solve()

#### Output
system_output = [{
    "num_produced": pulp.value(x_vars[i]),
    "total_256K_boards_used": pulp.value(y_vars[i]),
    "total_alt_boards_used": pulp.value(z_vars[i]),
    "total_disk_drives_used": pulp.value(d_vars[i])
} for i in range(N)]

result = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


