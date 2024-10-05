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

# Initialize the problem
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpContinuous)
crane = pulp.LpVariable.dicts("Crane", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("Storage", range(0, data['T'] + 1), lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += sum(
    data['UnloadCosts'][t-1] * amount[t] +
    data['HoldingCost'] * storage[t] +
    data['CraneCost'] * crane[t]
    for t in range(1, data['T'] + 1)
)

# Constraints
for t in range(1, data['T'] + 1):
    problem += amount[t] <= data['UnloadCapacity'][t-1]
    problem += amount[t] + storage[t-1] - storage[t] == data['Demands'][t-1]
    problem += storage[t] <= data['MaxContainer']
    problem += crane[t] * data['CraneCapacity'] >= amount[t]
    problem += crane[t] <= data['NumCranes']

problem += storage[0] == data['InitContainer']
problem += storage[data['T']] == 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')