import pulp
import json

# Data in JSON format
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Parameters
available = data['available']  # available tons of alloy
carbon = data['carbon']        # percentage of carbon in alloy
nickel = data['nickel']        # percentage of nickel in alloy
alloy_prices = data['alloy_prices']  # purchase price of alloy per ton
steel_prices = data['steel_prices']  # selling price of steel type per ton
carbon_min = data['carbon_min']      # minimum allowable percentage of carbon
nickel_max = data['nickel_max']      # maximum allowable percentage of nickel

A = len(available)  # number of alloys
S = len(steel_prices)  # number of steel types

# Define the Linear Programming problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S)) - \
           pulp.lpSum(alloy_prices[a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a]

# Carbon content constraints
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * alloy_amount[a][s] for a in range(A)) / total_steel[s]) >= carbon_min[s]

# Nickel content constraints
for s in range(S):
    problem += (pulp.lpSum(nickel[a] * alloy_amount[a][s] for a in range(A)) / total_steel[s]) <= nickel_max[s]

# Alloy 1 usage constraint
for s in range(S):
    problem += pulp.lpSum(alloy_amount[0][s] for _ in range(S)) <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')