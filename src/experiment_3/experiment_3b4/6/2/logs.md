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
To solve this problem, we need to create a Mixed-Integer Programming (MIP) model that will maximize the profit for DEC while taking into account the production constraints. Let's define the mathematical model:

######### Decision Variables
- \( x_i \): The number of systems of type \( i \) to produce (continuous).
- \( m_i \): The number of 256K memory boards used by system \( i \).
- \( a_i \): The number of alternative memory boards used by system \( i \) (only if the system is compatible with alternative memory).
- \( d_i \): The number of disk drives used by system \( i \).

######### Objective Function
Maximize the total profit, which is the total sales income minus the cost of resources (optional, as not explicitly required by the prompt):
\[ \text{Maximize} \quad \sum_{i=1}^{N} \text{price}_i \times x_i \]

######### Constraints
1. CPU supply constraint:
   \[
   \sum_{i=1}^{N} x_i \leq \text{max\_cpu}
   \]

2. Disk drive supply constraint:
   \[
   \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk\_drives}_i \times x_i \leq \text{max\_disk}
   \]

3. Memory board supply constraint:
   \[
   \text{min\_mem} \leq \sum_{i=1}^{N} \text{256K\_boards}_i \times x_i \leq \text{max\_mem}
   \]

4. Alternative memory board usage constraint:
   \[
   \sum_{i=1}^{N} a_i \leq \text{alt\_mem}
   \]

5. Demand constraints:
   \[
   x_i \leq \text{demand}_i \quad \forall i
   \]
   \[
   \sum_{i : \text{is\_workstation}[i] = \text{false}} x_i \leq \text{demand\_GP}
   \]
   \[
   \sum_{i : \text{is\_workstation}[i] = \text{true}} x_i \leq \text{demand\_WS}
   \]

6. Preorder fulfillment:
   \[
   x_i \geq \text{preorder}_i \quad \forall i
   \]

7. Memory compatibility constraints (only use alternative memory if compatible):
   \[
   a_i = 0 \quad \text{if alt\_compatible}[i] = \text{false}
   \]

Now let's code this in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}
\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of systems of type } i \text{ to produce (continuous)} \\
m_i & : \text{Number of 256K memory boards used by system } i \\
a_i & : \text{Number of alternative memory boards used by system } i \\
d_i & : \text{Number of disk drives used by system } i
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize} \quad & \sum_{i=1}^{N} \text{price}_i \times x_i
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{i=1}^{N} x_i \leq \text{max\_cpu} \\
& \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk\_drives}_i \times x_i \leq \text{max\_disk} \\
& \text{min\_mem} \leq \sum_{i=1}^{N} \text{256K\_boards}_i \times x_i \leq \text{max\_mem} \\
& \sum_{i=1}^{N} a_i \leq \text{alt\_mem} \\
& x_i \leq \text{demand}_i \quad \forall i \\
& \sum_{i : \text{is\_workstation}[i] = \text{false}} x_i \leq \text{demand\_GP} \\
& \sum_{i : \text{is\_workstation}[i] = \text{true}} x_i \leq \text{demand\_WS} \\
& x_i \geq \text{preorder}_i \quad \forall i \\
& a_i = 0 \quad \text{if alt\_compatible}[i] = \text{false}
\end{align*}

\end{document}
``` 

This model aims to maximize the profit by deciding the number of systems to produce, while respecting the constraints on CPU, memory, disk drives, demand, and preorders. The alternative memory boards are used only if they are compatible.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}
\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of systems of type } i \text{ to produce (continuous)} \\
m_i & : \text{Number of 256K memory boards used by system } i \\
a_i & : \text{Number of alternative memory boards used by system } i \\
d_i & : \text{Number of disk drives used by system } i
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize} \quad & \sum_{i=1}^{N} \text{price}_i \times x_i
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{i=1}^{N} x_i \leq \text{max\_cpu} \\
& \text{min\_disk} \leq \sum_{i=1}^{N} \text{disk\_drives}_i \times x_i \leq \text{max\_disk} \\
& \text{min\_mem} \leq \sum_{i=1}^{N} \text{256K\_boards}_i \times x_i \leq \text{max\_mem} \\
& \sum_{i=1}^{N} a_i \leq \text{alt\_mem} \\
& x_i \leq \text{demand}_i \quad \forall i \\
& \sum_{i : \text{is\_workstation}[i] = \text{false}} x_i \leq \text{demand\_GP} \\
& \sum_{i : \text{is\_workstation}[i] = \text{true}} x_i \leq \text{demand\_WS} \\
& x_i \geq \text{preorder}_i \quad \forall i \\
& a_i = 0 \quad \text{if alt\_compatible}[i] = \text{false}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

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
problem = pulp.LpProblem("Maximize_System_Production_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=data['Preorder'][i], upBound=data['Demand'][i], cat='Continuous') for i in range(data['N'])]
a = [pulp.LpVariable(f"a_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

#### Objective function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory']
problem += pulp.lpSum(a[i] for i in range(data['N'])) <= data['AltMemory']

for i in range(data['N']):
    if not data['AltCompatible'][i]:
        problem += a[i] == 0

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

