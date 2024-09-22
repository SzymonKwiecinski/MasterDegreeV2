import pulp

# Data from the JSON formatted input
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [
        [3, 2, 0, 0], 
        [0, 5, 2, 1], 
        [0, 0, 0, 5],
        [1, 0, 0, 0],
        [0, 3, 1, 1]
    ],
    'Prices': [7, 10, 5, 9]
}

# Extract data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Initialize LP model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{j+1}", lowBound=0) for j in range(M)]

# Objective function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Output the results
output = {"amount": [pulp.value(x[j]) for j in range(M)]}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')