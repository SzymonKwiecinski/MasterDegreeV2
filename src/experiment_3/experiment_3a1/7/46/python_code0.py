import pulp
import json

# Data input as provided
data_json = '{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}'
data = json.loads(data_json)

# Extract data from the JSON structure
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Constants
A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmount", (range(A), range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("TotalSteel", range(S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S)) - pulp.lpSum(alloy_prices[a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))

# Constraints

# Alloy Availability Constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a]

# Carbon Requirement Constraints
for s in range(S):
    problem += pulp.lpSum(carbon[a] * alloy_amount[a][s] for a in range(A)) >= carbon_min[s] * total_steel[s]

# Nickel Requirement Constraints
for s in range(S):
    problem += pulp.lpSum(nickel[a] * alloy_amount[a][s] for a in range(A)) <= nickel_max[s] * total_steel[s]

# Alloy 1 Limitation
problem += pulp.lpSum(alloy_amount[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')