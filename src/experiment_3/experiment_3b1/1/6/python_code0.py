import pulp

# Data from JSON format
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Create the linear programming problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=None) for t in range(T + 1)]
v = [pulp.LpVariable(f'v_{t}', lowBound=None) for t in range(T + 1)]
a = [pulp.LpVariable(f'a_{t}', lowBound=None) for t in range(T)]

# Objective Function: Minimize total fuel spent
fuel_spent = pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])  # Fuel is the sum of absolute accelerations
problem += fuel_spent, "Total_Fuel"

# Constraints
problem += (x[0] == x0, "Initial_Position")
problem += (v[0] == v0, "Initial_Velocity")
problem += (x[T] == xT, "Final_Position")
problem += (v[T] == vT, "Final_Velocity")

# Recursive equations
for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_{t}")

# Solve the problem
problem.solve()

# Collect results
x_values = [x[t].varValue for t in range(T + 1)]
v_values = [v[t].varValue for t in range(T + 1)]
a_values = [a[t].varValue for t in range(T)]
fuel_spend = pulp.value(problem.objective)

# Output
print(f"x = {x_values}")
print(f"v = {v_values}")
print(f"a = {a_values}")
print(f'fuel_spend = {fuel_spend}')
print(f' (Objective Value): <OBJ>{fuel_spend}</OBJ>')