import pulp

# Data input
data = {
    "available": [240000, 8000, 75000],
    "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

# Extract data
available = data["available"]
requirements = data["requirements"]
prices = data["prices"]
costs = data["costs"]
demands = data["demands"]

# Number of materials and products
N = len(available)
M = len(prices)

# Problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision variables: amount produced for each product
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit

# Constraints
# Material availability constraints
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Gather results
solution = {
    "amount": [pulp.value(amount[j]) for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')