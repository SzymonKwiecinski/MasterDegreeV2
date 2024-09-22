import pulp
import json

# Input Data
data = json.loads('{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}')

# Problem Definition
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
M = len(data['prices'])
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

# Objective Function
profit_per_unit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit_per_unit[j] * x[j] for j in range(M)), "Total_Profit"

# Constraints
N = len(data['available'])
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], f"Resource_Constraint_{i+1}"

for j in range(M):
    problem += x[j] <= data['demands'][j], f"Demand_Constraint_{j+1}"

# Solve the Problem
problem.solve()

# Output
amount = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')