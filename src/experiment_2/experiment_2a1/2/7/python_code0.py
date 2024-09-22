import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Position", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("Velocity", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("Acceleration", range(T), lowBound=None)

# Objective function: Minimize the maximum thrust
max_thrust = pulp.LpVariable("MaxThrust")
problem += max_thrust

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Constraints for position and velocity evolution
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    
# Final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Acceleration limits
for t in range(T):
    problem += (a[t] <= max_thrust)
    problem += (a[t] >= -max_thrust)

# Solve the problem
problem.solve()

# Collect results
positions = [pulp.value(x[t]) for t in range(T + 1)]
velocities = [pulp.value(v[t]) for t in range(T + 1)]
accelerations = [pulp.value(a[t]) for t in range(T)]
fuel_spent = pulp.value(max_thrust) * T  # Assuming fuel spent is max thrust times the duration

# Output results
results = {
    "x": positions,
    "v": velocities,
    "a": accelerations,
    "fuel_spend": fuel_spent,
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')