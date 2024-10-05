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
To model this problem, we will create a Mixed-Integer Linear Programming (MILP) formulation. We'll define decision variables, the objective function, and the constraints based on the problem description. Here is the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Model for DEC Production Optimization}

\textbf{Sets and Indices:}
\begin{align*}
    i & : \text{Index for computer systems,} \quad i = 1, \ldots, N.
\end{align*}

\textbf{Parameters:}
\begin{align*}
    \text{\texttt{price}}_i & : \text{Price of system } i. \\
    \text{\texttt{disk\_drives}}_i & : \text{Average units of disk drives requested for system } i. \\
    \text{\texttt{256K\_boards}}_i & : \text{Average units of 256K memory boards used by system } i. \\
    \text{\texttt{max\_cpu}} & : \text{Maximum units of CPU available.} \\
    \text{\texttt{min\_disk}}, \text{\texttt{max\_disk}} & : \text{Minimum and maximum units of disk drives available.} \\
    \text{\texttt{min\_mem}}, \text{\texttt{max\_mem}} & : \text{Minimum and maximum units of 256K memory boards available.} \\
    \text{\texttt{demand}}_i & : \text{Maximum demand for system } i. \\
    \text{\texttt{demand\_GP}}, \text{\texttt{demand\_WS}} & : \text{Maximum demand for GP and WS systems.} \\
    \text{\texttt{preorder}}_i & : \text{Pre-orders for system } i. \\
    \text{\texttt{alt\_mem}} & : \text{Units of alternative memory boards available.} \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
    x_i & : \text{Number of systems of type } i \text{ to produce (continuous).} \\
    y_i & : \text{Number of 256K memory boards used by system } i. \\
    z_i & : \text{Number of alternative memory boards used by system } i \text{ (binary)}.
\end{align*}

\textbf{Objective Function:}
\[
\max \sum_{i=1}^{N} \text{\texttt{price}}_i \cdot x_i
\]

\textbf{Constraints:}
\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{\texttt{max\_cpu}}, & \text{(CPU availability constraint)} \\
    & \text{\texttt{min\_disk}} \leq \sum_{i=1}^{N} \text{\texttt{disk\_drives}}_i \cdot x_i \leq \text{\texttt{max\_disk}}, & \text{(Disk drives availability constraint)} \\
    & \text{\texttt{min\_mem}} \leq \sum_{i=1}^{N} y_i \leq \text{\texttt{max\_mem}}, & \text{(256K memory availability constraint)} \\
    & \sum_{i=1}^{N} z_i \leq \text{\texttt{alt\_mem}}, & \text{(Alternative memory boards availability constraint)} \\
    & x_i \leq \text{\texttt{demand}}_i, & \forall i \quad \text{(Demand constraint)} \\
    & \sum_{i \in \text{GP}} x_i \leq \text{\texttt{demand\_GP}}, & \text{(GP demand constraint)} \\
    & \sum_{i \in \text{WS}} x_i \leq \text{\texttt{demand\_WS}}, & \text{(WS demand constraint)} \\
    & x_i \geq \text{\texttt{preorder}}_i, & \forall i \quad \text{(Preorder constraint)} \\
    & y_i = \text{\texttt{256K\_boards}}_i \cdot x_i, & \forall i \quad \text{(Memory usage constraint)} \\
\end{align*}

\textbf{Note:} The variable \( z_i \) should be binary if only certain systems can use alternative memory. The set \(\text{GP}\) and \(\text{WS}\) refer to systems that are general-purpose and workstations respectively, identified by the \text{\texttt{is\_workstation}} parameter.

