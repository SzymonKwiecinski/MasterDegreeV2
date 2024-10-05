import pulp

# Data from JSON input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Number of files
N = len(sizes)

# Create a problem
problem = pulp.LpProblem("Minimize_the_number_of_floppy_disks_used", pulp.LpMinimize)

# Potential number of disks (at most N if each file needs its own disk)
max_disks = N

# Decision variables
x = pulp.LpVariable.dicts("disk_usage", (range(max_disks), range(N)), cat='Binary')
y = pulp.LpVariable.dicts("disk_active", range(max_disks), cat='Binary')

# Objective: Minimize the number of disks used
problem += pulp.lpSum(y[d] for d in range(max_disks))

# Constraints
for j in range(N):
    # Each file must be stored in exactly one disk
    problem += pulp.lpSum(x[d][j] for d in range(max_disks)) == 1

for d in range(max_disks):
    # The total size of files on each disk cannot exceed its capacity
    problem += pulp.lpSum(x[d][j] * sizes[j] for j in range(N)) <= capacity * y[d]

# Solve the problem
problem.solve()

# Extract results
n_disks = sum(y[d].varValue for d in range(max_disks))
whichdisk = [next(d for d in range(max_disks) if x[d][j].varValue == 1) for j in range(N)]

# Output
solution = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')