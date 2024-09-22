import pulp

# Load data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

N = len(available)  # Number of raw materials
M = len(prices)  # Number of products

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * x[j] for j in range(M)])
problem += profit

# Constraints

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * x[j] for j in range(M)]) <= available[i]

# Demand constraints
for j in range(M):
    problem += x[j] <= demands[j]

# Solve
problem.solve()

# Results
amount = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "amount": amount,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')