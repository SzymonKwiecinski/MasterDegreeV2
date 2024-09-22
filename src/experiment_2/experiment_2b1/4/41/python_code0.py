import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}  # Example data

capacity = data['capacity']
sizes = data['size']
num_files = len(sizes)

# Create a LP problem
problem = pulp.LpProblem("FloppyDiskAllocation", pulp.LpMinimize)

# Decision Variables
# x[i][j] = 1 if file i is assigned to disk j, otherwise 0
x = pulp.LpVariable.dicts("x", (range(num_files), range(num_files)), cat='Binary')

# Objective Function: Minimize number of disks used
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
problem += n_disks

# Constraints
# Each file must be assigned to exactly one disk
for i in range(num_files):
    problem += pulp.lpSum(x[i][j] for j in range(num_files)) == 1

# Capacity constraints for each disk
for j in range(num_files):
    problem += pulp.lpSum(sizes[i] * x[i][j] for i in range(num_files)) <= capacity

# Constraint to ensure n_disks is at least the number of disks used
for j in range(num_files):
    problem += n_disks >= pulp.lpSum(x[i][j] for i in range(num_files))

# Solve the problem
problem.solve()

# Prepare output
used_disks = [j for j in range(num_files) if pulp.value(n_disks) >= sum(x[i][j].varValue for i in range(num_files))]
whichdisk = [next(j for j in range(num_files) if x[i][j].varValue == 1) for i in range(num_files)]

output = {
    'n_disks': int(pulp.value(n_disks)),
    'whichdisk': whichdisk
}

# Print the output
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')