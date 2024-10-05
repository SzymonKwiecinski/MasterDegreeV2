import pulp

# Data from the provided JSON format
data = {
    'available': [240000, 8000, 75000], 
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
    'prices': [40, 38, 9], 
    'costs': [30, 26, 7], 
    'demands': [10000, 2000, 10000]
}

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of products and materials
M = len(data['prices'])
N = len(data['available'])

# Decision variables
x = pulp.LpVariable.dicts("units", range(M), lowBound=0)

# Objective function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"Material_Constraint_{i}"

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')