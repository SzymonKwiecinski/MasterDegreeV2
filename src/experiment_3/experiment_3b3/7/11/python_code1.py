import pulp

# Constants from data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]
I = [pulp.LpVariable(f"I_{i}", lowBound=0, cat='Continuous') for i in range(T)]

# Objective function
problem += pulp.lpSum([storage_cost * I[i] for i in range(T)]) + \
           pulp.lpSum([switch_cost * (x[i+1] - x[i])**2 for i in range(T-1)])**0.5

# Initial inventory constraint
problem += (I[0] == 0 + x[0] - deliver[0]), "Initial_Inventory"

# Inventory balance constraints
for i in range(1, T):
    problem += (I[i] == I[i-1] + x[i] - deliver[i]), f"Inventory_Balance_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')