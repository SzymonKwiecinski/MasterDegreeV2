import pulp
import json

# Data input
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}

# Extracting data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the Linear Program
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Create decision variables
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0) for j in range(M)]

# Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M)), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the result
amounts_result = [amounts[j].varValue for j in range(M)]

# Output the result
output = {"amount": amounts_result}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')