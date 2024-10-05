import pulp

# Data from JSON format
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Initialize the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Sets
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations)), "Total_Transportation_Cost"

# Supply Constraints
for k in range(num_terminals):
    problem += pulp.lpSum(amount[k][j] for j in range(num_destinations)) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in range(num_destinations):
    problem += pulp.lpSum(amount[i][l] for i in range(num_terminals)) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')