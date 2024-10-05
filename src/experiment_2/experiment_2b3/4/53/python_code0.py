import pulp

data = {
    'NumTerminals': 3, 
    'NumDestinations': 4, 
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 
    'Demand': [65, 70, 50, 45], 
    'Supply': [150, 100, 100]
}

# Extract necessary data
NumTerminals = data['NumTerminals']
NumDestinations = data['NumDestinations']
Cost = data['Cost']
Demand = data['Demand']
Supply = data['Supply']

# Define the problem
problem = pulp.LpProblem("Soybeans_Transportation", pulp.LpMinimize)

# Variables: amount of soybeans transported from terminal i to destination j
amount = pulp.LpVariable.dicts("Amount", 
                               ((i, j) for i in range(NumTerminals) for j in range(NumDestinations)), 
                               lowBound=0, cat='Continuous')

# Objective function: minimize the total transportation cost
problem += pulp.lpSum(Cost[i][j] * amount[(i, j)] for i in range(NumTerminals) for j in range(NumDestinations))

# Constraints: supply constraints at terminals
for i in range(NumTerminals):
    problem += pulp.lpSum(amount[(i, j)] for j in range(NumDestinations)) <= Supply[i]

# Constraints: demand constraints at destinations
for j in range(NumDestinations):
    problem += pulp.lpSum(amount[(i, j)] for i in range(NumTerminals)) >= Demand[j]

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": i, "to": j, "amount": pulp.value(amount[(i, j)])} 
                for i in range(NumTerminals) for j in range(NumDestinations)]

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

# Printing the distribution and total cost
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')