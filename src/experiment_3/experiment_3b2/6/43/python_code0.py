import pulp

# Data from JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Model Initialization
problem = pulp.LpProblem("WildSportsProduction", pulp.LpMaximize)

# Decision Variables
M = len(data['prices'])
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function
profit_per_unit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit_per_unit[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints
# Raw Material Constraints
for i in range(len(data['available'])):
    problem += (pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]), f"Raw_Material_Constraint_{i+1}"

# Demand Constraints
for j in range(M):
    problem += (x[j] <= data['demands'][j]), f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')