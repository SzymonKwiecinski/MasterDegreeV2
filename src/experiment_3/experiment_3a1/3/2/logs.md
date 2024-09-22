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

\section*{Mathematical Model for Digital Equipment Corporation (DEC) Production Optimization}

\subsection*{Sets}
\begin{itemize}
    \item Let \( N \) be the number of different computer systems.
    \item Let \( i \) denote each system, where \( i = 1, 2, \ldots, N \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{is\_workstation}_i \): Boolean, true if system \( i \) is a workstation.
    \item \( \text{price}_i \): Price of system \( i \).
    \item \( \text{disk\_drives}_i \): Average number of disk drives requested for system \( i \).
    \item \( \text{mem}_i \): Average number of 256K memory boards used for system \( i \).
    \item \( \text{max\_cpu} \): Maximum number of CPUs available.
    \item \( \text{min\_disk} \), \( \text{max\_disk} \): Minimum and maximum supply of disk drives.
    \item \( \text{min\_mem} \), \( \text{max\_mem} \): Minimum and maximum supply of 256K memory boards.
    \item \( \text{demand}_i \): Maximum demand for system \( i \).
    \item \( \text{demand\_GP} \): Maximum demand for the whole GP family.
    \item \( \text{demand\_WS} \): Maximum demand for the whole WS family.
    \item \( \text{preorder}_i \): Preorders for system \( i \).
    \item \( \text{alt\_mem} \): Units of alternative memory boards available.
    \item \( \text{alt\_compatible}_i \): Boolean, true if system \( i \) can use alternative memory boards.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_i \): Number of systems produced of type \( i \) (continuous variable).
    \item Let \( alt\_used_i \): Number of alternative memory boards used for system \( i \) (integer variable, if any).
    \end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \text{costs}
\]

\subsection*{Constraints}

1. **CPU Constraints**:
\[
\sum_{i=1}^{N} x_i \leq \text{max\_cpu}
\]

2. **Disk Drive Constraints**:
\[
\sum_{i=1}^{N} (\text{disk\_drives}_i \cdot x_i) \geq \text{min\_disk}
\]
\[
\sum_{i=1}^{N} (\text{disk\_drives}_i \cdot x_i) \leq \text{max\_disk}
\]

3. **256K Memory Board Constraints**:
\[
\sum_{i=1}^{N} (\text{mem}_i \cdot x_i) + \sum_{i=1}^{N} (alt\_used_i \cdot \text{alt\_compatible}_i) \geq \text{min\_mem}
\]
\[
\sum_{i=1}^{N} (\text{mem}_i \cdot x_i) + \sum_{i=1}^{N} (alt\_used_i \cdot \text{alt\_compatible}_i) \leq \text{max\_mem}
\]

4. **Demand Constraints**:
\[
x_i \geq \text{preorder}_i \quad \forall i
\]
\[
\sum_{i \in \text{GP}} x_i \leq \text{demand\_GP}
\]
\[
\sum_{i \in \text{WS}} x_i \leq \text{demand\_WS}
\]

5. **Alternative Memory Board Usage**:
\[
alt\_used_i \leq \text{alt\_mem} \cdot \text{alt\_compatible}_i
\]

\subsection*{Output Format}
\begin{itemize}
    \item \textit{"system\_output"}: A list with details of each system produced:
    \[
    \text{system\_output} = \{ 
        \text{num\_produced} = x_i, \, 
        \text{total\_256K\_boards\_used} = \text{mem}_i \cdot x_i, \,
        \text{total\_alt\_boards\_used} = alt\_used_i, \,
        \text{total\_disk\_drives\_used} = \text{disk\_drives}_i \cdot x_i 
    \}
    \]
    \item \textit{"profit"}: Total profit for the next quarter.
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

\section*{Mathematical Model for Digital Equipment Corporation (DEC) Production Optimization}

