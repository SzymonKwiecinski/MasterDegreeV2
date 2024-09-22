import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Number of products (M) and number of raw materials (N)
M = len(data['prices'])
N = len(data['available'])

# Problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0) for j in range(M)]

# Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit

# Raw material constraints
for i in range(N):
    problem += (
        pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i],
        f"Raw_Material_Constraint_{i}"
    )

# Demand constraints
for j in range(M):
    problem += (
        x[j] <= data['demands'][j],
        f"Demand_Constraint_{j}"
    )

# Solve the problem
problem.solve()

# Output
product_amounts = {f'x_{j}': pulp.value(x[j]) for j in range(M)}
total_profit = pulp.value(problem.objective)

print("Amount of each product produced:")
for j in range(M):
    print(f"Product {j+1}: {product_amounts[f'x_{j}']}")

print(f"(Objective Value): <OBJ>{total_profit}</OBJ>")