import pulp
import json

# Parse data from JSON format
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0)
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
            pulp.lpSum(switch_cost * (pulp.lpSum(x[i] - x[i - 1] for i in range(2, T + 1)) if i > 1 else 0) for i in range(1, T + 1))

# Constraints
I[0] = 0  # Initial inventory

for i in range(1, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1]  # Inventory balance
problem += I[T] == 0  # End of year inventory constraint

# Solve the problem
problem.solve()

# Output results
production = [x[i].varValue for i in range(1, T + 1)]
cost = pulp.value(problem.objective)

print(f'Production levels: {production}')
print(f' (Objective Value): <OBJ>{cost}</OBJ>')