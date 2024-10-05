import pulp

# Data
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

# Model
problem = pulp.LpProblem("Container_Management", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpInteger)
crane = pulp.LpVariable.dicts("Crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("Storage", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpInteger)

# Objective function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] +
                      data['HoldingCost'] * storage[t] +
                      data['CraneCost'] * crane[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Demand fulfillment
    problem += amount[t] >= data['Demands'][t-1]
    
    # Unloading capacity
    problem += amount[t] <= data['UnloadCapacity'][t-1]
    
    # Crane capacity
    problem += crane[t] * data['CraneCapacity'] >= amount[t]
    
    # Storage balance
    if t == 1:
        problem += storage[t] == data['InitContainer'] + amount[t] - data['Demands'][t-1]
    else:
        problem += storage[t] == storage[t-1] + amount[t] - data['Demands'][t-1]
    
    # Maximum storage
    problem += storage[t] <= data['MaxContainer']

# Final storage should be zero
problem += storage[data['T']] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')