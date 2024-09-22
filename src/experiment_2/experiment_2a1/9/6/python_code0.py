import pulp
import json

data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Fuel_Minimization", pulp.LpMinimize)

# Create decision variables for position, velocity, and acceleration
x = [pulp.LpVariable(f"x_{t}", lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f"v_{t}", lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f"a_{t}", lowBound=None) for t in range(T)]

# Objective function: Minimize the total fuel spent (sum of |a_t|)
problem += pulp.lpSum(pulp.abs(a[t]) for t in range(T))

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Constraints for position and velocity updates
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])  # Position update
    problem += (v[t + 1] == v[t] + a[t])  # Velocity update

# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Solve the problem
problem.solve()

# Collect results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Prepare output in the required format
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')