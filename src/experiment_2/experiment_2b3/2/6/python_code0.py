import pulp

# Extracting data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Define LP problem
problem = pulp.LpProblem("RocketFuelMinimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum(pulp.lpAbs(a[t]) for t in range(T))

# Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")
problem += (x[T] == x_T, "Final_Position")
problem += (v[T] == v_T, "Final_Velocity")

for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Constraint_{t}")

# Solving the problem
problem.solve()

# Extracting the results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

result = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')