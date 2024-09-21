import pulp

# Data from the provided JSON
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], 
                     [0, 5, 2, 1, 0], 
                     [1, 0, 0, 5, 3], 
                     [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

# Define the problem
problem = pulp.LpProblem("Maximize_Total_Revenue", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['M']), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Prices'][i] * x[i] for i in range(data['M']))

# Constraints
for j in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][i][j] * x[i] for i in range(data['M'])) <= data['Available'][j], 
                 f"Raw_Material_Constraint_{j}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')