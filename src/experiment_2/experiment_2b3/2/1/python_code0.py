import pulp

# Define the data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}

# Extract data
M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
problem += pulp.lpSum(Prices[j] * amount[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(Requirements[j][i] * amount[j] for j in range(M)) <= Available[i]

# Solve the problem
problem.solve()

# Prepare output
output = {'amount': [pulp.value(amount[j]) for j in range(M)]}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')