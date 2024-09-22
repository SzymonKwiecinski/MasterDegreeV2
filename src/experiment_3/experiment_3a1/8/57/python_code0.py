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

# Create the problem
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'])
inventory = pulp.LpVariable.dicts("inventory", range(1, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] +
                       data['HoldingCost'] * inventory[t] +
                       data['CraneCost'] * crane[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    if t == 1:
        problem += inventory[t] == data['InitContainer'] + amount[t] - crane[t] * data['CraneCapacity']
    else:
        problem += inventory[t] == inventory[t-1] + amount[t] - crane[t] * data['CraneCapacity']

    problem += inventory[t] <= data['MaxContainer']
    problem += amount[t] <= data['UnloadCapacity'][t-1]

    if t < data['T']:
        problem += inventory[t-1] + amount[t] - crane[t] * data['CraneCapacity'] >= data['Demands'][t-1]
    else:
        problem += inventory[t] == 0

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(1, data['T'] + 1)]
cranes_rented = [crane[t].varValue for t in range(1, data['T'] + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')