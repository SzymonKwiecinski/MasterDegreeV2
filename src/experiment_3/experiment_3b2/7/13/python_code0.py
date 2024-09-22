import pulp
import json

# Load data
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_r", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=None, cat='Continuous')

# Objective function
problem += r, "Objective"

# Constraints
for i in range(M):
    norm_a_i = (sum(A[i][j]**2 for j in range(N)))**0.5  # L2 norm of a_i
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * norm_a_i) <= B[i], f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')