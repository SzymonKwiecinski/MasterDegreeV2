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
problem = pulp.LpProblem("Container_Management_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, cat='Integer')
store = pulp.LpVariable.dicts("store", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] + 
                       data['HoldingCost'] * store[t] + 
                       data['CraneCost'] * crane[t] 
                       for t in range(1, data['T'] + 1))

# Initial constraint
problem += store[0] == data['InitContainer']

# Flow balance constraints
for t in range(1, data['T'] + 1):
    problem += (data['InitContainer'] if t == 1 else store[t-1]) + amount[t] == data['Demands'][t-1] + store[t]

# Capacity and storage constraints
for t in range(1, data['T'] + 1):
    problem += amount[t] <= data['UnloadCapacity'][t-1]
    problem += store[t] <= data['MaxContainer']

# Loading constraints
for t in range(1, data['T'] + 1):
    problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t-1]
    problem += crane[t] <= data['NumCranes']

# End constraint
problem += store[data['T']] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')