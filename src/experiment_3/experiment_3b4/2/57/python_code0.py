import pulp

# Data from JSON
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", range(data['T'] + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([
    data['UnloadCosts'][t] * amount[t] +
    data['HoldingCost'] * storage[t] +
    data['CraneCost'] * crane[t]
    for t in range(data['T'])
])

# Constraints
# Initial storage
problem += storage[0] == data['InitContainer']

# Final storage must be zero
problem += storage[data['T']] == 0

for t in range(data['T']):
    # Amount constraints
    problem += amount[t] <= data['UnloadCapacity'][t]
    
    # Storage balance constraint
    problem += storage[t + 1] == storage[t] + amount[t] - data['Demands'][t]
    
    # Max container in storage
    problem += storage[t] <= data['MaxContainer']

    # Crane capacity constraint
    problem += data['Demands'][t] <= data['CraneCapacity'] * crane[t]

    # Max number of cranes
    problem += crane[t] <= data['NumCranes']

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')