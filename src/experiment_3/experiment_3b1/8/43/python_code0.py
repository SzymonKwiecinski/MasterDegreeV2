import pulp
import json

# Data provided in JSON format
data = {'available': [240000, 8000, 75000], 
        'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 
        'prices': [40, 38, 9], 
        'costs': [30, 26, 7], 
        'demands': [10000, 2000, 10000]}

# Extract data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of products and raw materials
M = len(prices)
N = len(available)

# Create the linear programming problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("amount_produced", range(M), lowBound=0)

# Objective function
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += x[j] <= demands[j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Extract results
amounts = [x[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "amount": amounts,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')