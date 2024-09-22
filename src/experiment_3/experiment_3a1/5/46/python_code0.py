import pulp
import json

# Data provided in JSON format
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Parameters
available = data['available']  # tons of each alloy
carbon = data['carbon']  # percentage of carbon in each alloy
nickel = data['nickel']  # percentage of nickel in each alloy
alloy_prices = data['alloy_prices']  # price per ton of each alloy
steel_prices = data['steel_prices']  # price per ton of each steel type
carbon_min = data['carbon_min']  # minimum carbon requirement for each steel type
nickel_max = data['nickel_max']  # maximum nickel limit for each steel type

# Indices for the model
S = len(steel_prices)  # Number of steel types
A = len(alloy_prices)  # Number of alloys

# Create the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0, cat='Continuous')

# Objective function
profit_from_steel = pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S))
cost_of_alloys = pulp.lpSum(alloy_prices[a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))
problem += profit_from_steel - cost_of_alloys, "Total_Profit"

# Constraints
# Alloy usage constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a], f"Alloy_Usage_Constraint_{a}"

# Carbon content constraints
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s], f"Carbon_Constraint_{s}"

# Nickel content constraints
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s], f"Nickel_Constraint_{s}"

# Alloy 1 usage constraint
problem += pulp.lpSum(alloy_amount[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S)), "Alloy1_Usage_Constraint"

# Solve the problem
problem.solve()

# Output results
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

print(f'Alloy Use: {alloy_use}')
print(f'Total Steel Produced: {total_steel_produced}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')