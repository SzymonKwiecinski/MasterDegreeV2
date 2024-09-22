import pulp

# Data from the JSON
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

# Define the problem
problem = pulp.LpProblem("Container_Handling_Seaport", pulp.LpMinimize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=data['NumCranes'], cat='Integer') for t in range(data['T'])]
containers = [pulp.LpVariable(f'containers_{t}', lowBound=0, upBound=data['MaxContainer'], cat='Continuous') for t in range(data['T'])]

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * amount[t] + data['HoldingCost'] * containers[t] + data['CraneCost'] * crane[t] for t in range(data['T']))

# Constraints
for t in range(data['T']):
    if t == 0:
        problem += containers[t] == data['InitContainer'] + amount[t]
    else:
        problem += containers[t] == data['InitContainer'] + pulp.lpSum(amount[i] for i in range(t + 1)) - pulp.lpSum(crane[j] * data['CraneCapacity'] for j in range(t + 1))

    problem += containers[t] <= data['MaxContainer']
    problem += amount[t] <= data['UnloadCapacity'][t]
    problem += amount[t] >= data['Demands'][t]

problem += containers[data['T'] - 1] == 0  # Last month containers must be zero

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(data['T'])]
cranes_rented = [crane[t].varValue for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')