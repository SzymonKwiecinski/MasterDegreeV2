import pulp
import json

# Data input
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], 
                        [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Problem definition
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("Amount", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Resource_Constraint_{i}"

# Solve the problem
problem.solve()

# Output result
amount_produced = [amounts[j].varValue for j in range(M)]
output = {"amount": amount_produced}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')