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

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Create a linear programming problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function: Maximize Z = sum((price_j - cost_j) * x_j)
problem += pulp.lpSum([(prices[j] - costs[j]) * x[j] for j in range(M)]), "Total_Profit"

# Material Constraints
for i in range(N):
    problem += pulp.lpSum([requirements[i][j] * x[j] for j in range(M)]) <= available[i], f"Material_Constraint_{i}"

# Demand Constraints
for j in range(M):
    problem += x[j] <= demands[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output results
amount = [x[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')