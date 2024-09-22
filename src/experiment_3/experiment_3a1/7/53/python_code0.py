import pulp
import json

# Data provided
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Define the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Create decision variables
routes = [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]
amounts = pulp.LpVariable.dicts("amount", routes, lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * amounts[(i, j)] for (i, j) in routes), "Total_Transportation_Cost"

# Supply Constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum(amounts[(k, j)] for j in range(data['NumDestinations'])) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum(amounts[(i, l)] for i in range(data['NumTerminals'])) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Collect the results
distribution = [{"from": i, "to": j, "amount": amounts[(i, j)].varValue} for (i, j) in routes if amounts[(i, j)].varValue > 0]
total_cost = pulp.value(problem.objective)

# Create output structure
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')

# Output the result in JSON format
print(json.dumps(output, indent=4))