import pulp
import json

# Load input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define decision variables for acceleration, position, and velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)  # velocity

# Initial conditions
problem += (x[0] == x_0, "Initial_Position_Condition")
problem += (v[0] == v_0, "Initial_Velocity_Condition")

# Constraints for position and velocity
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

# Final conditions
problem += (x[T] == x_T, "Final_Position_Condition")
problem += (v[T] == v_T, "Final_Velocity_Condition")

# Objective: Minimize total fuel spent (sum of absolute values of acceleration)
fuel_spent = pulp.lpSum([pulp.lpSum([a[t], -a[t]]) for t in range(T)])
problem += fuel_spent, "Minimize_Fuel_Spent"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')