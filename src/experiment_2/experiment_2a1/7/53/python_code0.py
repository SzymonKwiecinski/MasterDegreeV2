import pulp
import json

# Data from the input
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Extracting parameters from the data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Decision variables: amount of soybeans shipped from terminal i to destination j
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(cost[i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i][j] for j in range(num_destinations)) <= supply[i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i][j] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Prepare the output
distribution = []
for i in range(num_terminals):
    for j in range(num_destinations):
        amount_shipped = amount[i][j].varValue
        if amount_shipped > 0:
            distribution.append({"from": i, "to": j, "amount": amount_shipped})

total_cost = pulp.value(problem.objective)

# Output the result
result = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')

# Optionally, you can print the result, but omit that if you only want the objective value
# print(json.dumps(result, indent=4))