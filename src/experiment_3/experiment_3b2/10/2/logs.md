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
To solve this problem, we need to formulate a Mixed Integer Programming (MIP) model. The goal is to maximize the profit for DEC by deciding how many units of each system to produce while considering constraints related to CPU supply, disk drives, memory boards, demand limits, and pre-orders.

Below is the mathematical model for the problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Parameters:}
\begin{align*}
N &= \text{Number of systems} \\
\text{is\_workstation}_i &= \text{True if system } i \text{ is a workstation, False otherwise} \\
\text{price}_i &= \text{Price of system } i \\
\text{disk\_drives}_i &= \text{Number of disk drives requested for system } i \\
\text{256K\_boards}_i &= \text{Number of 256K memory boards used for system } i \\
\text{max\_cpu} &= \text{Maximum number of CPUs available} \\
\text{min\_disk}, \text{max\_disk} &= \text{Minimum and maximum number of disk drives available} \\
\text{min\_mem}, \text{max\_mem} &= \text{Minimum and maximum number of 256K memory boards available} \\
\text{demand}_i &= \text{Maximum demand for system } i \\
\text{demand\_GP}, \text{demand\_WS} &= \text{Maximum demand for GP and WS families} \\
\text{preorder}_i &= \text{Pre-orders for system } i \text{ that must be fulfilled} \\
\text{alt\_mem} &= \text{Units of alternative memory boards available} \\
\text{alt\_compatible}_i &= \text{True if system } i \text{ can use alternative memory boards, False otherwise}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
x_i &= \text{Number of systems } i \text{ produced} \\
\text{alt\_used}_i &= \text{Number of alternative memory boards used for system } i
\end{align*}

\textbf{Objective:} Maximize profit
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \times x_i
\]

\textbf{Constraints:}
\begin{align*}
\sum_{i=1}^{N} x_i &\leq \text{max\_cpu} && \text{(CPU constraint)} \\
\sum_{i=1}^{N} \text{disk\_drives}_i \times x_i &\leq \text{max\_disk} && \text{(Max disk drives constraint)} \\
\sum_{i=1}^{N} \text{disk\_drives}_i \times x_i &\geq \text{min\_disk} && \text{(Min disk drives constraint)} \\
\sum_{i=1}^{N} \text{256K\_boards}_i \times x_i &\leq \text{max\_mem} && \text{(Max 256K memory boards constraint)} \\
\sum_{i=1}^{N} \text{256K\_boards}_i \times x_i &\geq \text{min\_mem} && \text{(Min 256K memory boards constraint)} \\
x_i &\leq \text{demand}_i && \forall i \text{(Demand constraint for each system)} \\
\sum_{\text{is\_workstation}_i = \text{False}} x_i &\leq \text{demand\_GP} && \text{(Demand constraint for GP systems)} \\
\sum_{\text{is\_workstation}_i = \text{True}} x_i &\leq \text{demand\_WS} && \text{(Demand constraint for WS systems)} \\
x_i &\geq \text{preorder}_i && \forall i \text{(Pre-order fulfillment)} \\
\text{alt\_used}_i &\leq x_i \times \text{alt\_compatible}_i \times \text{alt\_mem} && \forall i \text{(Alternative memory usage constraint)} \\
\end{align*}
\end{document}
```

Key points in this model:
- The objective is to maximize the total profit by multiplying the number of systems produced by their respective prices.
- The constraints ensure the availability limits of CPUs, disk drives, and memory are respected.
- They also ensure that the pre-orders are fulfilled and that the production does not exceed the estimated demand.
- The alternative memory constraint ensures that only compatible systems can use the alternative memory boards.

You can solve this MIP problem using any MIP solver to determine the optimal production numbers and calculate expected profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Parameters:}
\begin{align*}
N &= \text{Number of systems} \\
\text{is\_workstation}_i &= \text{True if system } i \text{ is a workstation, False otherwise} \\
\text{price}_i &= \text{Price of system } i \\
\text{disk\_drives}_i &= \text{Number of disk drives requested for system } i \\
\text{256K\_boards}_i &= \text{Number of 256K memory boards used for system } i \\
\text{max\_cpu} &= \text{Maximum number of CPUs available} \\
\text{min\_disk}, \text{max\_disk} &= \text{Minimum and maximum number of disk drives available} \\
\text{min\_mem}, \text{max\_mem} &= \text{Minimum and maximum number of 256K memory boards available} \\
\text{demand}_i &= \text{Maximum demand for system } i \\
\text{demand\_GP}, \text{demand\_WS} &= \text{Maximum demand for GP and WS families} \\
\text{preorder}_i &= \text{Pre-orders for system } i \text{ that must be fulfilled} \\
\text{alt\_mem} &= \text{Units of alternative memory boards available} \\
\text{alt\_compatible}_i &= \text{True if system } i \text{ can use alternative memory boards, False otherwise}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
x_i &= \text{Number of systems } i \text{ produced} \\
\text{alt\_used}_i &= \text{Number of alternative memory boards used for system } i
\end{align*}

\textbf{Objective:} Maximize profit
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \times x_i
\]

\textbf{Constraints:}
\begin{align*}
\sum_{i=1}^{N} x_i &\leq \text{max\_cpu} && \text{(CPU constraint)} \\
\sum_{i=1}^{N} \text{disk\_drives}_i \times x_i &\leq \text{max\_disk} && \text{(Max disk drives constraint)} \\
\sum_{i=1}^{N} \text{disk\_drives}_i \times x_i &\geq \text{min\_disk} && \text{(Min disk drives constraint)} \\
\sum_{i=1}^{N} \text{256K\_boards}_i \times x_i &\leq \text{max\_mem} && \text{(Max 256K memory boards constraint)} \\
\sum_{i=1}^{N} \text{256K\_boards}_i \times x_i &\geq \text{min\_mem} && \text{(Min 256K memory boards constraint)} \\
x_i &\leq \text{demand}_i && \forall i \text{(Demand constraint for each system)} \\
\sum_{\text{is\_workstation}_i = \text{False}} x_i &\leq \text{demand\_GP} && \text{(Demand constraint for GP systems)} \\
\sum_{\text{is\_workstation}_i = \text{True}} x_i &\leq \text{demand\_WS} && \text{(Demand constraint for WS systems)} \\
x_i &\geq \text{preorder}_i && \forall i \text{(Pre-order fulfillment)} \\
\text{alt\_used}_i &\leq x_i \times \text{alt\_compatible}_i \times \text{alt\_mem} && \forall i \text{(Alternative memory usage constraint)} \\
\end{align*}
\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
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

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0, cat='Integer')

#### Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory"

#### Demand Constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS"

#### Pre-order Fulfillment
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_{i}"

#### Alternative Memory Usage Constraint
for i in range(data['N']):
    problem += alt_used[i] <= x[i] * data['AltCompatible'][i] * data['AltMemory'], f"Alt_Memory_Usage_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

