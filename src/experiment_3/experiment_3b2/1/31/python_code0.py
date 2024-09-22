import pulp
import json

# Data provided in JSON format
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Parameters
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(K), range(T)), lowBound=0, cat='Integer')  # Number of generators operating
y = pulp.LpVariable.dicts("y", (range(K), range(T)), cat='Binary')                # Generator start
z = pulp.LpVariable.dicts("z", (range(K), range(T)), lowBound=0)                  # Extra megawatts

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * x[k][t] + data['extracost'][k] * z[k][t] + data['startcost'][k] * y[k][t] 
                      for t in range(T) for k in range(K)), "Total_Cost"

# Constraints

# Demand satisfaction constraint
for t in range(T):
    problem += pulp.lpSum(data['minlevel'][k] * x[k][t] + z[k][t] for k in range(K)) >= data['demand'][t], f"Demand_Constraint_{t}"

# Generator limit constraint
for t in range(T):
    for k in range(K):
        problem += x[k][t] <= data['num'][k] * y[k][t], f"Generator_Limit_Constraint_k{K}_t{t}"

# Capacity constraints
for t in range(T):
    for k in range(K):
        problem += 0 <= z[k][t] <= (data['maxlevel'][k] - data['minlevel'][k]) * x[k][t], f"Capacity_Constraint_k{k}_t{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')