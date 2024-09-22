import pulp

# Data
available = [240000, 8000, 75000]
requirements = [[48, 1, 10], [40, 1, 10], [0, 1, 2]]
prices = [40, 38, 9]
costs = [30, 26, 7]
demands = [10000, 2000, 10000]

# Number of products
M = len(prices)
# Number of raw materials
N = len(available)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective Function
profit_contrib = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit_contrib[j] * amount[j] for j in range(M))

# Constraints

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i]

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')