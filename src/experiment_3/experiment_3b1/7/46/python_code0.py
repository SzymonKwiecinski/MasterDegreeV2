import pulp
import json

# Data
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Sets
alloys = range(len(data['available']))
steels = range(len(data['steel_prices']))

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (alloys, steels), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", steels, lowBound=0, cat='Continuous')
total_profit = pulp.LpVariable("total_profit", lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit_from_steel = pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in steels)
cost_of_alloys = pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(alloy_amount[a][s] for s in steels) for a in alloys)
problem += total_profit == profit_from_steel - cost_of_alloys, "Objective"

# Constraints
# Alloy availability
for a in alloys:
    problem += pulp.lpSum(alloy_amount[a][s] for s in steels) <= data['available'][a], f"Available_alloy_{a}"

# Carbon content
for s in steels:
    problem += (pulp.lpSum(alloy_amount[a][s] * data['carbon'][a] for a in alloys) / total_steel[s]) >= data['carbon_min'][s], f"Carbon_content_{s}"

# Nickel content
for s in steels:
    problem += (pulp.lpSum(alloy_amount[a][s] * data['nickel'][a] for a in alloys) / total_steel[s]) <= data['nickel_max'][s], f"Nickel_content_{s}"

# Alloy 1 restriction
problem += (pulp.lpSum(alloy_amount[0][s] for s in steels) <= 0.4 * pulp.lpSum(total_steel[s] for s in steels)), "Alloy_1_restriction"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')