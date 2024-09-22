import pulp

# Data from JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Number of products and raw materials
M = len(data['prices'])
N = len(data['available'])

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(M), lowBound=0)

# Objective function
profit_per_unit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit_per_unit[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints for raw materials
for i in range(N):
    problem += (
        pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], 
        f"RawMaterialConstraint_{i}"
    )

# Demand constraints
for j in range(M):
    problem += (x[j] <= data['demands'][j], f"DemandConstraint_{j}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')