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

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of computer systems
    \item $is\_workstation[i]$: Boolean indicating if system $i$ is a workstation
    \item $price[i]$: Price of system $i$
    \item $disk[i]$: Average number of disk drives requested for system $i$
    \item $mem[i]$: Average number of 256K memory boards requested for system $i$
    \item $max\_cpu$: Maximum CPUs available
    \item $min\_disk$: Minimum range of disk drives available
    \item $max\_disk$: Maximum range of disk drives available
    \item $min\_mem$: Minimum range of memory boards available
    \item $max\_mem$: Maximum range of memory boards available
    \item $demand[i]$: Maximum demand for system $i$
    \item $demand\_GP$: Maximum demand for the GP family
    \item $demand\_WS$: Maximum demand for the WS family
    \item $preorder[i]$: Preorder units for system $i$
    \item $alt\_mem$: Available alternative memory boards
    \item $alt\_compatible[i]$: Boolean indicating if system $i$ is compatible with alternative memory boards
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x[i]$: Number of systems produced of type $i$ (continuous variable)
    \item $y[i]$: Number of alternative memory boards used for system $i$ (integer variable)
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price[i] \cdot x[i]) - (cost\_mem \cdot \sum_{i=1}^{N} (mem[i] \cdot x[i] - y[i])) - (cost\_disk \cdot \sum_{i=1}^{N} disk[i] \cdot x[i])
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{i=1}^{N} x[i] \leq max\_cpu \quad \text{(CPU availability)} \\
2. & \quad \sum_{i=1}^{N} disk[i] \cdot x[i] \geq min\_disk \quad \text{(Minimum disk drives)} \\
3. & \quad \sum_{i=1}^{N} disk[i] \cdot x[i] \leq max\_disk \quad \text{(Maximum disk drives)} \\
4. & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] \geq min\_mem \quad \text{(Minimum memory boards)} \\
5. & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] \leq max\_mem \quad \text{(Maximum memory boards)} \\
6. & \quad x[i] \geq preorder[i] \quad \forall i \quad \text{(Satisfy preorders)} \\
7. & \quad \sum_{i \in GP} x[i] \leq demand\_GP \quad \text{(GP family demand)} \\
8. & \quad \sum_{i \in WS} x[i] \leq demand\_WS \quad \text{(WS family demand)} \\
9. & \quad y[i] \leq alt\_mem \quad \forall i \quad \text{(Alternative memory board limitation)} \\
10. & \quad y[i] \leq \sum_{j=1}^{N} mem[j] \cdot x[j] \quad \text{if } alt\_compatible[i] \\
\end{align*}

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

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of computer systems
    \item $is\_workstation[i]$: Boolean indicating if system $i$ is a workstation
    \item $price[i]$: Price of system $i$
    \item $disk[i]$: Average number of disk drives requested for system $i$
    \item $mem[i]$: Average number of 256K memory boards requested for system $i$
    \item $max\_cpu$: Maximum CPUs available
    \item $min\_disk$: Minimum range of disk drives available
    \item $max\_disk$: Maximum range of disk drives available
    \item $min\_mem$: Minimum range of memory boards available
    \item $max\_mem$: Maximum range of memory boards available
    \item $demand[i]$: Maximum demand for system $i$
    \item $demand\_GP$: Maximum demand for the GP family
    \item $demand\_WS$: Maximum demand for the WS family
    \item $preorder[i]$: Preorder units for system $i$
    \item $alt\_mem$: Available alternative memory boards
    \item $alt\_compatible[i]$: Boolean indicating if system $i$ is compatible with alternative memory boards
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x[i]$: Number of systems produced of type $i$ (continuous variable)
    \item $y[i]$: Number of alternative memory boards used for system $i$ (integer variable)
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{i=1}^{N} (price[i] \cdot x[i]) - (cost\_mem \cdot \sum_{i=1}^{N} (mem[i] \cdot x[i] - y[i])) - (cost\_disk \cdot \sum_{i=1}^{N} disk[i] \cdot x[i])
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{i=1}^{N} x[i] \leq max\_cpu \quad \text{(CPU availability)} \\
2. & \quad \sum_{i=1}^{N} disk[i] \cdot x[i] \geq min\_disk \quad \text{(Minimum disk drives)} \\
3. & \quad \sum_{i=1}^{N} disk[i] \cdot x[i] \leq max\_disk \quad \text{(Maximum disk drives)} \\
4. & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] \geq min\_mem \quad \text{(Minimum memory boards)} \\
5. & \quad \sum_{i=1}^{N} mem[i] \cdot x[i] \leq max\_mem \quad \text{(Maximum memory boards)} \\
6. & \quad x[i] \geq preorder[i] \quad \forall i \quad \text{(Satisfy preorders)} \\
7. & \quad \sum_{i \in GP} x[i] \leq demand\_GP \quad \text{(GP family demand)} \\
8. & \quad \sum_{i \in WS} x[i] \leq demand\_WS \quad \text{(WS family demand)} \\
9. & \quad y[i] \leq alt\_mem \quad \forall i \quad \text{(Alternative memory board limitation)} \\
10. & \quad y[i] \leq \sum_{j=1}^{N} mem[j] \cdot x[j] \quad \text{if } alt\_compatible[i] \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk = data['DiskDrives']
mem = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']

