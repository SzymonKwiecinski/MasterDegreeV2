import pulp
import json

# Data in JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create the problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints
# Raw Material Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i+1}"

# Demand Constraints
for j in range(M):
    problem += x[j] <= demands[j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Output results
amount_produced = [x[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f"Amount produced: {amount_produced}")
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')