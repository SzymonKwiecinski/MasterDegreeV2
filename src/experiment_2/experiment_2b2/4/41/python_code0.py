import pulp

# Parse the JSON input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create a problem instance
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Define variable: if disk i is used
used = pulp.LpVariable.dicts("DiskUsed", range(N), cat='Binary')

# Define variable: if file j is assigned to disk i
assign = pulp.LpVariable.dicts("Assign", [(j, i) for j in range(N) for i in range(N)], cat='Binary')

# Objective function: minimize the number of disks used
problem += pulp.lpSum(used[i] for i in range(N))

# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(assign[(j, i)] for i in range(N)) == 1

# Enforce capacity constraint on each disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * assign[(j, i)] for j in range(N)) <= capacity * used[i]

# Solve the problem
problem.solve()

# Determine the number of disks used
n_disks = sum(used[i].varValue for i in range(N))

# Determine the disk to which each file is assigned
whichdisk = [sum(i * assign[(j, i)].varValue for i in range(N)) for j in range(N)]

# Format the output
output = {
    "n_disks": int(n_disks),
    "whichdisk": [int(w) for w in whichdisk]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')