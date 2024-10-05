import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [
        [48, 1, 10],
        [40, 1, 10],
        [0, 1, 2]
    ],
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

# Number of products
M = len(prices)
# Number of raw materials
N = len(available)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x_vars = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective Function
profit = pulp.lpSum((prices[j] - costs[j]) * x_vars[j] for j in range(M))
problem += profit

# Raw Material Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x_vars[j] for j in range(M)) <= available[i]

# Demand Constraints
for j in range(M):
    problem += x_vars[j] <= demands[j]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')