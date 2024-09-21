import pulp

# Parse the input data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(1, M + 1)]

# Objective function
problem += pulp.lpSum([Prices[i] * x[i] for i in range(M)]), 'Total_Revenue'

# Constraints
for j in range(N):
    problem += pulp.lpSum([Requirements[i][j] * x[i] for i in range(M)]) <= Available[j], f'Resource_{j+1}_Constraint'

# Solve the problem
problem.solve()

# Output the result
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')