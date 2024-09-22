import pulp

# Read the data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("MinimizeNumberOfFloppyDisks", pulp.LpMinimize)

# Decision variables
# x[i][j] = 1 if file j is on disk i; 0 otherwise
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)),
                          cat='Binary')

# y[i] = 1 if disk i is used; 0 otherwise
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective: Minimize the number of disks used
problem += pulp.lpSum([y[i] for i in range(N)])

# Constraint: Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum([x[i, j] for i in range(N)]) == 1

# Constraint: The total size of files on each disk cannot exceed the capacity
for i in range(N):
    problem += pulp.lpSum([sizes[j] * x[i, j] for j in range(N)]) <= capacity * y[i]

# Solve the problem
problem.solve()

# Extract the solution
whichdisk = [-1] * N
for j in range(N):
    for i in range(N):
        if pulp.value(x[i, j]) == 1:
            whichdisk[j] = i

# Calculate the total number of disks used
n_disks = sum(pulp.value(y[i]) for i in range(N))

# Output result
result = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(result)
# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')