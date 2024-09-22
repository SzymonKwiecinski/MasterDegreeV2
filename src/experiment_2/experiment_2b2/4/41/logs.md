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

#### Parse the JSON input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

#### Create a problem instance
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

#### Define variable: if disk i is used
used = pulp.LpVariable.dicts("DiskUsed", range(N), cat='Binary')

#### Define variable: if file j is assigned to disk i
assign = pulp.LpVariable.dicts("Assign", [(j, i) for j in range(N) for i in range(N)], cat='Binary')

#### Objective function: minimize the number of disks used
problem += pulp.lpSum(used[i] for i in range(N))

#### Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(assign[(j, i)] for i in range(N)) == 1

#### Enforce capacity constraint on each disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * assign[(j, i)] for j in range(N)) <= capacity * used[i]

#### Solve the problem
problem.solve()

#### Determine the number of disks used
n_disks = sum(used[i].varValue for i in range(N))

#### Determine the disk to which each file is assigned
whichdisk = [sum(i * assign[(j, i)].varValue for i in range(N)) for j in range(N)]

#### Format the output
output = {
    "n_disks": int(n_disks),
    "whichdisk": [int(w) for w in whichdisk]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

