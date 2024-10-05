import pulp

# Parse the input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data["capacity"]
sizes = data["size"]
num_files = len(sizes)

# Define the problem
problem = pulp.LpProblem("Minimize_Disks_Used", pulp.LpMinimize)

# Variables
# x[i][j] is 1 if file i is on disk j, 0 otherwise
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(num_files) for j in range(num_files)), cat='Binary')

# y[j] is 1 if disk j is used, 0 otherwise
y = pulp.LpVariable.dicts("y", range(num_files), cat='Binary')

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(y[j] for j in range(num_files))

# Constraints
# Each file should be assigned to exactly one disk
for i in range(num_files):
    problem += pulp.lpSum(x[i, j] for j in range(num_files)) == 1

# Capacity constraints for each disk
for j in range(num_files):
    problem += pulp.lpSum(sizes[i] * x[i, j] for i in range(num_files)) <= capacity * y[j]

# Solve the problem
problem.solve()

# Prepare the output
n_disks = int(sum(y[j].varValue for j in range(num_files)))
whichdisk = [int(sum(j * x[i, j].varValue for j in range(num_files))) for i in range(num_files)]

# Output
result = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')