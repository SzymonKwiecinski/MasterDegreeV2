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
To solve the given problem, we will formulate a Mixed-Integer Programming (MIP) model where the objective is to maximize profit. We need to consider constraints related to CPUs, disk drives, memory boards, demand fulfillment, and usage of alternative memory boards.

Here is the mathematical model for the given problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MIP Formulation for DEC's Production Problem}

\subsection*{Parameters:}

\begin{itemize}
    \item $N$: Number of computer systems.
    \item $price_i$: Price of system $i$.
    \item $disk_i$: Average disk drives requested for system $i$.
    \item $mem_i$: Average 256K memory boards used for system $i$.
    \item $max\_cpu$: Maximum units of CPUs available.
    \item $min\_disk$, $max\_disk$: Supply range of disk drives.
    \item $min\_mem$, $max\_mem$: Supply range of 256K memory boards.
    \item $demand_i$: Maximum demand for system $i$.
    \item $demand\_GP$: Maximum demand for GP family.
    \item $demand\_WS$: Maximum demand for WS family.
    \item $preorder_i$: Pre-orders for system $i$.
    \item $alt\_mem$: Units of alternative memory boards available.
    \item $is\_workstation_i$: Boolean indicating if system $i$ is a workstation.
    \item $alt\_compatible_i$: Boolean indicating if system $i$ can use alternative memory.
\end{itemize}

\subsection*{Decision Variables:}

\begin{itemize}
    \item $x_i$: Number of system $i$ produced (continuous).
    \item $y_{alt,i}$: Alternative memory boards used in system $i$.
    \item $y_{256K,i}$: 256K memory boards used in system $i$.
    \item $d_{disk,i}$: Disk drives used in system $i$.
\end{itemize}

\subsection*{Objective Function:}

Maximize the profit,

\[
\text{Maximize} \quad Z = \sum_{i=1}^{N} price_i \times x_i
\]

\subsection*{Constraints:}

1. CPU constraint:

\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drive supply constraints:

\[
\sum_{i=1}^{N} d_{disk,i} \geq min\_disk
\]
\[
\sum_{i=1}^{N} d_{disk,i} \leq max\_disk
\]

3. Memory board supply constraints:

\[
\sum_{i=1}^{N} y_{256K,i} \geq min\_mem
\]
\[
\sum_{i=1}^{N} y_{256K,i} \leq max\_mem
\]

4. Demand fulfillment for each system:

\[
x_i \leq demand_i \quad \forall i
\]

5. Pre-order fulfillment:

\[
x_i \geq preorder_i \quad \forall i
\]

6. Demand for GP and WS families:

\[
\sum_{\substack{i=1 \\ \text{is\_workstation}_i = \text{false}}}^{N} x_i \leq demand\_GP
\]
\[
\sum_{\substack{i=1 \\ \text{is\_workstation}_i = \text{true}}}^{N} x_i \leq demand\_WS
\]

7. Memory boards usage:

\[
y_{256K,i} = mem_i \times x_i \quad \forall i
\]

8. Alternative memory boards usage:

\[
y_{alt,i} \leq alt\_compatible_i \times alt\_mem \quad \forall i
\]
\[
\sum_{i=1}^{N} y_{alt,i} \leq alt\_mem
\]

9. Disk drive usage:

\[
d_{disk,i} = disk_i \times x_i \quad \forall i
\]

\subsection*{Solution:}

The solution will include the number of each system produced, the total memory boards used, and the total disk drives used, along with the maximized profit.

