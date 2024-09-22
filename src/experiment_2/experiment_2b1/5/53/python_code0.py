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

# Extracting input data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Creating the LP problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(cost[i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations)), "TotalTransportationCost"

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i][j] for j in range(num_destinations)) <= supply[i], f"SupplyConstraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i][j] for i in range(num_terminals)) >= demand[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
distribution = []
for i in range(num_terminals):
    for j in range(num_destinations):
        if amount[i][j].varValue > 0:
            distribution.append({"from": i, "to": j, "amount": amount[i][j].varValue})

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')