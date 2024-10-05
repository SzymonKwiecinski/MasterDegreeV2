import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Unpacking data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and raw materials
M = len(prices)
N = len(available)

# Problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
profit = pulp.lpSum([(prices[j] - costs[j]) * x[j] for j in range(M)])
problem += profit

# Constraints
# Material constraints
for i in range(N):
    problem += pulp.lpSum([requirements[i][j] * x[j] for j in range(M)]) <= available[i]

# Demand constraints
for j in range(M):
    problem += x[j] <= demands[j]

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for j in range(M):
    print(f'Amount of product {j+1} to produce: {x[j].varValue}')