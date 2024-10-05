import pulp

# Data from the problem
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [
        [3, 2, 0, 0, 0],
        [0, 5, 2, 1, 0],
        [1, 0, 0, 5, 3],
        [0, 3, 1, 1, 5]
    ],
    'Prices': [7, 10, 5, 9]
}

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Variables: amount_j for each product j
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(data['M'])]

# Objective function: Maximize total revenue
problem += pulp.lpSum([data['Prices'][j] * amount[j] for j in range(data['M'])])

# Constraints: Limit usage of each raw material i
for i in range(data['N']):
    problem += pulp.lpSum([data['Requirements'][j][i] * amount[j] for j in range(data['M'])]) <= data['Available'][i]

# Solve the problem
problem.solve()

# Output result
output = {
    "amount": [amount[j].varValue for j in range(data['M'])]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')