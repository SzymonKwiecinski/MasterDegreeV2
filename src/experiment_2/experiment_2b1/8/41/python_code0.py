import pulp
import json

data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the LP problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
# x[i][j] is 1 if file j is placed on disk i, 0 otherwise
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# y[i] is 1 if disk i is used, 0 otherwise
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeDisks"

# Constraints for file assignment
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"FileAssigned_{j}"

# Constraints for disk capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"DiskCapacity_{i}"

# Solve the problem
problem.solve()

# Prepare the output
n_disks = sum(pulp.value(y[i]) for i in range(N))
whichdisk = [next(i for i in range(N) if pulp.value(x[i][j]) == 1) for j in range(N)]

# Print the results
result = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')