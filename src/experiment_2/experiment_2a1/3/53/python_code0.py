import pulp
import json

# Input Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Extracting data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost_matrix = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Define the problem
problem = pulp.LpProblem("Soybean Transportation Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost_matrix[i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations))

# Constraints
# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i][j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i][j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
distribution = []
for i in range(num_terminals):
    for j in range(num_destinations):
        if pulp.value(amount[i][j]) > 0:  # Only include non-zero shipments
            distribution.append({
                "from": i,
                "to": j,
                "amount": pulp.value(amount[i][j])
            })

# Total cost
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the output in JSON format
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')