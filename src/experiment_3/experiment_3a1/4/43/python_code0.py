import pulp

# Data extracted from the provided JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Indices and parameters
N = len(data['available'])          # Number of raw materials
M = len(data['prices'])             # Number of products

# Create the model
problem = pulp.LpProblem("WildSportsMaxProfit", pulp.LpMaximize)

# Decision Variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amounts[j] for j in range(M))
problem += profit

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * amounts[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += amounts[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Output results
for j in range(M):
    print(f'Amount of product {j+1} produced: {amounts[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')