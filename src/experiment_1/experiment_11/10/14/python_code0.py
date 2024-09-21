import pulp
import json

# Data
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
capacity = data['capacity']
size = data['size']
N = len(size)

# Initialize the problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeFloppyDisks"

# Constraints
# Constraint 1: File sizes on each floppy disk cannot exceed capacity
for i in range(N):
    problem += (pulp.lpSum(size[j] * x[i, j] for j in range(N)) <= capacity * y[i]), f"CapacityConstraint_{i}"

# Constraint 2: Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += (pulp.lpSum(x[i, j] for i in range(N)) == 1), f"FilePlacementConstraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')