import pulp

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Defining the problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", 
                                 ((i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])),
                                 lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] 
                       for i in range(data['NumTerminals']) 
                       for j in range(data['NumDestinations'])), "Total_Transportation_Cost"

# Supply Constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[(i, j)] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[(i, j)] for i in range(data['NumTerminals'])) >= data['Demand'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')