import pulp
import json

# Data provided in JSON format
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Extracting data from the JSON
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_X", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, T+1), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([x[j] for j in range(1, T+1)]), "Total_x"

# Constraints
for j in range(1, T+1):
    problem += (pulp.lpSum([x[(j-i-1) % T + 1] for i in range(Period)]) >= Demand[j-1]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')