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

# Model
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, upBound=data['NumCranes'], cat='Integer')
storage = pulp.LpVariable.dicts("storage", range(data['T']), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * amount[t] + data['HoldingCost'] * storage[t] + data['CraneCost'] * crane[t]
                       for t in range(data['T']))

# Constraints
problem += storage[0] == data['InitContainer']

for t in range(data['T']):
    # Demand Satisfaction
    if t > 0:
        problem += amount[t] + storage[t - 1] - storage[t] == data['Demands'][t]
    else:
        problem += amount[t] - storage[t] == data['Demands'][t]

    # Unloading Capacity
    problem += amount[t] <= data['UnloadCapacity'][t]

    # Storage Capacity
    problem += storage[t] <= data['MaxContainer']

    # Crane Loading Capacity
    problem += crane[t] * data['CraneCapacity'] >= amount[t]

# Final Storage Condition
problem += storage[data['T'] - 1] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')