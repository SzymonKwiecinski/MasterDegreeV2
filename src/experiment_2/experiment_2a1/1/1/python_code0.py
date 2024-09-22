import pulp
import json

# Input data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 
        'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], 
                        [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M)), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i], f"Material_{i+1}_Constraint"

# Solve the problem
problem.solve()

# Output results
amount_produced = [amounts[j].varValue for j in range(M)]
output = {"amount": amount_produced}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')