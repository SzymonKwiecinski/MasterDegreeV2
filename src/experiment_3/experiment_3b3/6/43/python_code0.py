import pulp

# Extracting data from provided JSON format.
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products (M) and raw materials (N)
M = len(prices)
N = len(available)

# Initialize the linear programming problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Decision variables: amount of each product to produce
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: Maximize total profit
profit = pulp.lpSum((prices[j] - costs[j]) * x[j] for j in range(M))
problem += profit

# Constraints

# 1. Raw material constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i])

# 2. Demand constraints
for j in range(M):
    problem += (x[j] <= demands[j])

# Solve the problem
problem.solve()

# Results
amounts = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')