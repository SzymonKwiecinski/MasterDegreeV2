import pulp
import json

# Data input
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the problem
problem = pulp.LpProblem("Maximize_Z", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Objective"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')