import pulp
import json

data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Extract data from JSON
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Define decision variables
amounts = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(amounts[i][j] * costs[i][j] for i in range(num_terminals) for j in range(num_destinations)), "TotalCost"

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amounts[i][j] for j in range(num_destinations)) <= supply[i], f"SupplyConstraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amounts[i][j] for i in range(num_terminals)) >= demand[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": i, "to": j, "amount": amounts[i][j].varValue} for i in range(num_terminals) for j in range(num_destinations) if amounts[i][j].varValue > 0]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')