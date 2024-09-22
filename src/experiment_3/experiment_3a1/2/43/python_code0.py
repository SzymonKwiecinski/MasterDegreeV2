import pulp
import json

# Data from JSON format
data_json = '{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}'
data = json.loads(data_json)

# Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Initialize the problem
problem = pulp.LpProblem("WildSportsProduction", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit[j] * amount[j] for j in range(M)), "Total_Profit"

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"RawMaterialConstraint_{i}"

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Output the results
amount_produced = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f'Amount of each product produced: {amount_produced}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')