import pulp

# Data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [
        [3, 2, 0, 0],
        [0, 5, 2, 1],
        [1, 0, 0, 5],
        [0, 3, 1, 1],
        [0, 0, 3, 0]
    ],
    'Prices': [7, 10, 5, 9]
}

# Number of goods and materials
M = data['M']
N = data['N']

# Available materials and requirements
available = data['Available']
requirements = data['Requirements']

# Prices for each good
prices = data['Prices']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')