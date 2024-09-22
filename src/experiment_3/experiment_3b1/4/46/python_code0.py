import pulp
import json

# Data in JSON format
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Problem Definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("AlloyUsage", (range(A), range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("SteelProduction", range(S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a][s] for s in range(S)) for a in range(A)), "Total_Profit"

# Constraints
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a], f"Available_Alloy_{a}"

for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * (x[a][s] / y[s]) for a in range(A)) >= data['carbon_min'][s], f"Carbon_Min_{s}"
    problem += pulp.lpSum(data['nickel'][a] * (x[a][s] / y[s]) for a in range(A)) <= data['nickel_max'][s], f"Nickel_Max_{s}"
    problem += pulp.lpSum(x[0][s]) <= 0.4 * y[s], f"Alloy_1_Usage_Limit_{s}"

# Solve the problem
problem.solve()

# Output Results
alloy_use = {f'alloy_{a}_steel_{s}': x[a][s].varValue for a in range(A) for s in range(S)}
total_steel = {f'steel_{s}': y[s].varValue for s in range(S)}
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')