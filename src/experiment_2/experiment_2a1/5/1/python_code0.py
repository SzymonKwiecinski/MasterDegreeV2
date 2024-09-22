import pulp
import json

# Input data
data = {
    'M': 4, 
    'N': 5, 
    'Available': [10, 20, 15, 35, 25], 
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
    'Prices': [7, 10, 5, 9]
}

# Extracting data from the input
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M)), "Total_Revenue"

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"Available_Resource_{i}"

# Solve the problem
problem.solve()

# Output the results
amounts_produced = [amount[j].varValue for j in range(M)]
result = {"amount": amounts_produced}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')