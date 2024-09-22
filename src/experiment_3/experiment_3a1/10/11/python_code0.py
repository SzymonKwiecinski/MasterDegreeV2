import pulp
import json

# Input data
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

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, T))

# Constraints
I[1] = x[1] - deliver[0]  # Initial inventory equation
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1], f"Inventory_Balance_{i}"

problem += I[T] == 0  # Final inventory constraint

# Solve the problem
problem.solve()

# Output results
production_schedule = [x[i].varValue for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Production Schedule: {production_schedule}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')