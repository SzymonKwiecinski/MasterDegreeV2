import pulp
import json

# Data from JSON
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')

# Parameters
T = data['T']
Deliver = data['Deliver']
StorageCost = data['StorageCost']
SwitchCost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)
I = pulp.LpVariable.dicts("I", range(T + 1), lowBound=0)
switch_vars = pulp.LpVariable.dicts("switch", range(1, T + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(StorageCost * I[i] for i in range(1, T + 1)) + pulp.lpSum(SwitchCost * switch_vars[i] for i in range(1, T)), "Total_Cost"

# Constraints
for i in range(1, T + 1):
    if i == 1:
        problem += x[i] + I[0] - I[i] == Deliver[i - 1], f"Balance_Constraint_{i}"
    else:
        problem += x[i] + I[i - 1] - I[i] == Deliver[i - 1], f"Balance_Constraint_{i}"
        
    if i < T:
        problem += switch_vars[i] >= x[i] - x[i - 1], f"Switch_Constraint_Upper_{i}"
        problem += switch_vars[i] >= x[i - 1] - x[i], f"Switch_Constraint_Lower_{i}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')