import pulp

# Data from the JSON
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}

# Unpacking the data
M = data['M']  # Number of goods
N = data['N']  # Number of raw materials
available = data['Available']  # Available amount of each raw material
requirements = data['Requirements']  # Requirements matrix
prices = data['Prices']  # Prices for each good

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define variables for the amount of each good to produce
amount_vars = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective: Maximize the total revenue
problem += pulp.lpSum(prices[j] * amount_vars[j] for j in range(M))

# Constraints: Ensure the materials used do not exceed the available resources
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount_vars[j] for j in range(M)) <= available[i]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "amount": [pulp.value(amount_vars[j]) for j in range(M)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')