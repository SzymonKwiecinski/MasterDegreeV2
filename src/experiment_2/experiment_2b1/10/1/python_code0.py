import pulp
import json

# Input data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}

# Parameters
M = data['M']  # number of goods
N = data['N']  # number of raw materials
available = data['Available']  # availability of raw materials
requirements = data['Requirements']  # requirements for each good
prices = data['Prices']  # prices of each good

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M)), "Total Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Material_{i}"

# Solve the problem
problem.solve()

# Output the amounts produced
output = {"amount": [amounts[j].varValue for j in range(M)]}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')