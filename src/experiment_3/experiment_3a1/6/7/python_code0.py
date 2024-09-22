import pulp

# Data from the provided JSON format
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Trajectory_Optimization", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Initial conditions
problem += (x[0] == x0, "InitialPosition")
problem += (v[0] == v0, "InitialVelocity")

# Dynamic equations of motion
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"PositionUpdate_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"VelocityUpdate_{t}")

# Boundary conditions
problem += (x[T] == xT, "FinalPosition")
problem += (v[T] == vT, "FinalVelocity")

# Objective: Minimize the maximum thrust (max |a_t|)
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
for t in range(T):
    problem += (max_thrust >= a[t], f"MaxThrustConstraint_{t}")
    problem += (max_thrust >= -a[t], f"MaxThrustNegativeConstraint_{t}")

problem += pulp.lpSum([abs(a[t]) for t in range(T)])  # Fuel consumption

# Solve the problem
problem.solve()

# Extract results
x_result = [x[i].varValue for i in range(T + 1)]
v_result = [v[i].varValue for i in range(T + 1)]
a_result = [a[i].varValue for i in range(T)]

# Calculate fuel spent
fuel_spent = sum(abs(a[i].varValue) for i in range(T))

# Output the results
output = {
    "x": x_result,
    "v": v_result,
    "a": a_result,
    "fuel_spend": fuel_spent
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')