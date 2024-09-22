import pulp

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Planning", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')
switch = pulp.LpVariable.dicts("Switch", range(T-1), lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T))
switch_cost_term = pulp.lpSum(switch_cost * switch[i] for i in range(T-1))
problem += total_cost + switch_cost_term

# Constraints
problem += inventory[0] == x[0] - deliver[0]
for i in range(1, T):
    problem += inventory[i] == inventory[i-1] + x[i] - deliver[i]
for i in range(T-1):
    problem += switch[i] >= x[i+1] - x[i]
    problem += switch[i] >= x[i] - x[i+1]

# Solve the problem
problem.solve()

# Output result
production_plan = [pulp.value(x[i]) for i in range(T)]
result = {
    "x": production_plan,
    "cost": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')