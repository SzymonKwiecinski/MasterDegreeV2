import pulp

# Data provided
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Decision variables
M = len(data['prices'])
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

# Material constraints
N = len(data['available'])
for i in range(N):
    problem += (pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"Material_Constraint_{i+1}")

# Demand constraints
for j in range(M):
    problem += (x[j] <= data['demands'][j], f"Demand_Constraint_{j+1}")

# Solve the problem
problem.solve()

# Results
for j in range(M):
    print(f"Amount of product {j+1} produced: {pulp.value(x[j])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')