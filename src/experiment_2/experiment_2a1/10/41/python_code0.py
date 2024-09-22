import pulp
import json

data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Unpack data
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the LP problem
problem = pulp.LpProblem("FloppyDiskAllocation", pulp.LpMinimize)

# Create binary variables for each file and each disk
x = pulp.LpVariable.dicts("file_on_disk", (range(N), range(N)), cat='Binary')

# Objective: Minimize the number of disks used
problem += pulp.lpSum([1 for d in range(N) if pulp.lpSum(x[j][d] for j in range(N)) > 0]), "MinimizeDisks"

# Constraint: Each file must be allocated to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][d] for d in range(N)) == 1, f"AssignFile_{j}"

# Constraint: The total size of files on each disk must not exceed the capacity
for d in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][d] for j in range(N)) <= capacity, f"DiskCapacity_{d}"

# Solve the problem
problem.solve()

# Extract the results
n_disks = int(pulp.value(problem.objective))
whichdisk = [next(d for d in range(N) if pulp.value(x[j][d]) == 1) for j in range(N)]

# Prepare the output
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

# Print the output and the objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')