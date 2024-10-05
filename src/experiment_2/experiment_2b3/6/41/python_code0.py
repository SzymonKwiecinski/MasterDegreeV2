import pulp

# Parse the JSON data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Extract the inputs
capacity = data['capacity']
sizes = data['size']
N = len(sizes)  # number of files

# Maximum number of disks needed is at worst each file on a separate disk
max_disks = N

# Create the problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision variables
# y_d is 1 if disk d is used
y = pulp.LpVariable.dicts("disk_used", range(max_disks), cat='Binary')
# x_jd is 1 if file j is on disk d
x = pulp.LpVariable.dicts("file_on_disk", [(j, d) for j in range(N) for d in range(max_disks)], cat='Binary')

# Objective: Minimize the number of disks used
problem += pulp.lpSum([y[d] for d in range(max_disks)])

# Constraints
# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum([x[(j, d)] for d in range(max_disks)]) == 1

# The sum of sizes of files on each disk must not exceed the capacity of a disk
for d in range(max_disks):
    problem += pulp.lpSum([sizes[j] * x[(j, d)] for j in range(N)]) <= capacity * y[d]

# Solve the problem
problem.solve()

# Extract output data structure
n_disks = int(sum([pulp.value(y[d]) for d in range(max_disks)]))
whichdisk = [next(d for d in range(max_disks) if pulp.value(x[(j, d)]) == 1) for j in range(N)]

output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')