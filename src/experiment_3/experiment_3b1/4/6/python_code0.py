import pulp

# Data from the provided JSON format
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Parameters initialization
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']
T = data['TotalTime']

# Define the problem
problem = pulp.LpProblem("RocketMotion", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # Acceleration
v = pulp.LpVariable.dicts("v", range(T), lowBound=None)  # Velocity
x = pulp.LpVariable.dicts("x", range(T), lowBound=None)  # Position

# Objective function: Minimize sum of absolute accelerations
problem += pulp.lpSum([pulp.abs(a[t]) for t in range(T)]), "Total_Acceleration"

# Constraints
problem += x[0] == x0, "Initial_Position"
problem += v[0] == v0, "Initial_Velocity"

# Dynamics equations and target conditions
for t in range(T - 1):
    problem += x[t + 1] == x[t] + v[t], f"Position_Update_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Update_{t}"

problem += x[T - 1] == xT, "Final_Position"
problem += v[T - 1] == vT, "Final_Velocity"

# Solve the problem
problem.solve()

# Output results
result = {
    "x": [x[t].varValue for t in range(T)],
    "v": [v[t].varValue for t in range(T)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{result["fuel_spend"]}</OBJ>')