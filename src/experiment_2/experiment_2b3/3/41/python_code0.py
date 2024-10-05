import pulp

# Data extracted from the JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Problem setup
problem = pulp.LpProblem("Disk_Minimization", pulp.LpMinimize)

# Constants
capacity = data['capacity']
sizes = data['size']
N = len(sizes)  # Number of files

# Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective: Minimize number of disks used
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
# 1. Each file must be stored in exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(N)) == 1

# 2. The total size of files on each disk i should not exceed the disk capacity
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] * sizes[j] for j in range(N)) <= capacity * y[i]

# Solving the problem
problem.solve()

# Results
n_disks = sum(y[i].varValue for i in range(N))
whichdisk = [next(i for i in range(N) if pulp.value(x[(i, j)]) == 1) for j in range(N)]

output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')