#### Costs (assuming hypothetical values for cost_mem and cost_disk)
cost_mem = 1000
cost_disk = 500

#### Problem Definition
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  #### Continuous for systems produced
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')  #### Integer for alternative memory boards

#### Objective Function
profit = pulp.lpSum(price[i] * x[i] for i in range(N)) - \
         pulp.lpSum(cost_mem * (mem[i] * x[i] - y[i]) for i in range(N)) - \
         pulp.lpSum(cost_disk * disk[i] * x[i] for i in range(N))

problem += profit

#### Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu  #### CPU availability
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) >= min_disk  #### Minimum disk drives
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) <= max_disk  #### Maximum disk drives
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) >= min_mem  #### Minimum memory boards
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) <= max_mem  #### Maximum memory boards

for i in range(N):
    problem += x[i] >= preorder[i]  #### Satisfy preorders

#### Demand constraints for GP and WS families
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_gp  #### GP family demand
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_ws  #### WS family demand

for i in range(N):
    problem += y[i] <= alt_mem  #### Alternative memory board limitation
    if alt_compatible[i]:
        problem += y[i] <= pulp.lpSum(mem[j] * x[j] for j in range(N))  #### Alternative memory board compatibility

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp
import json

#### Input data
data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk = data['DiskDrives']
mem = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']

#### Costs (assuming hypothetical values for cost_mem and cost_disk)
cost_mem = 1000
cost_disk = 500

#### Problem Definition
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  #### Continuous for systems produced
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')  #### Integer for alternative memory boards

#### Objective Function
profit = pulp.lpSum(price[i] * x[i] for i in range(N)) - \
         pulp.lpSum(cost_mem * (mem[i] * x[i] - y[i]) for i in range(N)) - \
         pulp.lpSum(cost_disk * disk[i] * x[i] for i in range(N))

problem += profit

#### Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu  #### CPU availability
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) >= min_disk  #### Minimum disk drives
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) <= max_disk  #### Maximum disk drives
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) >= min_mem  #### Minimum memory boards
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) <= max_mem  #### Maximum memory boards

for i in range(N):
    problem += x[i] >= preorder[i]  #### Satisfy preorders

#### Demand constraints for GP and WS families
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_gp  #### GP family demand
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_ws  #### WS family demand

for i in range(N):
    problem += y[i] <= alt_mem  #### Alternative memory board limitation
    if alt_compatible[i]:
        problem += y[i] <= pulp.lpSum(mem[j] * x[j] for j in range(N))  #### Alternative memory board compatibility

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/10/2/python_code0.py", line 5, in <module>
    data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk = data['DiskDrives']
mem = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']

#### Costs (assuming hypothetical values for cost_mem and cost_disk)
cost_mem = 1000
cost_disk = 500

#### Problem Definition
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  #### Continuous for systems produced
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')  #### Integer for alternative memory boards

#### Objective Function
profit = pulp.lpSum(price[i] * x[i] for i in range(N)) - \
         pulp.lpSum(cost_mem * (mem[i] * x[i] - y[i]) for i in range(N)) - \
         pulp.lpSum(cost_disk * disk[i] * x[i] for i in range(N))

problem += profit

#### Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu  #### CPU availability
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) >= min_disk  #### Minimum disk drives
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) <= max_disk  #### Maximum disk drives
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) >= min_mem  #### Minimum memory boards
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) <= max_mem  #### Maximum memory boards

for i in range(N):
    problem += x[i] >= preorder[i]  #### Satisfy preorders

#### Demand constraints for GP and WS families
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_gp  #### GP family demand
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_ws  #### WS family demand

for i in range(N):
    problem += y[i] <= alt_mem  #### Alternative memory board limitation
    if alt_compatible[i]:
        problem += y[i] <= pulp.lpSum(mem[j] * x[j] for j in range(N))  #### Alternative memory board compatibility

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

