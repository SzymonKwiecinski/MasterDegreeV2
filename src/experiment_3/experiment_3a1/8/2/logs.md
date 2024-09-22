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

\section*{Mathematical Model for DEC's Computer Systems Production}

\subsection*{Variables}
Let \( x_i \) be the number of systems of type \( i \) produced, where \( i = 1, 2, \ldots, N \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{is\_workstation}_i \) : boolean indicating if system \( i \) is a workstation.
    \item \( \text{price}_i \) : price of system \( i \).
    \item \( \text{disk\_drives}_i \) : average number of disk drives requested for system \( i \).
    \item \( \text{256K\_boards}_i \) : average memory boards required for system \( i \).
    \item \( \text{max\_cpu} \) : maximum number of CPUs available.
    \item \( \text{min\_disk} \) : minimum number of disk drives available.
    \item \( \text{max\_disk} \) : maximum number of disk drives available.
    \item \( \text{min\_mem} \) : minimum number of 256K memory boards available.
    \item \( \text{max\_mem} \) : maximum number of 256K memory boards available.
    \item \( \text{demand}_i \) : maximum demand for system \( i \).
    \item \( \text{demand\_GP} \) : maximum demand for general-purpose systems.
    \item \( \text{demand\_WS} \) : maximum demand for workstation systems.
    \item \( \text{preorder}_i \) : preorders for system \( i \).
    \item \( \text{alt\_mem} \) : available alternative memory boards.
    \item \( \text{alt\_compatible}_i \) : boolean for compatibility with alternative memory boards for system \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:

\[
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \cdot x_i - \text{costs}(x_i) \right)
\]

Where \(\text{costs}(x_i)\) accounts for memory and disk drive costs.

\subsection*{Constraints}
1. CPU constraint:
\[
\sum_{i=1}^{N} x_i \leq \text{max\_cpu}
\]

2. Disk drive constraint:
\[
\sum_{i=1}^{N} \text{disk\_drives}_i \cdot x_i \geq \text{min\_disk}
\]
\[
\sum_{i=1}^{N} \text{disk\_drives}_i \cdot x_i \leq \text{max\_disk}
\]

3. Memory board constraint:
\[
\sum_{i=1}^{N} \text{256K\_boards}_i \cdot x_i \geq \text{min\_mem}
\]
\[
\sum_{i=1}^{N} \text{256K\_boards}_i \cdot x_i + \sum_{i=1}^{N} \text{alt\_compatible}_i \cdot x_i \leq \text{max\_mem} + \text{alt\_mem}
\]

4. Demand constraints:
\[
\sum_{i \,:\, \text{is\_workstation}_i} x_i \leq \text{demand\_WS}
\]
\[
\sum_{i \,:\, \neg \text{is\_workstation}_i} x_i \leq \text{demand\_GP}
\]

5. Preorder constraints:
\[
x_i \geq \text{preorder}_i, \quad \forall i \in \{1, 2, \ldots, N\}
\]

6. Demand limits:
\[
x_i \leq \text{demand}_i, \quad \forall i
\]

