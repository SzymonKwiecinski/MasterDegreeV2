import pulp

# Data from JSON
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
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Define the objective function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Total_Revenue"

# Add constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Print the outputs
print(f'Objective (Total Revenue): <OBJ>{pulp.value(problem.objective)}</OBJ>')

for j in range(M):
    print(f'x_{j} = {x[j].varValue}')