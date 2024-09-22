import pulp

# Data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T+1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(0, T+1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (x[i+1] - x[i] if i < T else 0) for i in range(1, T+1)), "Total_Cost"

# Constraints
problem += I[0] == 0  # Initial inventory

for i in range(1, T+1):
    problem += I[i] == I[i-1] + x[i] - deliver[i-1], f"Inventory_Constraint_{i}"

# Solve the problem
problem.solve()

# Output results
production_plan = [x[i].varValue for i in range(1, T+1)]
print(f'Production Plan: {production_plan}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')