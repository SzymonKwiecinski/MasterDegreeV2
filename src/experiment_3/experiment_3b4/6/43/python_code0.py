import pulp

# Problem data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of products
M = len(data['prices'])

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit, "Total_Profit"

# Material constraints
for i in range(len(data['available'])):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"Material_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')