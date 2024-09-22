import pulp

# Data from the provided JSON
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

# Create the LP problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')
containers = pulp.LpVariable.dicts("containers", range(0, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] + 
                       data['HoldingCost'] * containers[t] + 
                       data['CraneCost'] * crane[t] 
                       for t in range(1, data['T'] + 1))

# Constraints
# Demand Fulfillment
for t in range(1, data['T'] + 1):
    problem += amount[t] + (containers[t-1] if t > 1 else data['InitContainer']) - containers[t] == data['Demands'][t-1]

# Unloading Capacity
for t in range(1, data['T'] + 1):
    problem += amount[t] <= data['UnloadCapacity'][t-1]

# Crane Rental Capacity
for t in range(1, data['T'] + 1):
    problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t-1]

# Maximum Cranes
for t in range(1, data['T'] + 1):
    problem += crane[t] <= data['NumCranes']

# Yard Storage Limit
for t in range(1, data['T'] + 1):
    problem += containers[t] <= data['MaxContainer']

# Initial Condition
problem += containers[0] == data['InitContainer']

# Final Condition
problem += containers[data['T']] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')