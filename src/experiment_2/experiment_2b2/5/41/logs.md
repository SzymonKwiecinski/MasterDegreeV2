# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP
PROBLEM INFO:

- Before going on vacation you want to make floppy disk backups of important files. 
- You have at your disposal several blank floppy disks with capacities of \var{capacity} GB. 
- They are given the size of the files that you want to save.
- Each file \var{j} has size \var{size_{j}}.
- Assuming that you do not have any programs to compress the data and that you have enough floppy disks available for back up everything.

INPUT FORMAT:

{
	"capacity": capacity,
	"size": [size_{j} for j in 1,...,N]
}

OBJECTIVE: How to distribute these files on the floppy disks in order to minimize the number of floppy disks used.

OUTPUT INFO:

- \var{n_disks} represents the total number of floppy disks used
- \var{whichdisk} represents on which disk each file is distributed. Its length is determined by \var{n_disks}

OUTPUT FORMAT:

{
	"n_disks": n_disks,
	"whichdisk": [disk_{j} for j in 1,...,N]
}
</DESCRIPTION>
<DATA>
{'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
num_files = len(sizes)

#### Problem
problem = pulp.LpProblem("Minimum_Disks_Backup", pulp.LpMinimize)

#### Variables
n_disks = pulp.LpVariable('n_disks', lowBound=0, cat='Integer')
assignments = pulp.LpVariable.dicts('disk_assign', ((i, j) for i in range(num_files) for j in range(num_files)), cat='Binary')
disks_used = pulp.LpVariable.dicts('disk_used', (j for j in range(num_files)), cat='Binary')

#### Objective
problem += n_disks

#### Constraints
for i in range(num_files):
    problem += pulp.lpSum(assignments[i, j] for j in range(num_files)) == 1

for j in range(num_files):
    problem += pulp.lpSum(assignments[i, j] * sizes[i] for i in range(num_files)) <= capacity * disks_used[j]

problem += pulp.lpSum(disks_used[j] for j in range(num_files)) == n_disks

#### Solve
problem.solve()

#### Extract solution
n_disks_value = int(pulp.value(n_disks))
whichdisk = [-1] * num_files

disk_indices = [j for j in range(num_files) if pulp.value(disks_used[j]) > 0.5]

for i in range(num_files):
    for j in disk_indices:
        if pulp.value(assignments[i, j]) > 0.5:
            whichdisk[i] = disk_indices.index(j)
            break

#### Output
result = {
    "n_disks": n_disks_value,
    "whichdisk": whichdisk
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

