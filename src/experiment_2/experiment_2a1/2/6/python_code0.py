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
problem = pulp.LpProblem("Rocket_Problem", pulp.LpMinimize)

# Decision variables for positions, velocities, and accelerations
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective function: minimize total fuel spent
problem += pulp.lpSum([pulp.lpAbs(a_t) for a_t in a]), "Total_Fuel"

# Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")

problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

# Solve the problem
problem.solve()

# Collect the results
result_x = [pulp.value(x[t]) for t in range(T + 1)]
result_v = [pulp.value(v[t]) for t in range(T + 1)]
result_a = [pulp.value(a[t]) for t in range(T)]

# Calculate total fuel spent
fuel_spent = pulp.value(problem.objective)

# Prepare output
output = {
    "x": result_x,
    "v": result_v,
    "a": result_a,
    "fuel_spend": fuel_spent,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')