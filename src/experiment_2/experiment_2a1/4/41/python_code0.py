import pulp
import json

data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Disks_Used", pulp.LpMinimize)

# Create binary decision variables for each file j and each disk i
x = pulp.LpVariable.dicts("disk", (range(N), range(N)), cat='Binary')

# Objective: Minimize the number of disks used
n_disks = pulp.LpVariable("n_disks", lowBound=1, cat='Integer')
problem += n_disks

# Constraints: A file j can only be placed on one disk
for j in range(N):
    problem += pulp.lpSum(x[j][i] for i in range(N)) == 1

# Constraints: The total size on each disk i cannot exceed the capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][i] for j in range(N)) <= capacity

# Define a constraint linking n_disks and the usage of disks
for i in range(N):
    problem += pulp.lpSum(x[j][i] for j in range(N)) <= n_disks

# Solve the problem
problem.solve()

# Collect results
n_disks_used = int(pulp.value(n_disks))
disk_assignment = [next(i for i in range(n_disks_used) if pulp.value(x[j][i]) == 1) for j in range(N)]

# Prepare output
output = {
    "n_disks": n_disks_used,
    "whichdisk": disk_assignment
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')