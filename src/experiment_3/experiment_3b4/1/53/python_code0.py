import pulp

# Data provided in JSON format
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

# Create a LP minimization problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
amount_vars = {(i, j): pulp.LpVariable(f'amount_{i}_{j}', lowBound=0, cat='Continuous') 
               for i in range(num_terminals) for j in range(num_destinations)}

# Objective function
problem += pulp.lpSum(cost[i][j] * amount_vars[(i, j)] for i in range(num_terminals) for j in range(num_destinations)), "Total Transportation Cost"

# Supply constraints for each terminal
for k in range(num_terminals):
    problem += pulp.lpSum(amount_vars[(k, j)] for j in range(num_destinations)) <= supply[k], f'Supply_Constraint_{k}'

# Demand constraints for each destination
for l in range(num_destinations):
    problem += pulp.lpSum(amount_vars[(i, l)] for i in range(num_terminals)) >= demand[l], f'Demand_Constraint_{l}'

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')