import pulp

# Data from the problem
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

# Initializing problem
problem = pulp.LpProblem('Minimize_Transport_Cost', pulp.LpMinimize)

# Unpack data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Decision variables
shipment_vars = pulp.LpVariable.dicts("shipment",
                                      ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
                                      lowBound=0,
                                      cat=pulp.LpContinuous)

# Objective function
problem += pulp.lpSum(shipment_vars[i, j] * costs[i][j] for i in range(num_terminals) for j in range(num_destinations)), "Total_Transport_Cost"

# Constraints

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(shipment_vars[i, j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(shipment_vars[i, j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Preparing output format
output = {
    "distribution": [
        {
            "from": i,
            "to": j,
            "amount": shipment_vars[i, j].varValue
        }
        for i in range(num_terminals) for j in range(num_destinations)
    ],
    "total_cost": pulp.value(problem.objective)
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

output