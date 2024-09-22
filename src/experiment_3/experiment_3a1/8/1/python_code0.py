import pulp

# Data from JSON format
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

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("goods", range(data['M']), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Prices'][j] * x[j] for j in range(data['M']))

# Constraints
for i in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][i][j] * x[j] for j in range(data['M'])) <= data['Available'][i])

# Solve the problem
problem.solve()

# Output the results
produced_amounts = {j: x[j].varValue for j in range(data['M'])}
print("Produced amounts:", produced_amounts)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')