import pulp

# Parse the input data
data = {
    'InitialPosition': 0, 
    'InitialVelocity': 0, 
    'FinalPosition': 1, 
    'FinalVelocity': 0, 
    'TotalTime': 20
}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Initialize the problem
problem = pulp.LpProblem("Rocket_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0)

# Objective: Minimize the absolute acceleration (fuel consumption)
problem += pulp.lpSum(abs_a[t] for t in range(T))

# Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    problem += (abs_a[t] >= a[t], f"Abs_Positive_{t}")
    problem += (abs_a[t] >= -a[t], f"Abs_Negative_{t}")

# Solve the problem
problem.solve()

# Extract the results
x_values = [pulp.value(x[i]) for i in range(T+1)]
v_values = [pulp.value(v[i]) for i in range(T+1)]
a_values = [pulp.value(a[i]) for i in range(T)]
fuel_spent = pulp.value(problem.objective)

# Format the output
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')