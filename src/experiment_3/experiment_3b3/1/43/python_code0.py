import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Indices for products and raw materials
M = len(data['prices'])  # number of products
N = len(data['available'])  # number of raw materials

# Decision variables
x = [pulp.LpVariable(f'x_{j+1}', lowBound=0, cat='Continuous') for j in range(M)]

# Problem
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

# Objective Function
profit = [(data['prices'][j] - data['costs'][j]) * x[j] for j in range(M)]
problem += pulp.lpSum(profit), "Total Profit"

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"RawMaterial_{i+1}"

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j], f"Demand_{j+1}"

# Solve the problem
problem.solve()

# Output the results
for j in range(M):
    print(f"Amount of product {j+1} produced: {pulp.value(x[j])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')