import pulp
import json

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Thrust_Optimization", pulp.LpMinimize)

# Create decision variables for position, velocity, and acceleration
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: Minimize the total fuel (sum of absolute accelerations)
problem += pulp.lpSum([pulp.lpSum([a_t]) for a_t in a]), "TotalFuel"

# Initial conditions
problem += (x[0] == x_0, "InitialPosition")
problem += (v[0] == v_0, "InitialVelocity")

# Dynamics constraints
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionConstraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityConstraint_{t}")

# Final conditions
problem += (x[T] == x_T, "FinalPosition")
problem += (v[T] == v_T, "FinalVelocity")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output in the required format
print(json.dumps(output))