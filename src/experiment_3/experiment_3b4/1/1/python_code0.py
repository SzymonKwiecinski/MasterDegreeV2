import pulp

# Data provided
data = {
    'M': 4, 
    'N': 5, 
    'Available': [10, 20, 15, 35, 25], 
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 
    'Prices': [7, 10, 5, 9]
}

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(data['M'])]

# Objective Function
problem += pulp.lpSum(data['Prices'][j] * x[j] for j in range(data['M'])), "Total_Revenue"

# Constraints
for i in range(data['N']):
    problem += pulp.lpSum(data['Requirements'][j][i] * x[j] for j in range(data['M'])) <= data['Available'][i], f"Material_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')