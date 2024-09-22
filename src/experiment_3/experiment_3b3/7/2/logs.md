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

\section*{Mathematical Model for DEC's Production Optimization Problem}

\subsection*{Sets}
\begin{itemize}
    \item \( i \in \{1, 2, \ldots, N\} \): represents different system types.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( is\_workstation[i] \): boolean indicating if system \( i \) is a workstation (WS).
    \item \( price[i] \): price of system \( i \).
    \item \( disk[i] \): average number of disk drives requested for system \( i \).
    \item \( mem[i] \): average number of 256K memory boards requested for system \( i \).
    \item \( max\_cpu \): maximum number of CPUs available.
    \item \( min\_disk \): minimum number of disk drives available.
    \item \( max\_disk \): maximum number of disk drives available.
    \item \( min\_mem \): minimum number of 256K memory boards available.
    \item \( max\_mem \): maximum number of 256K memory boards available.
    \item \( demand[i] \): estimated maximum demand for system \( i \).
    \item \( demand\_GP \): estimated maximum demand for the general-purpose (GP) family.
    \item \( demand\_WS \): estimated maximum demand for the workstation (WS) family.
    \item \( preorder[i] \): preorders received for system \( i \).
    \item \( alt\_mem \): available alternative memory boards.
    \item \( alt\_compatible[i] \): boolean indicating if alternative memory can be used for system \( i \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x[i] \): number of systems of type \( i \) to produce, \( x[i] \geq 0 \).
    \item \( alt[i] \): number of alternative memory boards used for system \( i \), \( alt[i] \geq 0 \).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Max } Z = \sum_{i=1}^{N} \left( price[i] \cdot x[i] - (mem[i] \cdot 256K\_cost + disk[i] \cdot disk\_cost + alt[i] \cdot alt\_cost) \right)
\]

\subsection*{Constraints}
\begin{align}
    \sum_{i=1}^{N} x[i] & \leq max\_cpu \quad \text{(CPU constraint)} \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \geq min\_disk \quad \text{(Disk supply constraint)} \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \leq max\_disk \quad \text{(Disk supply constraint)} \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \geq min\_mem \quad \text{(Memory supply constraint)} \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \leq max\_mem \quad \text{(Memory supply constraint)} \\
    x[i] & \leq demand[i] \quad \forall i \quad \text{(Demand constraint for each system)} \\
    \sum_{i \text{ s.t. } is\_workstation[i]} x[i] & \leq demand\_WS \quad \text{(Total WS demand constraint)} \\
    \sum_{i \text{ s.t. } \neg is\_workstation[i]} x[i] & \leq demand\_GP \quad \text{(Total GP demand constraint)} \\
    x[i] & \geq preorder[i] \quad \forall i \quad \text{(Preorder constraint)} \\
    alt[i] & \leq alt\_mem \quad \text{(Alternative memory board constraint)} \\
    alt[i] & \leq alt\_compatible[i] \cdot  x[i] \quad \forall i \quad \text{(Alternative memory compatibility)}
\end{align}

\subsection*{Output}
The output will be in the following JSON format:
\begin{verbatim}
{
    "system_output": [
        {
            "num_produced": x[i],
            "total_256K_boards_used": mem[i] \cdot x[i],
            "total_alt_boards_used": alt[i],
            "total_disk_drives_used": disk[i] \cdot x[i]
        }
        for i in 1, ..., N
    ],
    "profit": Z
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

\section*{Mathematical Model for DEC's Production Optimization Problem}

\subsection*{Sets}
\begin{itemize}
    \item \( i \in \{1, 2, \ldots, N\} \): represents different system types.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( is\_workstation[i] \): boolean indicating if system \( i \) is a workstation (WS).
    \item \( price[i] \): price of system \( i \).
    \item \( disk[i] \): average number of disk drives requested for system \( i \).
    \item \( mem[i] \): average number of 256K memory boards requested for system \( i \).
    \item \( max\_cpu \): maximum number of CPUs available.
    \item \( min\_disk \): minimum number of disk drives available.
    \item \( max\_disk \): maximum number of disk drives available.
    \item \( min\_mem \): minimum number of 256K memory boards available.
    \item \( max\_mem \): maximum number of 256K memory boards available.
    \item \( demand[i] \): estimated maximum demand for system \( i \).
    \item \( demand\_GP \): estimated maximum demand for the general-purpose (GP) family.
    \item \( demand\_WS \): estimated maximum demand for the workstation (WS) family.
    \item \( preorder[i] \): preorders received for system \( i \).
    \item \( alt\_mem \): available alternative memory boards.
    \item \( alt\_compatible[i] \): boolean indicating if alternative memory can be used for system \( i \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x[i] \): number of systems of type \( i \) to produce, \( x[i] \geq 0 \).
    \item \( alt[i] \): number of alternative memory boards used for system \( i \), \( alt[i] \geq 0 \).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Max } Z = \sum_{i=1}^{N} \left( price[i] \cdot x[i] - (mem[i] \cdot 256K\_cost + disk[i] \cdot disk\_cost + alt[i] \cdot alt\_cost) \right)
\]

