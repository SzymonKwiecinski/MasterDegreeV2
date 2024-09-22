import pulp
import json

# Data input
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the problem
problem = pulp.LpProblem("Rocket_Trajectory", pulp.LpMinimize)

# Define the variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T+1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T+1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: Minimize total fuel spent
problem += pulp.lpSum([pulp.lpAbs(a_t) for a_t in a]), "Total_Fuel_Spent"

# Initial conditions
problem += x[0] == x_0, "Initial_Position"
problem += v[0] == v_0, "Initial_Velocity"

# Constraints for the rocket motion
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Final conditions
problem += x[T] == x_T, "Final_Position"
problem += v[T] == v_T, "Final_Velocity"

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

# If needed to see the output structure
print(json.dumps(output, indent=2))