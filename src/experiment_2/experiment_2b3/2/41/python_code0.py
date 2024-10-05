import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Problem
problem = pulp.LpProblem("Minimize_Disks", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((j, d) for j in range(N) for d in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (d for d in range(N)), cat='Binary')

# Objective: Minimize number of disks used
problem += pulp.lpSum(y[d] for d in range(N))

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[j, d] for d in range(N)) == 1

for d in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[j, d] for j in range(N)) <= capacity * y[d]

# Solve
problem.solve()

# Retrieve Results
n_disks = int(pulp.value(problem.objective))
whichdisk = [None] * N

for j in range(N):
    for d in range(N):
        if pulp.value(x[j, d]) == 1:
            whichdisk[j] = d
            break

# Output
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')