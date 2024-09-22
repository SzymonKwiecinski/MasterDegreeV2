import pulp

# Data
available = [240000, 8000, 75000]
requirements = [[48, 1, 10], [40, 1, 10], [0, 1, 2]]
prices = [40, 38, 9]
costs = [30, 26, 7]
demands = [10000, 2000, 10000]

M = len(prices)
N = len(available)

# Define the LP problem
problem = pulp.LpProblem('WildSports', pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
profit = pulp.lpSum((prices[j] - costs[j]) * amount[j] for j in range(M))
problem += profit

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i]

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j]

# Solve the problem
problem.solve()

# Output results
for j in range(M):
    print(f"Amount produced of product {j + 1}: {amount[j].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')