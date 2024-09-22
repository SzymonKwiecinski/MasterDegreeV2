import pulp
import json

# Data provided in JSON format
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

M = data['M']  # Number of goods
N = data['N']  # Number of raw materials
available = data['Available']  # Available amounts of raw materials
requirements = data['Requirements']  # Requirements of each good
prices = data['Prices']  # Prices of each good

# Create the problem variable
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for the amount of each good to produce
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M)), "Total_Revenue"

# Constraints based on available raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the results
amounts_output = [amounts[j].varValue for j in range(M)]
print(f'Output: {{"amount": {amounts_output}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')