import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
I = [pulp.LpVariable(f'I_{i}', lowBound=0, cat='Continuous') for i in range(T)]

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * pulp.lpSum(x[i+1] - x[i] for i in range(T-1) if x[i+1] > x[i]))

# Constraints
problem += (I[0] == 0), "Initial_Inventory_Constraint"

for i in range(T):
    if i == 0:
        problem += (x[i] == deliver[i] + I[i]), f"Balance_Constraint_{i}"
    else:
        problem += (I[i-1] + x[i] == deliver[i] + I[i]), f"Balance_Constraint_{i}"

# Solve
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')