\subsection*{Constraints}
\begin{align}
    \sum_{i=1}^{N} x[i] & \leq max\_cpu \quad \text{(CPU constraint)} \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \geq min\_disk \quad \text{(Disk supply constraint)} \\
    \sum_{i=1}^{N} disk[i] \cdot x[i] & \leq max\_disk \quad \text{(Disk supply constraint)} \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \geq min\_mem \quad \text{(Memory supply constraint)} \\
    \sum_{i=1}^{N} mem[i] \cdot x[i] & \leq max\_mem \quad \text{(Memory supply constraint)} \\
    x[i] & \leq demand[i] \quad \forall i \quad \text{(Demand constraint for each system)} \\
    \sum_{i \text{ s.t. } is\_workstation[i]} x[i] & \leq demand\_WS \quad \text{(Total WS demand constraint)} \\
    \sum_{i \text{ s.t. } \neg is\_workstation[i]} x[i] & \leq demand\_GP \quad \text{(Total GP demand constraint)} \\
    x[i] & \geq preorder[i] \quad \forall i \quad \text{(Preorder constraint)} \\
    alt[i] & \leq alt\_mem \quad \text{(Alternative memory board constraint)} \\
    alt[i] & \leq alt\_compatible[i] \cdot  x[i] \quad \forall i \quad \text{(Alternative memory compatibility)}
\end{align}

\subsection*{Output}
The output will be in the following JSON format:
\begin{verbatim}
{
    "system_output": [
        {
            "num_produced": x[i],
            "total_256K_boards_used": mem[i] \cdot x[i],
            "total_alt_boards_used": alt[i],
            "total_disk_drives_used": disk[i] \cdot x[i]
        }
        for i in 1, ..., N
    ],
    "profit": Z
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Cost parameters
disk_cost = 100  #### assumed cost of disk
board_cost = 200  #### assumed cost of 256K memory board
alt_cost = 150  #### assumed cost of alternative memory board

#### Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
alt = [pulp.LpVariable(f'alt_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

#### Objective Function
problem += pulp.lpSum([
    data['Price'][i] * x[i] - (data['MemoryBoards'][i] * board_cost + data['DiskDrives'][i] * disk_cost + alt[i] * alt_cost)
    for i in range(data['N'])
])

#### Constraints
#### CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

#### Disk supply constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']

#### Memory supply constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) >= data['MinMemory']
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) <= data['MaxMemory']

#### Demand constraints for each system
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]
    problem += x[i] >= data['Preorder'][i]

#### Total WS and GP demand constraints
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']

#### Alternative memory board constraints
for i in range(data['N']):
    problem += alt[i] <= data['AltMemory']
    problem += alt[i] <= data['AltCompatible'][i] * x[i]

#### Solve the problem
problem.solve()

#### Output
system_output = [{
    "num_produced": int(pulp.value(x[i])),
    "total_256K_boards_used": int(data['MemoryBoards'][i] * pulp.value(x[i])),
    "total_alt_boards_used": int(pulp.value(alt[i])),
    "total_disk_drives_used": int(data['DiskDrives'][i] * pulp.value(x[i]))
} for i in range(data['N'])]

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

