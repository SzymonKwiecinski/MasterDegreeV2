import pulp
import json

# Given data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Variables
T = data['TotalTime']
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration only for t=0 to T-1

# Create the problem
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

# Objective function: Minimize total fuel consumed
problem += pulp.lpSum([pulp.abs(a[t]) for t in range(T)]), "TotalFuel"

# Initial conditions
x[0] = data['InitialPosition']
v[0] = data['InitialVelocity']

# Constraints for motion equations
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"PositionConstraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"VelocityConstraint_{t}"

# Final conditions
problem += x[T] == data['FinalPosition'], "FinalPositionConstraint"
problem += v[T] == data['FinalVelocity'], "FinalVelocityConstraint"

# Solve the problem
problem.solve()

# Collect results
results = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{results["fuel_spend"]}</OBJ>')

# Optionally, print the results in JSON format
print(json.dumps(results, indent=4))