import pulp

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

NumTerminals = data['NumTerminals']
NumDestinations = data['NumDestinations']
Cost = data['Cost']
Demand = data['Demand']
Supply = data['Supply']

# Create a linear programming problem
problem = pulp.LpProblem("Transportation", pulp.LpMinimize)

# Decision Variables
amount_vars = {}
for i in range(NumTerminals):
    for j in range(NumDestinations):
        amount_vars[(i, j)] = pulp.LpVariable(f'amount_{i}_{j}', lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Cost[i][j] * amount_vars[(i, j)] for i in range(NumTerminals) for j in range(NumDestinations))

# Supply Constraints
for i in range(NumTerminals):
    problem += pulp.lpSum(amount_vars[(i, j)] for j in range(NumDestinations)) <= Supply[i]

# Demand Constraints
for j in range(NumDestinations):
    problem += pulp.lpSum(amount_vars[(i, j)] for i in range(NumTerminals)) >= Demand[j]

# Solve the problem
problem.solve()

# Display results
distribution = [{'from': i, 'to': j, 'amount': pulp.value(amount_vars[(i, j)])}
                for i in range(NumTerminals)
                for j in range(NumDestinations) 
                if pulp.value(amount_vars[(i, j)]) > 0]

print("Distribution:")
for dist in distribution:
    print(dist)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')