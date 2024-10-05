import pulp

# Data input
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Extract data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and materials
M = len(prices)
N = len(available)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Integer') for j in range(M)]

# Objective function
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Results
amounts = [pulp.value(amount[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

output = {
    "amount": amounts,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>') 