import pulp

# Parse input data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [
        [34, 49, 17, 26],
        [52, 64, 23, 14],
        [20, 28, 12, 17]
    ],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Extract data
NumTerminals = data['NumTerminals']
NumDestinations = data['NumDestinations']
Costs = data['Cost']
Demands = data['Demand']
Supplies = data['Supply']

# Indices
terminals = range(NumTerminals)
destinations = range(NumDestinations)

# Create LP problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", [(i, j) for i in terminals for j in destinations], lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(Costs[i][j] * amount[(i, j)] for i in terminals for j in destinations), "Total_Transportation_Cost"

# Supply constraints
for i in terminals:
    problem += pulp.lpSum(amount[(i, j)] for j in destinations) <= Supplies[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in destinations:
    problem += pulp.lpSum(amount[(i, j)] for i in terminals) >= Demands[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output data
distribution = [{"from": i, "to": j, "amount": pulp.value(amount[(i, j)])} for i in terminals for j in destinations]

# Output the result
output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')