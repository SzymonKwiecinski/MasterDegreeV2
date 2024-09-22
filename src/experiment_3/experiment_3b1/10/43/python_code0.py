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

# Create the linear programming problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("Production", range(M), lowBound=0)

# Objective Function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints for raw materials
for i in range(N):
    problem += (pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"Material_Constraint_{i}")

# Demand constraints
for j in range(M):
    problem += (x[j] <= data['demands'][j], f"Demand_Constraint_{j}")

# Solve the problem
problem.solve()

# Output the results
amounts = [x[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f'Amount produced of each product: {amounts}')
print(f'Total profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')