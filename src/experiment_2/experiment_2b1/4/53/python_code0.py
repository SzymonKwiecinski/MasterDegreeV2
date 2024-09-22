import pulp
import json

# Input data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Create the problem
problem = pulp.LpProblem("Transportation Problem", pulp.LpMinimize)

# Define variables
routes = [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]
amount = pulp.LpVariable.dicts("amount", routes, lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), "Total Cost"

# Supply constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[(i, j)] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[(i, j)] for i in range(data['NumTerminals'])) >= data['Demand'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": i, "to": j, "amount": amount[(i, j)].varValue} for i in range(data['NumTerminals']) for j in range(data['NumDestinations']) if amount[(i, j)].varValue > 0]
total_cost = pulp.value(problem.objective)

# Print the output in the required format
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))

# Objective value output
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')