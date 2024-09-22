import pulp

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Production_And_Inventory_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T+1), lowBound=0, cat='Continuous')

# Objective function
cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + pulp.lpSum([switch_cost * abs(x[i+1] - x[i]) for i in range(T-1)]) 
problem += cost

# Constraints
problem += (inventory[0] == 0)  # Beginning inventory is zero
for i in range(T):
    if i == 0:
        problem += (x[i] - deliver[i] + inventory[i] == inventory[i + 1])
    else:
        problem += (x[i] - deliver[i] + inventory[i] == inventory[i + 1])
        
# Solve the problem
problem.solve()

# Prepare output
productions = [x[i].varValue for i in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "x": productions,
    "cost": total_cost,
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')