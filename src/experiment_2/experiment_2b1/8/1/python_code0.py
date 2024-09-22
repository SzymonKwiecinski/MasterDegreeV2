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

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Define the objective function
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M))

# Define constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"Material_{i}")

# Solve the problem
problem.solve()

# Output the amounts produced
amounts_produced = [amount[j].varValue for j in range(M)]
output = {
    "amount": amounts_produced
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')