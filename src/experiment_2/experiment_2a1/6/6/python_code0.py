import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Unpack data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize fuel consumption
problem += pulp.lpSum([pulp.lpSum([a[t] for t in range(T)])]), "TotalFuel"

# Constraints
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionUpdate_t{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityUpdate_t{t}")

problem += (x[T] == x_T, "FinalPosition")
problem += (v[T] == v_T, "FinalVelocity")

# Solve the problem
problem.solve()

# Extract results
positions = [x[t].varValue for t in range(T + 1)]
velocities = [v[t].varValue for t in range(T + 1)]
accelerations = [a[t].varValue for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Format output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')