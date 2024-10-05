import pulp

# Input data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']
M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: amount of each product to produce
amount_vars = [pulp.LpVariable(f'amount_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: maximize total profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount_vars[j] for j in range(M)])
problem += profit

# Constraints: raw material availability
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount_vars[j] for j in range(M)]) <= available[i]

# Constraints: forecasted maximum demand
for j in range(M):
    problem += amount_vars[j] <= demands[j]

# Solve the problem
problem.solve()

# Collect results
amount = [pulp.value(amount_var) for amount_var in amount_vars]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "amount": amount,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')