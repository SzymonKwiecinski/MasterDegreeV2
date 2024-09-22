import pulp
import json

# Data provided in JSON format
data_json = '{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}'
data = json.loads(data_json)

# Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of products
N = len(available)  # Number of raw materials

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Problem definition
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Objective function
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit, "Total_Profit"

# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i+1}"

# Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')