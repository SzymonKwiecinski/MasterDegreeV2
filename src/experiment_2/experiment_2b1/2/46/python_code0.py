import pulp
import json

# Input data
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

S = len(steel_prices)  # Number of steel types
A = len(available)     # Number of alloys

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0)

# Objective function
problem += pulp.lpSum(total_steel[s] * steel_prices[s] for s in range(S)) - pulp.lpSum(alloy_amount[a, s] * alloy_prices[a] for a in range(A) for s in range(S))

# Constraints
# Carbon and Nickel constraints for each steel type
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a, s] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s], f"Carbon_min_constraint_{s}"
    problem += pulp.lpSum(alloy_amount[a, s] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s], f"Nickel_max_constraint_{s}"

# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a], f"Available_alloy_constraint_{a}"

# At most 40% of alloy 1 can be used across all steel types
problem += pulp.lpSum(alloy_amount[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S)), "Alloy_1_constraint"

# Solve the problem
problem.solve()

# Prepare results
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')