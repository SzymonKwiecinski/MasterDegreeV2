import pulp

# Input Data
data = {
    "available": [240000, 8000, 75000],
    "requirements": [
        [48, 1, 10],
        [40, 1, 10],
        [0, 1, 2]
    ],
    "prices": [40, 38, 9],
    "costs": [30, 26, 7],
    "demands": [10000, 2000, 10000]
}

available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products
M = len(prices)
# Number of materials
N = len(available)

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: amount of each product produced
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, upBound=demands[j], cat='Continuous') for j in range(M)]

# Define the objective function: maximize total profit
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum([profit[j] * amount[j] for j in range(M)])

# Define the constraints: ensure the availability of raw materials is not exceeded
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i]

# Solve the problem
problem.solve()

# Output formatting
output = {
    "amount": [pulp.value(amount[j]) for j in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')