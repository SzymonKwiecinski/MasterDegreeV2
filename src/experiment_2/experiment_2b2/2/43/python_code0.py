import pulp

# Problem Input
data = {
    "available": [240000, 8000, 75000],
    "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

# Extracting data
available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
costs = data["costs"]
demands = data["demands"]

# Number of products
M = len(prices)
# Number of raw materials
N = len(available)

# Initialize the problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables for amount to produce of each product
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective Function: Maximize total profit
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum([profit[j] * amount[j] for j in range(M)])

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Output result
amount_produced = [pulp.value(amount[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

output = {
    "amount": amount_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')