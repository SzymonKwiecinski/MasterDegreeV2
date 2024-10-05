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

#### Problem data
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

#### Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(data['N'])]
mem_used = [pulp.LpVariable(f"mem_used{i}", lowBound=0) for i in range(data['N'])]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used{i}", lowBound=0) for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used{i}", lowBound=0) for i in range(data['N'])]

#### Objective function: maximize profit
total_profit = pulp.lpSum([
    x[i] * data['Price'][i] for i in range(data['N'])
])
problem += total_profit

#### Constraints
#### Demand constraints for each system
for i in range(data['N']):
    problem += (x[i] <= data['Demand'][i], f"Demand_constraint_{i}")
    problem += (x[i] >= data['Preorder'][i], f"Preorder_constraint_{i}")

#### CPU constraint
problem += (pulp.lpSum(x) <= data['MaxCpu'], "CPU_supply_constraint")

#### Memory constraints
total_mem_used = pulp.lpSum([
    x[i] * data['MemoryBoards'][i] for i in range(data['N'])
])
problem += (total_mem_used >= data['MinMemory'], "Min_memory_constraint")
problem += (total_mem_used <= data['MaxMemory'], "Max_memory_constraint")

#### Alternative memory use constraint
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += (alt_mem_used[i] <= data['AltMemory'], f"Alt_memory_constraint_{i}")
    else:
        problem += (alt_mem_used[i] == 0, f"Alt_memory_constraint_{i}_not_compatible")

#### Disk drive constraints
total_disk_used = pulp.lpSum([
    x[i] * data['DiskDrives'][i] for i in range(data['N'])
])
problem += (total_disk_used >= data['MinDisk'], "Min_disk_constraint")
problem += (total_disk_used <= data['MaxDisk'], "Max_disk_constraint")

#### GP demand constraint
total_GP = pulp.lpSum([
    x[i] for i in range(data['N']) if not data['IsWorkstation'][i]
])
problem += (total_GP <= data['DemandGP'], "GP_demand_constraint")

#### WS demand constraint
total_WS = pulp.lpSum([
    x[i] for i in range(data['N']) if data['IsWorkstation'][i]
])
problem += (total_WS <= data['DemandWS'], "WS_demand_constraint")

#### Solve problem
problem.solve()

#### Prepare output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": pulp.value(mem_used[i]),
        "total_alt_boards_used": pulp.value(alt_mem_used[i]),
        "total_disk_drives_used": pulp.value(disk_used[i])
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(total_profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

