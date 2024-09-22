import pulp
import json

# Data input
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Sets
alloys = range(len(data['available']))  # A
steels = range(len(data['steel_prices']))  # S

# Parameters
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Variables
x = pulp.LpVariable.dicts("x", (alloys, steels), 0)  # Amount of alloy a used in steel type s
total_steel = pulp.LpVariable.dicts("total_steel", steels, 0)  # Total amount of steel produced
total_profit = pulp.LpVariable("total_profit")  # Total profit

# Problem Definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in steels) - \
           pulp.lpSum(alloy_prices[a] * pulp.lpSum(x[a][s] for s in steels) for a in alloys)

# Material Constraints
for a in alloys:
    problem += pulp.lpSum(x[a][s] for s in steels) <= available[a]

# Carbon Constraints
for s in steels:
    problem += pulp.lpSum(x[a][s] * carbon[a] for a in alloys) >= carbon_min[s] * total_steel[s]

# Nickel Constraints
for s in steels:
    problem += pulp.lpSum(x[a][s] * nickel[a] for a in alloys) <= nickel_max[s] * total_steel[s]

# Alloy 1 Constraint
for s in steels:
    problem += pulp.lpSum(x[0][s] for a in alloys) <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')