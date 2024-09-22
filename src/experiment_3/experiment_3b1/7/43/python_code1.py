import pulp

# Data from the provided JSON format
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

# Create the LP problem
problem = pulp.LpProblem("Wild_Sports_Production_Optimization", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("Amount", range(M), lowBound=0)

# Objective function
problem += pulp.lpSum((data['prices'][j] - data['costs'][j]) * amounts[j] for j in range(M)), "Total_Profit"

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * amounts[j] for j in range(M)) <= data['available'][i], f"Raw_Material_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += amounts[j] <= data['demands'][j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Print the results
amounts_produced = [amounts[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Amounts Produced): {amounts_produced}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')