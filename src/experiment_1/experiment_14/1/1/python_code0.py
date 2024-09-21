import pulp

# Data
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

# Create the model
problem = pulp.LpProblem("Maximize_Firm_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i+1}", lowBound=0, cat='Continuous') for i in range(data['M'])]

# Objective function
problem += pulp.lpSum(data['Prices'][i] * x[i] for i in range(data['M'])), "Total_Revenue"

# Constraints
# Raw material availability constraints
for j in range(data['N']):
    problem += pulp.lpSum(data['Requirements'][i][j] * x[i] for i in range(data['M'])) <= data['Available'][j], f"Material_{j+1}_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')