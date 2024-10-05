import pulp

# Data
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
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Problem
problem = pulp.LpProblem("Soybean_Transport", pulp.LpMinimize)

# Variables
routes = [(i, j) for i in range(num_terminals) for j in range(num_destinations)]
amount = pulp.LpVariable.dicts("Amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective
problem += pulp.lpSum([amount[i][j] * cost[i][j] for i, j in routes]), "Total_Transportation_Cost"

# Constraints
# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum([amount[i][j] for j in range(num_destinations)]) <= supply[i], f"Supply_Constraint_Terminal_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum([amount[i][j] for i in range(num_terminals)]) >= demand[j], f"Demand_Constraint_Destination_{j}"

# Solve
problem.solve()

# Output
distribution = [{"from": i, "to": j, "amount": pulp.value(amount[i][j])} for i, j in routes]
total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')