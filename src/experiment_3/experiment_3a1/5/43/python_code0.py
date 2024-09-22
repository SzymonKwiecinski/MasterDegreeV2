import pulp

# Data from the provided JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Parameters
M = len(data['prices'])  # Number of products
N = len(data['available'])  # Number of resources

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Product", range(M), lowBound=0)

# Objective Function
profit_coefficients = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit_coefficients[j] * x[j] for j in range(M)), "Total_Profit"

# Resource Constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"Resource_Constraint_{i+1}"

# Demand Constraints
for j in range(M):
    problem += x[j] <= data['demands'][j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Output the results
for j in range(M):
    print(f'Product {j+1} produced: {x[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')