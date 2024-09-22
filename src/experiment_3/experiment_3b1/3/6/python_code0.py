import pulp
import json

# Data from the provided JSON format
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Problem setup
T = data['TotalTime']
x0 = data['InitialPosition']
v0 = data['InitialVelocity']
xT = data['FinalPosition']
vT = data['FinalVelocity']

# Create the problem
problem = pulp.LpProblem("Rocket_Motion_Optimization", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Objective function: Minimize the sum of absolute values of acceleration
problem += pulp.lpSum([pulp.lpAbs(a[t]) for t in range(T)])

# Initial conditions
problem += x[0] == x0
problem += v[0] == v0

# Final state requirements
problem += x[T] == xT
problem += v[T] == vT

# Constraints for dynamics
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]

# Solve the problem
problem.solve()

# Gather the results
result = {
    "x": [x[t].varValue for t in range(T + 1)],
    "v": [v[t].varValue for t in range(T + 1)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Output results
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')