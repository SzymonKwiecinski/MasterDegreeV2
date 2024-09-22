import pulp

# Extract data from JSON
data = {
    "x_0": 0,
    "v_0": 0,
    "x_T": 1,
    "v_T": 0,
    "T": 20
}

x_0 = data['x_0']
v_0 = data['v_0']
x_T = data['x_T']
v_T = data['v_T']
T = data['T']

# Create a linear programming problem
problem = pulp.LpProblem("RocketTrajectory", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Position", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("Velocity", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("Acceleration", range(T), cat='Continuous')
abs_a = pulp.LpVariable.dicts("AbsAcceleration", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize total fuel spend
problem += pulp.lpSum(abs_a[t] for t in range(T)), "TotalFuelSpend"

# Constraints
problem += x[0] == x_0, "InitialPosition"
problem += v[0] == v_0, "InitialVelocity"
problem += x[T] == x_T, "FinalPosition"
problem += v[T] == v_T, "FinalVelocity"

for t in range(T):
    problem += x[t+1] == x[t] + v[t], f"PositionUpdate_{t}"
    problem += v[t+1] == v[t] + a[t], f"VelocityUpdate_{t}"
    problem += abs_a[t] >= a[t], f"PosAbsAccel_{t}"
    problem += abs_a[t] >= -a[t], f"NegAbsAccel_{t}"

# Solve the problem
problem.solve()

# Extract the results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(a_val) for a_val in a_values)

# Output in the specified format
output = {
    "x": x_values[1:],
    "v": v_values[1:],
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')