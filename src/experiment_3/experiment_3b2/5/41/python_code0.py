import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
M = N  # Assuming M = N as stated

# Create the problem
problem = pulp.LpProblem("Disk_Packing_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(1, M + 1) for j in range(1, N + 1)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(1, M + 1), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(1, M + 1)), "Minimize_Disk_Usage"

# Constraints
# Each file must be placed on exactly one disk
for j in range(1, N + 1):
    problem += pulp.lpSum(x[i, j] for i in range(1, M + 1)) == 1, f"File_{j}_placement"

# Respect disk capacity
for i in range(1, M + 1):
    problem += pulp.lpSum(data['size'][j - 1] * x[i, j] for j in range(1, N + 1)) <= data['capacity'] * y[i], f"Disk_{i}_capacity"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')