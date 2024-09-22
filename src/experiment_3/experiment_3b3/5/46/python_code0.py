import pulp
import json

# Load data
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Parameters
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Sets
A = range(len(available))  # Alloys
S = range(len(steel_prices))  # Steel types

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", [(a, s) for a in A for s in S], lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", S, lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([steel_prices[s] * total_steel[s] for s in S]) - pulp.lpSum([alloy_prices[a] * alloy_amount[a, s] for a in A for s in S])
problem += profit

# Constraints
# Alloy availability
for a in A:
    problem += pulp.lpSum(alloy_amount[a, s] for s in S) <= available[a], f"Alloy_Availability_{a}"

# Carbon requirement
for s in S:
    problem += pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in A) >= carbon_min[s] * total_steel[s], f"Carbon_Requirement_{s}"

# Nickel limitation
for s in S:
    problem += pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in A) <= nickel_max[s] * total_steel[s], f"Nickel_Limitation_{s}"

# Proportion of alloy 1
problem += pulp.lpSum(alloy_amount[0, s] for s in S) <= 0.4 * pulp.lpSum(total_steel[s] for s in S), "Proportion_Alloy_1"

# Total steel production
for s in S:
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a, s] for a in A), f"Total_Steel_Production_{s}"

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')