import pulp
import json

# Data from JSON
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) - \
         pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))

problem += profit, "Total_Profit"

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= data['available'][a], f"Alloy_Availability_{a}"

# Carbon content constraints for each steel type
for s in range(S):
    problem += (pulp.lpSum(data['carbon'][a] * alloy_amount[a][s] for a in range(A)) >= 
                 data['carbon_min'][s] * total_steel[s], f"Carbon_Constraint_{s}")

# Nickel content constraints for each steel type
for s in range(S):
    problem += (pulp.lpSum(data['nickel'][a] * alloy_amount[a][s] for a in range(A)) <= 
                 data['nickel_max'][s] * total_steel[s], f"Nickel_Constraint_{s}")

# Maximum limit of alloy 1 in all steel types
problem += (pulp.lpSum(alloy_amount[0][s] for s in range(S)) <= 
            0.4 * pulp.lpSum(total_steel[s] for s in range(S)), "Max_Alloy_1")

# Solve the problem
problem.solve()

# Print the results
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')