\subsection*{Output Format}
The output should be formatted as follows:
\begin{verbatim}
{
    "system_output": [
        {
            "num_produced": x_i,
            "total_256K_boards_used": \text{boards_used}_i,
            "total_alt_boards_used": \text{alt_boards_used}_i,
            "total_disk_drives_used": \text{disk_used}_i
        } 
        \text{ for } i = 1, \ldots, N
    ],
    "profit": \text{total_profit}
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

\section*{Mathematical Model for DEC's Computer Systems Production}

\subsection*{Variables}
Let \( x_i \) be the number of systems of type \( i \) produced, where \( i = 1, 2, \ldots, N \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{is\_workstation}_i \) : boolean indicating if system \( i \) is a workstation.
    \item \( \text{price}_i \) : price of system \( i \).
    \item \( \text{disk\_drives}_i \) : average number of disk drives requested for system \( i \).
    \item \( \text{256K\_boards}_i \) : average memory boards required for system \( i \).
    \item \( \text{max\_cpu} \) : maximum number of CPUs available.
    \item \( \text{min\_disk} \) : minimum number of disk drives available.
    \item \( \text{max\_disk} \) : maximum number of disk drives available.
    \item \( \text{min\_mem} \) : minimum number of 256K memory boards available.
    \item \( \text{max\_mem} \) : maximum number of 256K memory boards available.
    \item \( \text{demand}_i \) : maximum demand for system \( i \).
    \item \( \text{demand\_GP} \) : maximum demand for general-purpose systems.
    \item \( \text{demand\_WS} \) : maximum demand for workstation systems.
    \item \( \text{preorder}_i \) : preorders for system \( i \).
    \item \( \text{alt\_mem} \) : available alternative memory boards.
    \item \( \text{alt\_compatible}_i \) : boolean for compatibility with alternative memory boards for system \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:

\[
\text{Profit} = \sum_{i=1}^{N} \left( \text{price}_i \cdot x_i - \text{costs}(x_i) \right)
\]

Where \(\text{costs}(x_i)\) accounts for memory and disk drive costs.

\subsection*{Constraints}
1. CPU constraint:
\[
\sum_{i=1}^{N} x_i \leq \text{max\_cpu}
\]

2. Disk drive constraint:
\[
\sum_{i=1}^{N} \text{disk\_drives}_i \cdot x_i \geq \text{min\_disk}
\]
\[
\sum_{i=1}^{N} \text{disk\_drives}_i \cdot x_i \leq \text{max\_disk}
\]

3. Memory board constraint:
\[
\sum_{i=1}^{N} \text{256K\_boards}_i \cdot x_i \geq \text{min\_mem}
\]
\[
\sum_{i=1}^{N} \text{256K\_boards}_i \cdot x_i + \sum_{i=1}^{N} \text{alt\_compatible}_i \cdot x_i \leq \text{max\_mem} + \text{alt\_mem}
\]

4. Demand constraints:
\[
\sum_{i \,:\, \text{is\_workstation}_i} x_i \leq \text{demand\_WS}
\]
\[
\sum_{i \,:\, \neg \text{is\_workstation}_i} x_i \leq \text{demand\_GP}
\]

5. Preorder constraints:
\[
x_i \geq \text{preorder}_i, \quad \forall i \in \{1, 2, \ldots, N\}
\]

6. Demand limits:
\[
x_i \leq \text{demand}_i, \quad \forall i
\]

\subsection*{Output Format}
The output should be formatted as follows:
\begin{verbatim}
{
    "system_output": [
        {
            "num_produced": x_i,
            "total_256K_boards_used": \text{boards_used}_i,
            "total_alt_boards_used": \text{alt_boards_used}_i,
            "total_disk_drives_used": \text{disk_used}_i
        } 
        \text{ for } i = 1, \ldots, N
    ],
    "profit": \text{total_profit}
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the given JSON
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

#### Create the optimization problem
problem = pulp.LpProblem("Computer_Systems_Production", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(1, data['N'] + 1), lowBound=0, cat='Integer')

#### Objective function
profit = pulp.lpSum(data['Price'][i-1] * x[i] for i in range(1, data['N'] + 1))
costs = pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1))  #### Assuming cost is related to memory boards
problem += profit - costs, "Total_Profit"

#### Constraints
#### CPU constraint
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1)) <= data['MaxCpu'], "CPU_Constraint"

#### Disk drive constraints
problem += pulp.lpSum(data['DiskDrives'][i-1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i-1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxDisk'], "Max_Disk_Constraint"

#### Memory board constraints
problem += pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinMemory'], "Min_Memory_Constraint"
problem += (pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1)) + 
             pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['AltCompatible'][i-1])) <= data['MaxMemory'] + data['AltMemory'], "Max_Memory_Constraint"

#### Demand constraints for workstations and general-purpose
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['IsWorkstation'][i-1]) <= data['DemandWS'], "Demand_WS_Constraint"
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if not data['IsWorkstation'][i-1]) <= data['DemandGP'], "Demand_GP_Constraint"

#### Preorder constraints
for i in range(1, data['N'] + 1):
    problem += x[i] >= data['Preorder'][i-1], f"Preorder_Constraint_{i}"

#### Demand limits
for i in range(1, data['N'] + 1):
    problem += x[i] <= data['Demand'][i-1], f"Demand_Limit_{i}"

#### Solve the problem
problem.solve()

#### Prepare output
system_output = []
for i in range(1, data['N'] + 1):
    boards_used = data['MemoryBoards'][i-1] * x[i].varValue
    alt_boards_used = x[i].varValue if data['AltCompatible'][i-1] else 0
    disk_used = data['DiskDrives'][i-1] * x[i].varValue
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": boards_used,
        "total_alt_boards_used": alt_boards_used,
        "total_disk_drives_used": disk_used
    })

total_profit = pulp.value(problem.objective)

#### Output the result
import json
result = {
    "system_output": system_output,
    "profit": total_profit
}
print(json.dumps(result, indent=4))

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

