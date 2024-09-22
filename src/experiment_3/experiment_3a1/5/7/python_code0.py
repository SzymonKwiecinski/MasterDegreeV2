import pulp
import json

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Create the problem
problem = pulp.LpProblem("Rocket_Dynamics", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)  # acceleration
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # velocity

# Initial conditions
x[0] = x0
v[0] = v0

# Constraints for state dynamics
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}"

# Final conditions
problem += x[T] == xT, "Final_Position"
problem += v[T] == vT, "Final_Velocity"

# Objective function: minimize the maximum acceleration
max_a = pulp.LpVariable("max_a", lowBound=None)
problem += max_a

# Adding the constraints for maximum acceleration
for t in range(T):
    problem += a[t] <= max_a, f"Max_Acceleration_Upper_{t}"
    problem += -a[t] <= max_a, f"Max_Acceleration_Lower_{t}"

# Solve the problem
problem.solve()

# Collect results
result = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T)],
    "fuel_spend": pulp.value(max_a)  # Assuming fuel spent is directly related to max acceleration
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the results in the desired format
print(json.dumps(result, indent=4))