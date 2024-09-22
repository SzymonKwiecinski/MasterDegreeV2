import pulp
import json

# Data input in JSON format
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}

# Extracting data for the problem
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for the amount of each good produced
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0) for j in range(M)]

# Objective function: Maximize total revenue
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M))

# Constraints for the resource availability
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"ResourceConstraint_{i}"

# Solve the problem
problem.solve()

# Output: the amount of each good produced
amounts_output = [amounts[j].varValue for j in range(M)]
output = {"amount": amounts_output}

# Printing the result
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')