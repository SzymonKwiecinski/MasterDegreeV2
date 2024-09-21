import pulp
import json

# Data input
data = json.loads('{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}')

# Parameters
NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Create a problem variable
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(NumProducts), lowBound=0)

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumProducts)]), "Total_Profit"

# Constraints
for m in range(NumMachines):
    problem += pulp.lpSum([ProduceTime[k][m] * x[k] for k in range(NumProducts)]) <= AvailableTime[m], f"Time_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')