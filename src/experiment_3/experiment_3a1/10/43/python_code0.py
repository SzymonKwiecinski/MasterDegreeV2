import pulp
import json

# Data from JSON
data_json = "{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}"
data = json.loads(data_json.replace("'", "\""))

# Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # number of products
N = len(available)  # number of raw materials

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Produces", range(M), lowBound=0)

# Objective function
profit_terms = [(prices[j] - costs[j]) * x[j] for j in range(M)]
problem += pulp.lpSum(profit_terms), "Total_Profit"

# Constraints
# Raw material constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i]), f"RawMaterial_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += (x[j] <= demands[j]), f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Output results
amounts = [x[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')