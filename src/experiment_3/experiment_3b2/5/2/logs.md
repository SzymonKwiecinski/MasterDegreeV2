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
To model this problem as a Mixed-Integer Programming (MIP) problem, we need to define decision variables, an objective function, and constraints based on the information provided.

Here's the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( i \in \{1, \ldots, N\} \): Index for computer systems.
    \item \( \text{GP}, \text{WS} \): Sets for general-purpose and workstation systems respectively.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_i \): Price of system \( i \).
    \item \( \text{disk}_i \): Average units of disk drive requested for system \( i \).
    \item \( \text{mem}_i \): Average units of 256K memory boards used by system \( i \).
    \item \( \text{max\_cpu} \): Maximum units of CPUs available.
    \item \( \text{min\_disk}, \text{max\_disk} \): Range of available disk drives.
    \item \( \text{min\_mem}, \text{max\_mem} \): Range of available 256K memory boards.
    \item \( \text{demand}_i \): Maximum demand for system \( i \).
    \item \( \text{demand\_GP}, \text{demand\_WS} \): Maximum demand for GP and WS systems.
    \item \( \text{preorder}_i \): Preorders for system \( i \) to be fulfilled.
    \item \( \text{alt\_mem} \): Units of alternative memory boards available.
    \item \( \text{alt\_compatible}_i \): Boolean indicating if system \( i \) can use alternative memory.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \): Number of systems \( i \) to produce (continuous).
    \item \( \text{mem\_used}_i \): Total 256K memory boards used by system \( i \).
    \item \( \text{alt\_used}_i \): Total alternative boards used by system \( i \) (if compatible).
    \item \( \text{disk\_used}_i \): Total disk drives used by system \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \times x_i
\]

\subsection*{Constraints}
\begin{align}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} & \text{(CPU availability)} \\
    & \sum_{i=1}^{N} \text{disk}_i \times x_i \leq \text{max\_disk} & \text{(Disk drive upper limit)} \\
    & \sum_{i=1}^{N} \text{disk}_i \times x_i \geq \text{min\_disk} & \text{(Disk drive lower limit)} \\
    & \sum_{i=1}^{N} \text{mem\_used}_i \leq \text{max\_mem} & \text{(256K memory board upper limit)} \\
    & \sum_{i=1}^{N} \text{mem\_used}_i \geq \text{min\_mem} & \text{(256K memory board lower limit)} \\
    & \sum_{i \in \text{GP}} x_i \leq \text{demand\_GP} & \text{(GP systems demand)} \\
    & \sum_{i \in \text{WS}} x_i \leq \text{demand\_WS} & \text{(WS systems demand)} \\
    & x_i \leq \text{demand}_i & \forall i \text{ (Demand for system \( i \))} \\
    & x_i \geq \text{preorder}_i & \forall i \text{ (Preorders)}

\end{align}

For alternative memory usage:
\begin{align}
    & \text{alt\_used}_i = 0, & \text{if }\text{alt\_compatible}_i = \text{false} \\
    & \sum_{i=1}^{N} \text{alt\_used}_i \leq \text{alt\_mem} & \text{(Alternative memory limit)}
\end{align}

