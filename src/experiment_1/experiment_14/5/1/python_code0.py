import pulp

# Data from JSON
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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Firm_Revenue", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(1, data['M'] + 1)]

# Objective function: Maximize total revenue
problem += pulp.lpSum([data['Prices'][i] * x[i] for i in range(data['M'])])

# Constraints
# Raw material availability constraints
for j in range(data['N']):
    problem += pulp.lpSum([data['Requirements'][i][j] * x[i] for i in range(data['M'])]) <= data['Available'][j]

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')