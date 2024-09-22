import pulp

# Data from JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Parameters
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Initialize the problem
problem = pulp.LpProblem("Production_Inventory_Planning", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(T)]
I = [pulp.LpVariable(f'I_{i}', lowBound=0) for i in range(T)]

# Objective function components
storage_costs = pulp.lpSum(storage_cost * I[i] for i in range(T))
switch_costs = pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(T-1)) + \
                          pulp.lpSum(switch_cost * (x[i] - x[i+1]) for i in range(T-1))

# Objective function
problem += storage_costs + switch_costs, "Total_Cost"

# Constraints
# Initial inventory
problem += (I[0] == x[0] - deliver[0]), "Inventory_Constraint_0"

# Remaining inventory constraints
for i in range(1, T):
    problem += (I[i] == I[i-1] + x[i] - deliver[i]), f"Inventory_Constraint_{i}"

# Solve the problem
problem.solve()

# Results
for i in range(T):
    print(f'Month {i+1}: Produced {x[i].varValue} units, Inventory {I[i].varValue} units')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')