import pulp
import json

# Input data
data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Define the problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Define variables
routes = [(k, l) for k in range(data['NumTerminals']) for l in range(data['NumDestinations'])]
amounts = pulp.LpVariable.dicts("amount", routes, lowBound=0)

# Objective function: Minimize transportation cost
problem += pulp.lpSum(data['Cost'][k][l] * amounts[(k, l)] for k in range(data['NumTerminals']) for l in range(data['NumDestinations']))

# Supply constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum(amounts[(k, l)] for l in range(data['NumDestinations'])) <= data['Supply'][k], f"Supply_{k}"

# Demand constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum(amounts[(k, l)] for k in range(data['NumTerminals'])) >= data['Demand'][l], f"Demand_{l}"

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": k, "to": l, "amount": amounts[(k, l)].varValue} for k in range(data['NumTerminals']) for l in range(data['NumDestinations']) if amounts[(k, l)].varValue > 0]

total_cost = pulp.value(problem.objective)

# Output results
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')