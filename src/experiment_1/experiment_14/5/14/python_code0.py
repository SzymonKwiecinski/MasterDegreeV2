import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("Floppy_Disk_Allocation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts('y', (i for i in range(N)), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i]

for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1

# Solve
problem.solve()

# Print the result
for i in range(N):
    if pulp.value(y[i]) == 1:
        print(f"Floppy disk {i + 1} is used and contains files:", end=' ')
        for j in range(N):
            if pulp.value(x[i, j]) == 1:
                print(f"file {j + 1}", end=' ')
        print()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')