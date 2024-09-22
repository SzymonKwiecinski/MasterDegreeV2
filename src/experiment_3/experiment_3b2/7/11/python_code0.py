import pulp
import json

# Data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0)
I = pulp.LpVariable.dicts("I", range(T), lowBound=0)
y = pulp.LpVariable.dicts("y", range(T-1), lowBound=0)

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(T)) + pulp.lpSum(switch_cost * y[i] for i in range(T-1))

# Constraints
problem += I[0] == 0  # Initial Inventory

for i in range(1, T):
    problem += x[i] + I[i-1] == deliver[i] + I[i]  # Inventory balance
    problem += y[i-1] >= x[i] - x[i-1]  # Switch cost constraint
    problem += y[i-1] >= x[i-1] - x[i]  # Switch cost constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')