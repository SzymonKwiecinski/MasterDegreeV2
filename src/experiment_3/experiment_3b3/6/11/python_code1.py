import pulp

# Data from JSON
data = {'T': 12,
        'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
        'StorageCost': 5,
        'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Problem definition
problem = pulp.LpProblem("Production_Plan", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("I", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([storage_cost * I[i] + 
                       switch_cost * pulp.lpSum([pulp.lpSum([x[j] - x[j-1] for j in range(1, T)]) if j > 0 else 0 for j in range(1, T)]) 
                       for i in range(T)])

# Constraints
# Initial inventory
problem += I[0] == x[0] - deliver[0]

# Inventory balance
for i in range(1, T):
    problem += I[i] == I[i-1] + x[i] - deliver[i]

# Final inventory constraint
problem += I[T-1] == 0

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')