\subsection*{Sets}
\begin{itemize}
    \item Let \( N \) be the number of different computer systems.
    \item Let \( i \) denote each system, where \( i = 1, 2, \ldots, N \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{is\_workstation}_i \): Boolean, true if system \( i \) is a workstation.
    \item \( \text{price}_i \): Price of system \( i \).
    \item \( \text{disk\_drives}_i \): Average number of disk drives requested for system \( i \).
    \item \( \text{mem}_i \): Average number of 256K memory boards used for system \( i \).
    \item \( \text{max\_cpu} \): Maximum number of CPUs available.
    \item \( \text{min\_disk} \), \( \text{max\_disk} \): Minimum and maximum supply of disk drives.
    \item \( \text{min\_mem} \), \( \text{max\_mem} \): Minimum and maximum supply of 256K memory boards.
    \item \( \text{demand}_i \): Maximum demand for system \( i \).
    \item \( \text{demand\_GP} \): Maximum demand for the whole GP family.
    \item \( \text{demand\_WS} \): Maximum demand for the whole WS family.
    \item \( \text{preorder}_i \): Preorders for system \( i \).
    \item \( \text{alt\_mem} \): Units of alternative memory boards available.
    \item \( \text{alt\_compatible}_i \): Boolean, true if system \( i \) can use alternative memory boards.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_i \): Number of systems produced of type \( i \) (continuous variable).
    \item Let \( alt\_used_i \): Number of alternative memory boards used for system \( i \) (integer variable, if any).
    \end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} (\text{price}_i \cdot x_i) - \text{costs}
\]

\subsection*{Constraints}

1. **CPU Constraints**:
\[
\sum_{i=1}^{N} x_i \leq \text{max\_cpu}
\]

2. **Disk Drive Constraints**:
\[
\sum_{i=1}^{N} (\text{disk\_drives}_i \cdot x_i) \geq \text{min\_disk}
\]
\[
\sum_{i=1}^{N} (\text{disk\_drives}_i \cdot x_i) \leq \text{max\_disk}
\]

3. **256K Memory Board Constraints**:
\[
\sum_{i=1}^{N} (\text{mem}_i \cdot x_i) + \sum_{i=1}^{N} (alt\_used_i \cdot \text{alt\_compatible}_i) \geq \text{min\_mem}
\]
\[
\sum_{i=1}^{N} (\text{mem}_i \cdot x_i) + \sum_{i=1}^{N} (alt\_used_i \cdot \text{alt\_compatible}_i) \leq \text{max\_mem}
\]

4. **Demand Constraints**:
\[
x_i \geq \text{preorder}_i \quad \forall i
\]
\[
\sum_{i \in \text{GP}} x_i \leq \text{demand\_GP}
\]
\[
\sum_{i \in \text{WS}} x_i \leq \text{demand\_WS}
\]

5. **Alternative Memory Board Usage**:
\[
alt\_used_i \leq \text{alt\_mem} \cdot \text{alt\_compatible}_i
\]

\subsection*{Output Format}
\begin{itemize}
    \item \textit{"system\_output"}: A list with details of each system produced:
    \[
    \text{system\_output} = \{ 
        \text{num\_produced} = x_i, \, 
        \text{total\_256K\_boards\_used} = \text{mem}_i \cdot x_i, \,
        \text{total\_alt\_boards\_used} = alt\_used_i, \,
        \text{total\_disk\_drives\_used} = \text{disk\_drives}_i \cdot x_i 
    \}
    \]
    \item \textit{"profit"}: Total profit for the next quarter.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

#### Model Initialization
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  #### Continuous variable
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0, cat='Integer')

#### Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

#### Constraints
#### CPU Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

#### Disk Drive Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

#### 256K Memory Board Constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] * data['AltCompatible'][i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] * data['AltCompatible'][i] for i in range(data['N'])) <= data['MaxMemory']

#### Demand Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']

#### Alternative Memory Board Usage
for i in range(data['N']):
    problem += alt_used[i] <= data['AltMemory'] * data['AltCompatible'][i]

#### Solve the problem
problem.solve()

#### Output the results
system_output = {}
for i in range(data['N']):
    system_output[i] = {
        'num_produced': x[i].varValue,
        'total_256K_boards_used': data['MemoryBoards'][i] * x[i].varValue,
        'total_alt_boards_used': alt_used[i].varValue,
        'total_disk_drives_used': data['DiskDrives'][i] * x[i].varValue
    }

profit_value = pulp.value(problem.objective)

print(f'System Output: {system_output}')
print(f'Profit: {profit_value}')
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')
```

