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

\section*{Mathematical Model for DEC's Production Problem}

\subsection*{Sets}
Let \( N \) be the number of different computer systems produced by DEC, indexed by \( i \in \{1, 2, \ldots, N\} \).

\subsection*{Parameters}
\begin{itemize}
    \item \( is\_workstation_i \): A binary variable indicating if system \( i \) is a workstation (1) or a general-purpose system (0).
    \item \( price_i \): The price of system \( i \) (in dollars).
    \item \( disk_i \): Average disk drives requested for system \( i \).
    \item \( mem_i \): Average number of 256K memory boards required for system \( i \).
    \item \( max\_cpu \): Maximum number of CPUs available.
    \item \( min\_disk \): Minimum number of disk drives available.
    \item \( max\_disk \): Maximum number of disk drives available.
    \item \( min\_mem \): Minimum number of 256K memory boards available.
    \item \( max\_mem \): Maximum number of 256K memory boards available.
    \item \( demand_i \): Maximum demand for system \( i \) in the next quarter.
    \item \( demand\_GP \): Maximum demand for the general-purpose (GP) family.
    \item \( demand\_WS \): Maximum demand for the workstation (WS) family.
    \item \( preorder_i \): Preorders received for system \( i \).
    \item \( alt\_mem \): Number of alternative memory boards available.
    \item \( alt\_compatible_i \): A binary variable indicating if system \( i \) can use the alternative memory board.
\end{itemize}

\subsection*{Decision Variables}
Let \( x_i \) be the number of systems produced of type \( i \) (can be non-integer).  
Let \( m_i \) be the number of 256K memory boards used for system \( i \).  
Let \( a_i \) be the number of alternative memory boards used for system \( i \).  
Let \( d_i \) be the number of disk drives used for system \( i \).  

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{Costs}
\]

\subsection*{Constraints}

1. CPU constraints:
\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drives constraints:
\[
\sum_{i=1}^{N} d_i \cdot x_i \geq min\_disk
\]
\[
\sum_{i=1}^{N} d_i \cdot x_i \leq max\_disk
\]

3. Memory constraints:
\[
\sum_{i=1}^{N} m_i \cdot x_i + \sum_{i=1}^{N} a_i \cdot x_i \leq min\_mem
\]
\[
\sum_{i=1}^{N} m_i \cdot x_i + \sum_{i=1}^{N} a_i \cdot x_i \leq max\_mem
\]

4. Demand constraints:
\[
x_i \geq preorder_i \quad \forall i
\]
\[
\sum_{i \in GP} x_i \leq demand\_GP
\]
\[
\sum_{i \in WS} x_i \leq demand\_WS
\]

5. Alternative memory board constraints:
\[
a_i \leq alt\_mem \cdot alt\_compatible_i \quad \forall i
\]

6. Non-negativity and other conditions:
\[
x_i \geq 0 \quad \text{and can be non-integer}
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

\section*{Mathematical Model for DEC's Production Problem}

\subsection*{Sets}
Let \( N \) be the number of different computer systems produced by DEC, indexed by \( i \in \{1, 2, \ldots, N\} \).

\subsection*{Parameters}
\begin{itemize}
    \item \( is\_workstation_i \): A binary variable indicating if system \( i \) is a workstation (1) or a general-purpose system (0).
    \item \( price_i \): The price of system \( i \) (in dollars).
    \item \( disk_i \): Average disk drives requested for system \( i \).
    \item \( mem_i \): Average number of 256K memory boards required for system \( i \).
    \item \( max\_cpu \): Maximum number of CPUs available.
    \item \( min\_disk \): Minimum number of disk drives available.
    \item \( max\_disk \): Maximum number of disk drives available.
    \item \( min\_mem \): Minimum number of 256K memory boards available.
    \item \( max\_mem \): Maximum number of 256K memory boards available.
    \item \( demand_i \): Maximum demand for system \( i \) in the next quarter.
    \item \( demand\_GP \): Maximum demand for the general-purpose (GP) family.
    \item \( demand\_WS \): Maximum demand for the workstation (WS) family.
    \item \( preorder_i \): Preorders received for system \( i \).
    \item \( alt\_mem \): Number of alternative memory boards available.
    \item \( alt\_compatible_i \): A binary variable indicating if system \( i \) can use the alternative memory board.
\end{itemize}

\subsection*{Decision Variables}
Let \( x_i \) be the number of systems produced of type \( i \) (can be non-integer).  
Let \( m_i \) be the number of 256K memory boards used for system \( i \).  
Let \( a_i \) be the number of alternative memory boards used for system \( i \).  
Let \( d_i \) be the number of disk drives used for system \( i \).  

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price_i \cdot x_i) - \text{Costs}
\]

\subsection*{Constraints}

1. CPU constraints:
\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drives constraints:
\[
\sum_{i=1}^{N} d_i \cdot x_i \geq min\_disk
\]
\[
\sum_{i=1}^{N} d_i \cdot x_i \leq max\_disk
\]

3. Memory constraints:
\[
\sum_{i=1}^{N} m_i \cdot x_i + \sum_{i=1}^{N} a_i \cdot x_i \leq min\_mem
\]
\[
\sum_{i=1}^{N} m_i \cdot x_i + \sum_{i=1}^{N} a_i \cdot x_i \leq max\_mem
\]

4. Demand constraints:
\[
x_i \geq preorder_i \quad \forall i
\]
\[
\sum_{i \in GP} x_i \leq demand\_GP
\]
\[
\sum_{i \in WS} x_i \leq demand\_WS
\]

5. Alternative memory board constraints:
\[
a_i \leq alt\_mem \cdot alt\_compatible_i \quad \forall i
\]

6. Non-negativity and other conditions:
\[
x_i \geq 0 \quad \text{and can be non-integer}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from json
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

#### Sets and indices
N = data['N']
GP = [i for i in range(N) if not data['IsWorkstation'][i]]
WS = [i for i in range(N) if data['IsWorkstation'][i]]

#### Decision variables
x = pulp.LpVariable.dicts('x', range(N), lowBound=0, cat='Continuous')
m = pulp.LpVariable.dicts('m', range(N), lowBound=0, cat='Continuous')
a = pulp.LpVariable.dicts('a', range(N), lowBound=0, cat='Continuous')
d = pulp.LpVariable.dicts('d', range(N), lowBound=0, cat='Continuous')

#### Define the problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Objective function
profits = pulp.lpSum(data['Price'][i] * x[i] for i in range(N))
problem += profits, "Total Profit"

#### Constraints

#### CPU constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= data['MaxCpu'], "CPU Constraint"

#### Disk drives constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) >= data['MinDisk'], "Min Disk Drives"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) <= data['MaxDisk'], "Max Disk Drives"

#### Memory constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] + a[i] for i in range(N)) <= data['MinMemory'], "Min Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] + a[i] for i in range(N)) <= data['MaxMemory'], "Max Memory"

#### Demand and preorder constraints
for i in range(N):
    problem += x[i] >= data['Preorder'][i], f"Preorder Constraint {i}"

problem += pulp.lpSum(x[i] for i in GP) <= data['DemandGP'], "Demand GP"
problem += pulp.lpSum(x[i] for i in WS) <= data['DemandWS'], "Demand WS"

#### Alternative memory board constraints
for i in range(N):
    problem += a[i] <= data['AltMemory'] * data['AltCompatible'][i], f"Alt Memory Constraint {i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```
This code sets up and solves the production problem using the Pulp library based on the mathematical model and data provided. It maximizes profitability under constraints related to CPUs, disk drives, memory boards, and demand preorders.

