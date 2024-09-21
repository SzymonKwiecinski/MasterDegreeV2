import pulp
import json

# Data in JSON format
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Extract data
T = data['T']
Demand = data['Demand']

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Define decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Continuous')

# Objective function
problem += N, "Minimize_Nurses"

# Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_{t+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')