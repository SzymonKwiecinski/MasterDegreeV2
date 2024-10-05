import pulp

# Data
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

# Indices
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Create the LP problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", 
                               ((k, l) for k in terminals for l in destinations), 
                               lowBound=0, 
                               cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][k][l] * amount[k, l] for k in terminals for l in destinations), "Total Cost"

# Supply Constraints
for k in terminals:
    problem += pulp.lpSum(amount[k, l] for l in destinations) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in destinations:
    problem += pulp.lpSum(amount[k, l] for k in terminals) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')