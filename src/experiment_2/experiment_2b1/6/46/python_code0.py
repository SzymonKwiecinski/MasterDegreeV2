import pulp
import json

# Data provided in JSON format
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Extracting data from the provided input
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Define the number of alloys and steel types
A = len(available)
S = len(steel_prices)

# Create the LP problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Define decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective function: Maximize profit
problem += pulp.lpSum(total_steel[s] * steel_prices[s] for s in range(S)) - pulp.lpSum(alloy_amount[a][s] * alloy_prices[a] for a in range(A) for s in range(S))

# Constraints for alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= available[a]

# Constraints for steel properties
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s]
    problem += pulp.lpSum(alloy_amount[a][s] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s]
    
# Constraint for alloy 1
for s in range(S):
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Prepare the output
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_values = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_values,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')