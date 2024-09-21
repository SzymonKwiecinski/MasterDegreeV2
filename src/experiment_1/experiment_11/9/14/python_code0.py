import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
Capacity = data['capacity']
Size = data['size']

# Create the problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')  # x[i][j]: file j on disk i
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')  # y[i]: disk i used

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Total_Disks_Used"

# Constraints
# Constraint 1: The sum of file sizes on each floppy disk cannot exceed the capacity
for i in range(N):
    problem += pulp.lpSum(Size[j] * x[i][j] for j in range(N)) <= Capacity * y[i], f"Capacity_Constraint_{i}"

# Constraint 2: Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"File_Placement_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')