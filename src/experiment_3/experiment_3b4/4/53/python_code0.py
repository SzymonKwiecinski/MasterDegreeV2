import pulp

# Data input
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

# Extracting data elements
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Indices
terminals = range(num_terminals)
destinations = range(num_destinations)

# Problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Shipment", ((i, j) for i in terminals for j in destinations), 
                          lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost[i][j] * x[i, j] for i in terminals for j in destinations), "Total_Transportation_Cost"

# Supply Constraints
for i in terminals:
    problem += pulp.lpSum(x[i, j] for j in destinations) <= supply[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in destinations:
    problem += pulp.lpSum(x[i, j] for i in terminals) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the results
print("Optimal Shipment Plan:")
for i in terminals:
    for j in destinations:
        print(f"Ship from Terminal {i} to Destination {j}: {pulp.value(x[i, j])}")

# Print objective value
print(f'Total transportation cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')