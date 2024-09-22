import pulp

# Given data from JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Extracting values from the data
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the optimization problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Decision variables for acceleration
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat='Continuous')
# Decision variables for position and velocity
x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None, cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None, cat='Continuous')

# Objective function: Minimize total fuel consumption (total acceleration)
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)]), "Total_Fuel_Spent"

# Initial conditions
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

# Dynamic constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Final conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

# Solve the problem
problem.solve()

# Gather results
fuel_spent = pulp.value(problem.objective)
x_values = [pulp.value(x[t]) for t in range(T + 1)]
v_values = [pulp.value(v[t]) for t in range(T + 1)]
a_values = [pulp.value(a[t]) for t in range(T)]

# Prepare output
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(f' (Objective Value): <OBJ>{fuel_spent}</OBJ>')