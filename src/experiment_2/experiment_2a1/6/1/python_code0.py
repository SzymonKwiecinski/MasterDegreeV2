import pulp
import json

# Input data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25],
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
        'Prices': [7, 10, 5, 9]}

# Extracting parameters from data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0) for j in range(M)]

# Define the objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M))

# Define the constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i]), f'Constraint_{i}'

# Solve the problem
problem.solve()

# Prepare the output
amounts_result = [amounts[j].varValue for j in range(M)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the amounts
output = {
    "amount": amounts_result
}
print(json.dumps(output))