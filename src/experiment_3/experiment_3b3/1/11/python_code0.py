import pulp

# Data from the JSON
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the Linear Programming problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Produce", range(1, T+1), lowBound=0, cat=pulp.LpContinuous)
I = pulp.LpVariable.dicts("Inventory", range(1, T+1), lowBound=0, cat=pulp.LpContinuous)

# Objective function
problem += (pulp.lpSum(storage_cost * I[i] for i in range(1, T+1)) +
            pulp.lpSum(switch_cost * pulp.lpAbs(x[i+1] - x[i]) for i in range(1, T) if i < T))

# Constraints
# Inventory balance for each month
for i in range(1, T+1):
    if i == 1:
        problem += I[i] == x[i] - deliver[i-1]
    else:
        problem += I[i] == I[i-1] + x[i] - deliver[i-1]

# Final inventory constraint
problem += I[T] == 0

# Solve the problem
problem.solve()

# Output results
production_plan = [x[i].varValue for i in range(1, T+1)]
print("Production Plan:", production_plan)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')