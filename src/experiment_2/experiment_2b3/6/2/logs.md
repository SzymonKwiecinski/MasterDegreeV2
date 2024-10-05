# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
<DATA>
{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load the data
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

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_compatible = data['AltCompatible']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_mem = data['AltMemory']

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
alt_used = [pulp.LpVariable(f'alt_used_{i}', lowBound=0, cat='Continuous') if alt_compatible[i] else 0 for i in range(N)]

#### Objective function
profit = pulp.lpSum([price[i] * x[i] for i in range(N)])
problem += profit, "Total_Profit"

#### Constraints
problem += pulp.lpSum(x) <= max_cpu, "CPU_Constraint"
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk, "Min_Disk_Constraint"
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk, "Max_Disk_Constraint"
problem += pulp.lpSum([memory_boards[i] * x[i] - alt_used[i] for i in range(N)]) >= min_mem, "Min_Mem_Constraint"
problem += pulp.lpSum([memory_boards[i] * x[i] - alt_used[i] for i in range(N)]) <= max_mem, "Max_Mem_Constraint"
problem += pulp.lpSum([alt_used[i] for i in range(N) if alt_compatible[i]]) <= alt_mem, "Alt_Mem_Constraint"

#### Demand constraints
for i in range(N):
    problem += x[i] <= demand[i] + preorder[i], f"Demand_Constraint_{i}"
    if preorder[i] > 0:
        problem += x[i] >= preorder[i], f"Preorder_Constraint_{i}"

#### Total demand for GP and WS systems
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_gp, "Total_GP_Demand"
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_ws, "Total_WS_Demand"

#### Solve the problem
problem.solve()

#### Prepare the output data
output_data = {
    "system_output": [
        {
            "num_produced": pulp.value(x[i]),
            "total_256K_boards_used": pulp.value(memory_boards[i] * x[i] - alt_used[i]) if alt_compatible[i] else pulp.value(memory_boards[i] * x[i]),
            "total_alt_boards_used": pulp.value(alt_used[i]) if alt_compatible[i] else 0,
            "total_disk_drives_used": pulp.value(disk_drives[i] * x[i])
        }
        for i in range(N)
    ],
    "profit": pulp.value(problem.objective)
}

#### Print the result
print(json.dumps(output_data, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

