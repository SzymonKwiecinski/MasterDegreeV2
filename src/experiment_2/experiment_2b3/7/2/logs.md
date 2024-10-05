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

#### Data input
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

#### Initialize the problem
problem = pulp.LpProblem("DEC_Production", pulp.LpMaximize)

#### Decision variables
num_produced = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
total_alt_boards_used = [pulp.LpVariable(f'alt_{i}', lowBound=0, cat='Continuous') for i in range(N)]

#### Objective Function: Maximize profit
profit = pulp.lpSum((price[i] * num_produced[i]) for i in range(N))
problem += profit

#### Constraints

#### CPU availability
problem += pulp.lpSum(num_produced[i] for i in range(N)) <= max_cpu

#### Disk drive constraints
total_disk_drives = pulp.lpSum(disk_drives[i] * num_produced[i] for i in range(N))
problem += total_disk_drives >= min_disk
problem += total_disk_drives <= max_disk

#### Memory board constraints
total_memory_boards = pulp.lpSum(memory_boards[i] * num_produced[i] for i in range(N))
total_standard_boards = total_memory_boards - pulp.lpSum(total_alt_boards_used[i] for i in range(N))
problem += total_standard_boards >= min_mem
problem += total_standard_boards <= max_mem

#### Alternative memory constraints
for i in range(N):
    if alt_compatible[i]:
        problem += total_alt_boards_used[i] <= num_produced[i] * memory_boards[i]
    else:
        problem += total_alt_boards_used[i] == 0

#### Alternative memory supply constraint
problem += pulp.lpSum(total_alt_boards_used[i] for i in range(N)) <= alt_mem

#### Demand and preorder constraints
for i in range(N):
    problem += num_produced[i] >= preorder[i]
    problem += num_produced[i] <= demand[i]

#### Total GP and WS demand constraints
problem += pulp.lpSum(num_produced[i] for i in range(N) if not is_workstation[i]) <= demand_gp
problem += pulp.lpSum(num_produced[i] for i in range(N) if is_workstation[i]) <= demand_ws

#### Solve the problem
problem.solve()

#### Prepare the output
system_output = [
    {
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": pulp.value(num_produced[i]) * memory_boards[i] - pulp.value(total_alt_boards_used[i]),
        "total_alt_boards_used": pulp.value(total_alt_boards_used[i]),
        "total_disk_drives_used": pulp.value(num_produced[i]) * disk_drives[i]
    }
    for i in range(N)
]

profit_value = pulp.value(profit)

output = {
    "system_output": system_output,
    "profit": profit_value
}

#### Print the results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

