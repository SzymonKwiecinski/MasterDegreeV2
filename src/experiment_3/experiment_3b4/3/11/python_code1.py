import pulp

# Data from provided JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Extracting data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Initialize the Problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]
I = [pulp.LpVariable(f"I{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]

# Objective Function
storage_cost_term = pulp.lpSum(storage_cost * I[i] for i in range(T))
switch_cost_term = pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(T-1))
problem += storage_cost_term + switch_cost_term

# Constraints
# Initial Inventory Constraint
problem += I[0] == 0

# Inventory Balance Constraints
for i in range(T):
    if i == 0:
        problem += I[i] == x[i] - deliver[i]
    else:
        problem += I[i] == I[i-1] + x[i] - deliver[i]

# Solve the Problem
problem.solve()

# Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')