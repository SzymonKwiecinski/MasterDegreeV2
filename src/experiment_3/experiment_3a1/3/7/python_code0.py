import pulp
import json

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x0 = data['X0']
v0 = data['V0']
xT = data['XT']
vT = data['VT']
T = data['T']

# Problem Definition
problem = pulp.LpProblem("Rocket Movement Optimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)  # Position
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)  # Velocity
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)       # Acceleration

# Objective Function: Minimize the maximum thrust required
max_thrust = pulp.LpVariable("max_thrust", lowBound=0)
problem += max_thrust

# Constraints
problem += (x[0] == x0, "Initial position")
problem += (v[0] == v0, "Initial velocity")
problem += (x[T] == xT, "Target position")
problem += (v[T] == vT, "Target velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position constraint at time {t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity constraint at time {t}")
    problem += (a[t] <= max_thrust, f"Thrust constraint at time {t}")
    problem += (a[t] >= -max_thrust, f"Negative thrust constraint at time {t}")

# Solve the problem
problem.solve()

# Extract outputs
result = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T)],
    "fuel_spend": pulp.value(max_thrust)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print result in JSON format
print(json.dumps(result, indent=2))