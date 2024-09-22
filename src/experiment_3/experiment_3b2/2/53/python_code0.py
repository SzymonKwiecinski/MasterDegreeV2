import pulp

# Load data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Problem definition
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
                            [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])], 
                            lowBound=0, 
                            cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * x[(i, j)] for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), "Total_Transportation_Cost"

# Supply constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(x[(i, j)] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(x[(i, j)] for i in range(data['NumTerminals'])) >= data['Demand'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')