\end{document}
```

This model seeks to maximize profit by determining the optimal production quantities of each system while adhering to resource constraints and demand projections.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( i \in \{1, \ldots, N\} \): Index for computer systems.
    \item \( \text{GP}, \text{WS} \): Sets for general-purpose and workstation systems respectively.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_i \): Price of system \( i \).
    \item \( \text{disk}_i \): Average units of disk drive requested for system \( i \).
    \item \( \text{mem}_i \): Average units of 256K memory boards used by system \( i \).
    \item \( \text{max\_cpu} \): Maximum units of CPUs available.
    \item \( \text{min\_disk}, \text{max\_disk} \): Range of available disk drives.
    \item \( \text{min\_mem}, \text{max\_mem} \): Range of available 256K memory boards.
    \item \( \text{demand}_i \): Maximum demand for system \( i \).
    \item \( \text{demand\_GP}, \text{demand\_WS} \): Maximum demand for GP and WS systems.
    \item \( \text{preorder}_i \): Preorders for system \( i \) to be fulfilled.
    \item \( \text{alt\_mem} \): Units of alternative memory boards available.
    \item \( \text{alt\_compatible}_i \): Boolean indicating if system \( i \) can use alternative memory.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_i \): Number of systems \( i \) to produce (continuous).
    \item \( \text{mem\_used}_i \): Total 256K memory boards used by system \( i \).
    \item \( \text{alt\_used}_i \): Total alternative boards used by system \( i \) (if compatible).
    \item \( \text{disk\_used}_i \): Total disk drives used by system \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{i=1}^{N} \text{price}_i \times x_i
\]

\subsection*{Constraints}
\begin{align}
    & \sum_{i=1}^{N} x_i \leq \text{max\_cpu} & \text{(CPU availability)} \\
    & \sum_{i=1}^{N} \text{disk}_i \times x_i \leq \text{max\_disk} & \text{(Disk drive upper limit)} \\
    & \sum_{i=1}^{N} \text{disk}_i \times x_i \geq \text{min\_disk} & \text{(Disk drive lower limit)} \\
    & \sum_{i=1}^{N} \text{mem\_used}_i \leq \text{max\_mem} & \text{(256K memory board upper limit)} \\
    & \sum_{i=1}^{N} \text{mem\_used}_i \geq \text{min\_mem} & \text{(256K memory board lower limit)} \\
    & \sum_{i \in \text{GP}} x_i \leq \text{demand\_GP} & \text{(GP systems demand)} \\
    & \sum_{i \in \text{WS}} x_i \leq \text{demand\_WS} & \text{(WS systems demand)} \\
    & x_i \leq \text{demand}_i & \forall i \text{ (Demand for system \( i \))} \\
    & x_i \geq \text{preorder}_i & \forall i \text{ (Preorders)}

\end{align}

For alternative memory usage:
\begin{align}
    & \text{alt\_used}_i = 0, & \text{if }\text{alt\_compatible}_i = \text{false} \\
    & \sum_{i=1}^{N} \text{alt\_used}_i \leq \text{alt\_mem} & \text{(Alternative memory limit)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(1, data['N'] + 1), lowBound=0)  #### Number of systems to produce

#### Objective Function
problem += pulp.lpSum(data['Price'][i - 1] * x[i] for i in range(1, data['N'] + 1)), "Total_Profit"

#### Constraints
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1)) <= data['MaxCpu'], "CPU_Availability"
problem += pulp.lpSum(data['DiskDrives'][i - 1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxDisk'], "Disk_Upper_Limit"
problem += pulp.lpSum(data['DiskDrives'][i - 1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinDisk'], "Disk_Lower_Limit"
problem += pulp.lpSum(data['MemoryBoards'][i - 1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxMemory'], "Memory_Upper_Limit"
problem += pulp.lpSum(data['MemoryBoards'][i - 1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinMemory'], "Memory_Lower_Limit"
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['IsWorkstation'][i - 1]) <= data['DemandWS'], "WS_Systems_Demand"
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if not data['IsWorkstation'][i - 1]) <= data['DemandGP'], "GP_Systems_Demand"
for i in range(1, data['N'] + 1):
    problem += x[i] <= data['Demand'][i - 1], f"Demand_for_system_{i}"
    problem += x[i] >= data['Preorder'][i - 1], f"Preorders_for_system_{i}"

#### Alternative memory constraints
problem += pulp.lpSum((data['MemoryBoards'][i - 1] if data['AltCompatible'][i - 1] else 0) * x[i] for i in range(1, data['N'] + 1)) <= data['AltMemory'], "Alternative_Memory_Limit"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

