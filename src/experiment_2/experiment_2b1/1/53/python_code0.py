import pulp
import json

# Input data
data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Number of terminals and destinations
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the optimization problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective function: minimize transportation costs
problem += pulp.lpSum(amount[k][l] * costs[k][l] for k in range(num_terminals) for l in range(num_destinations)), "TotalTransportationCost"

# Supply constraints
for k in range(num_terminals):
    problem += pulp.lpSum(amount[k][l] for l in range(num_destinations)) <= supply[k], f"SupplyLimit_terminal_{k}"

# Demand constraints
for l in range(num_destinations):
    problem += pulp.lpSum(amount[k][l] for k in range(num_terminals)) >= demand[l], f"DemandRequirement_destination_{l}"

# Solve the problem
problem.solve()

# Prepare the output
distribution = []
for k in range(num_terminals):
    for l in range(num_destinations):
        if amount[k][l].varValue > 0:
            distribution.append({"from": k, "to": l, "amount": amount[k][l].varValue})

total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print output
print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')