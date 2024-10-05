import pulp

# Parsing the data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

# Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define variables
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function - Maximize total revenue
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M))

# Constraints - Material availability constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Gather results
solution = {
    "amount": [pulp.value(amounts[j]) for j in range(M)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')