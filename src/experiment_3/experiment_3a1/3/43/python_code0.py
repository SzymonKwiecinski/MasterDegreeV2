import pulp

# Define the data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
profits = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profits[j] * amounts[j] for j in range(M)), "Total_Profit"

# Resource constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * amounts[j] for j in range(M)) <= data['available'][i], f"Resource_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += amounts[j] <= data['demands'][j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Output the results
for j in range(M):
    print(f"Amount of product {j+1} to produce: {amounts[j].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')