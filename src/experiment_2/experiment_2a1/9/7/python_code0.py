import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)       # Acceleration

# Objective: Minimize the maximum thrust (acceleration)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints
problem += x[0] == x0  # Initial position
problem += v[0] == v0  # Initial velocity

for t in range(T):
    problem += x[t + 1] == x[t] + v[t]  # Position update
    problem += v[t + 1] == v[t] + a[t]  # Velocity update
    problem += a[t] <= max_thrust        # Acceleration must not exceed max_thrust
    problem += a[t] >= -max_thrust       # Acceleration must not exceed -max_thrust

problem += x[T] == xT  # Final position constraint
problem += v[T] == vT  # Final velocity constraint

# Solve the problem
problem.solve()

# Prepare output
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust) * T  # Assuming fuel spent is proportional to max thrust and time

# Output
output = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

# Print results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')