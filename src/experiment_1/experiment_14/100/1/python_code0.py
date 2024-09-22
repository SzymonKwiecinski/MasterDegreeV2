import pulp

# Data provided
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

# Number of products and materials
M = data['M']
N = data['N']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(M)]

# Objective function
problem += pulp.lpSum(data['Prices'][i] * x[i] for i in range(M)), "Total Revenue"

# Constraints
# Raw material availability
for j in range(N):
    problem += (pulp.lpSum(data['Requirements'][i][j] * x[i] for i in range(M)) <= data['Available'][j], f"Material_{j}_Availability")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')