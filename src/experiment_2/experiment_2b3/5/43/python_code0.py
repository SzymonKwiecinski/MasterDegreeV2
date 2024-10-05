import pulp

# Data input
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Unpack the data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and raw materials
M = len(prices)
N = len(available)

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: Maximize Profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints
# Raw Material Constraints
for i in range(N):
    problem += (pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]), f'Material_{i+1}_Availability'

# Demand Constraints
for j in range(M):
    problem += (amount[j] <= demands[j]), f'Demand_{j+1}_Constraint'

# Solve the problem
problem.solve()

# Results
amount_values = [pulp.value(amount[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "amount": amount_values,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')