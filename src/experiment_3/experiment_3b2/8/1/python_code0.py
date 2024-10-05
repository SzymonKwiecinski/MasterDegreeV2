import pulp
import json

# Data in JSON format
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

# Extracting data from JSON
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Creating the LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Available_Constraint_{i}"

# Solving the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')