\end{document}
```

This LaTeX code outlines a Mixed-Integer Programming model considering all the constraints and the objective to maximize the profit. The solution must be obtained via an optimization solver capable of handling MIP problems.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MIP Formulation for DEC's Production Problem}

\subsection*{Parameters:}

\begin{itemize}
    \item $N$: Number of computer systems.
    \item $price_i$: Price of system $i$.
    \item $disk_i$: Average disk drives requested for system $i$.
    \item $mem_i$: Average 256K memory boards used for system $i$.
    \item $max\_cpu$: Maximum units of CPUs available.
    \item $min\_disk$, $max\_disk$: Supply range of disk drives.
    \item $min\_mem$, $max\_mem$: Supply range of 256K memory boards.
    \item $demand_i$: Maximum demand for system $i$.
    \item $demand\_GP$: Maximum demand for GP family.
    \item $demand\_WS$: Maximum demand for WS family.
    \item $preorder_i$: Pre-orders for system $i$.
    \item $alt\_mem$: Units of alternative memory boards available.
    \item $is\_workstation_i$: Boolean indicating if system $i$ is a workstation.
    \item $alt\_compatible_i$: Boolean indicating if system $i$ can use alternative memory.
\end{itemize}

\subsection*{Decision Variables:}

\begin{itemize}
    \item $x_i$: Number of system $i$ produced (continuous).
    \item $y_{alt,i}$: Alternative memory boards used in system $i$.
    \item $y_{256K,i}$: 256K memory boards used in system $i$.
    \item $d_{disk,i}$: Disk drives used in system $i$.
\end{itemize}

\subsection*{Objective Function:}

Maximize the profit,

\[
\text{Maximize} \quad Z = \sum_{i=1}^{N} price_i \times x_i
\]

\subsection*{Constraints:}

1. CPU constraint:

\[
\sum_{i=1}^{N} x_i \leq max\_cpu
\]

2. Disk drive supply constraints:

\[
\sum_{i=1}^{N} d_{disk,i} \geq min\_disk
\]
\[
\sum_{i=1}^{N} d_{disk,i} \leq max\_disk
\]

3. Memory board supply constraints:

\[
\sum_{i=1}^{N} y_{256K,i} \geq min\_mem
\]
\[
\sum_{i=1}^{N} y_{256K,i} \leq max\_mem
\]

4. Demand fulfillment for each system:

\[
x_i \leq demand_i \quad \forall i
\]

5. Pre-order fulfillment:

\[
x_i \geq preorder_i \quad \forall i
\]

6. Demand for GP and WS families:

\[
\sum_{\substack{i=1 \\ \text{is\_workstation}_i = \text{false}}}^{N} x_i \leq demand\_GP
\]
\[
\sum_{\substack{i=1 \\ \text{is\_workstation}_i = \text{true}}}^{N} x_i \leq demand\_WS
\]

7. Memory boards usage:

\[
y_{256K,i} = mem_i \times x_i \quad \forall i
\]

8. Alternative memory boards usage:

\[
y_{alt,i} \leq alt\_compatible_i \times alt\_mem \quad \forall i
\]
\[
\sum_{i=1}^{N} y_{alt,i} \leq alt\_mem
\]

9. Disk drive usage:

\[
d_{disk,i} = disk_i \times x_i \quad \forall i
\]

\subsection*{Solution:}

The solution will include the number of each system produced, the total memory boards used, and the total disk drives used, along with the maximized profit.

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from the provided JSON
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

#### Create the Linear Programming problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=data['Preorder'][i], upBound=data['Demand'][i], cat='Continuous') for i in range(data['N'])]
y_256K = [pulp.LpVariable(f'y_256K_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
y_alt = [pulp.LpVariable(f'y_alt_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
d_disk = [pulp.LpVariable(f'd_disk_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

#### Objective function
problem += pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])

#### Constraints
#### 1. CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

#### 2. Disk drive supply constraints
problem += pulp.lpSum(d_disk) >= data['MinDisk']
problem += pulp.lpSum(d_disk) <= data['MaxDisk']

#### 3. Memory board supply constraints
problem += pulp.lpSum(y_256K) >= data['MinMemory']
problem += pulp.lpSum(y_256K) <= data['MaxMemory']

#### 6. Demand for GP and WS families
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

#### 7. Memory boards usage
for i in range(data['N']):
    problem += y_256K[i] == data['MemoryBoards'][i] * x[i]

#### 8. Alternative memory boards usage
for i in range(data['N']):
    problem += y_alt[i] <= data['AltCompatible'][i] * data['AltMemory']
problem += pulp.lpSum(y_alt) <= data['AltMemory']

#### 9. Disk drive usage
for i in range(data['N']):
    problem += d_disk[i] == data['DiskDrives'][i] * x[i]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Print decision variables to give insight into the model's outcome
for i in range(data['N']):
    print(f"System {i+1}: Produced: {x[i].varValue}, 256K Memory used: {y_256K[i].varValue}, Alt Memory used: {y_alt[i].varValue}, Disk Drives used: {d_disk[i].varValue}")
```

