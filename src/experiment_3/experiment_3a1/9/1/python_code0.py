import pulp
import json

# Data
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Resource_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the results
amounts = [x[j].varValue for j in range(M)]
print(f"Amount produced: {amounts}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')