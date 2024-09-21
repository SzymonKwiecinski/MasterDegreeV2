import pulp

# Data extracted from the JSON input
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

# Number of goods and raw materials
M = data['M']
N = data['N']

# Available amounts of raw materials
available = data['Available']

# Requirements of raw materials for each good
requirements = data['Requirements']

# Prices per good
prices = data['Prices']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i+1}', lowBound=0, cat='Continuous') for i in range(M)]

# Objective function
problem += pulp.lpSum(prices[i] * x[i] for i in range(M)), "Total Revenue"

# Constraints
for j in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[i] for i in range(M)) <= available[j], f"Raw_material_availability_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')