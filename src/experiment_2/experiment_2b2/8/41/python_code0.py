from pulp import LpProblem, LpVariable, lpSum, LpMinimize
import pulp

# Data from the problem
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Extracting sizes and capacity
file_sizes = data['size']
capacity = data['capacity']
N = len(file_sizes)  # Number of files
max_disks = N  # The maximum number of disks needed, each file on a separate disk

# Create the problem
problem = LpProblem("Minimize_Disks_Used", LpMinimize)

# Variables
# y[i] = 1 if disk i is used, 0 otherwise
y = LpVariable.dicts("DiskUsed", list(range(max_disks)), cat='Binary')

# x[i][j] = 1 if file j is placed on disk i, 0 otherwise
x = LpVariable.dicts("FileOnDisk", (range(max_disks), range(N)), cat='Binary')

# Objective
# Minimize the number of disks used
problem += lpSum(y[i] for i in range(max_disks)), "TotalDisksUsed"

# Constraints
# Each file must be on exactly one disk
for j in range(N):
    problem += lpSum(x[i][j] for i in range(max_disks)) == 1, f"File_{j}_On_One_Disk"

# The sum of the sizes of the files on each disk must not exceed the disk's capacity
for i in range(max_disks):
    problem += lpSum(x[i][j] * file_sizes[j] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_Disk_{i}"

# Solve the problem
problem.solve()

# Extracting results
n_disks = sum(y[i].varValue for i in range(max_disks))
whichdisk = [None] * N

for j in range(N):
    for i in range(max_disks):
        if x[i][j].varValue == 1:
            whichdisk[j] = i
            break

output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')