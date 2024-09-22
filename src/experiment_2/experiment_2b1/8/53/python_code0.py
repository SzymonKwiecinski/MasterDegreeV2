import pulp
import json

# Given data from the problem statement
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Define the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts("Amount", (range(data['NumTerminals']), range(data['NumDestinations'])), lowBound=0, cat='Continuous')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(amount[i][j] * data['Cost'][i][j] for i in range(data['NumTerminals']) for j in range(data['NumDestinations']))

# Supply constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[i][j] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[i][j] for i in range(data['NumTerminals'])) >= data['Demand'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
output = {"distribution": [], "total_cost": pulp.value(problem.objective)}

for i in range(data['NumTerminals']):
    for j in range(data['NumDestinations']):
        if pulp.value(amount[i][j]) > 0:
            output["distribution"].append({
                "from": i,
                "to": j,
                "amount": pulp.value(amount[i][j])
            })

# Print the output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')