\end{document}
```

This model aims to maximize the total profit by deciding how many of each computer system DEC should produce. The model considers constraints on resources such as CPUs, disk drives, and memory boards, as well as demand and preorders.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Model for DEC Production Optimization}

\textbf{Sets and Indices:}
\begin{align*}
    i & : \text{Index for computer systems,} \quad i = 1, \ldots, N.
\end{align*}

\textbf{Parameters:}
\begin{align*}
    \text{\texttt{price}}_i & : \text{Price of system } i. \\
    \text{\texttt{disk\_drives}}_i & : \text{Average units of disk drives requested for system } i. \\
    \text{\texttt{256K\_boards}}_i & : \text{Average units of 256K memory boards used by system } i. \\
    \text{\texttt{max\_cpu}} & : \text{Maximum units of CPU available.} \\
    \text{\texttt{min\_disk}}, \text{\texttt{max\_disk}} & : \text{Minimum and maximum units of disk drives available.} \\
    \text{\texttt{min\_mem}}, \text{\texttt{max\_mem}} & : \text{Minimum and maximum units of 256K memory boards available.} \\
    \text{\texttt{demand}}_i & : \text{Maximum demand for system } i. \\
    \text{\texttt{demand\_GP}}, \text{\texttt{demand\_WS}} & : \text{Maximum demand for GP and WS systems.} \\
    \text{\texttt{preorder}}_i & : \text{Pre-orders for system } i. \\
    \text{\texttt{alt\_mem}} & : \text{Units of alternative memory boards available.} \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
    x_i & : \text{Number of systems of type } i \text{ to produce (continuous).} \\
    y_i & : \text{Number of 256K memory boards used by system } i. \\
    z_i & : \text{Number of alternative memory boards used by system } i \text{ (binary)}.
\end{align*}

\textbf{Objective Function:}
\[
\max \sum_{i=1}^{N} \text{\texttt{price}}_i \cdot x_i
\]

\textbf{Constraints:}
\begin{align*}
    & \sum_{i=1}^{N} x_i \leq \text{\texttt{max\_cpu}}, & \text{(CPU availability constraint)} \\
    & \text{\texttt{min\_disk}} \leq \sum_{i=1}^{N} \text{\texttt{disk\_drives}}_i \cdot x_i \leq \text{\texttt{max\_disk}}, & \text{(Disk drives availability constraint)} \\
    & \text{\texttt{min\_mem}} \leq \sum_{i=1}^{N} y_i \leq \text{\texttt{max\_mem}}, & \text{(256K memory availability constraint)} \\
    & \sum_{i=1}^{N} z_i \leq \text{\texttt{alt\_mem}}, & \text{(Alternative memory boards availability constraint)} \\
    & x_i \leq \text{\texttt{demand}}_i, & \forall i \quad \text{(Demand constraint)} \\
    & \sum_{i \in \text{GP}} x_i \leq \text{\texttt{demand\_GP}}, & \text{(GP demand constraint)} \\
    & \sum_{i \in \text{WS}} x_i \leq \text{\texttt{demand\_WS}}, & \text{(WS demand constraint)} \\
    & x_i \geq \text{\texttt{preorder}}_i, & \forall i \quad \text{(Preorder constraint)} \\
    & y_i = \text{\texttt{256K\_boards}}_i \cdot x_i, & \forall i \quad \text{(Memory usage constraint)} \\
\end{align*}

\textbf{Note:} The variable \( z_i \) should be binary if only certain systems can use alternative memory. The set \(\text{GP}\) and \(\text{WS}\) refer to systems that are general-purpose and workstations respectively, identified by the \text{\texttt{is\_workstation}} parameter.

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided
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

#### Create the problem
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  #### Continuous
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0)  #### Continuous
z = pulp.LpVariable.dicts("z", range(data['N']), cat='Binary')  #### Binary

#### Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

#### Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU_Constraint"
problem += (data['MinDisk'] <= pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Drive_Constraint")
problem += (data['MinMemory'] <= pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Constraint")
problem += pulp.lpSum(z[i] for i in range(data['N'])) <= data['AltMemory'], "Alternative_Memory_Constraint"

for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"
    problem += y[i] == data['MemoryBoards'][i] * x[i], f"Memory_Usage_Constraint_{i}"

#### GP and WS Constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS_Demand_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

