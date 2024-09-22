import pulp
import json

# Input data
data = json.loads("{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}")

# Extracting data from the JSON
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

S = len(steel_prices)  # Number of types of steel
A = len(available)     # Number of alloys

# Create the optimization problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
problem += pulp.lpSum(steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_amount[a][s] for a in range(A)) for s in range(S))

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a]

# Steel production constraints
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] for a in range(A)) == total_steel[s]

# Carbon content constraints
for s in range(S):
    problem += pulp.lpSum(carbon[a] * alloy_amount[a][s] for a in range(A)) >= carbon_min[s] * total_steel[s]

# Nickel content constraints
for s in range(S):
    problem += pulp.lpSum(nickel[a] * alloy_amount[a][s] for a in range(A)) <= nickel_max[s] * total_steel[s]

# Limit on alloy 1 usage
for s in range(S):
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Result formatting
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Print the results
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

# Print the final objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')