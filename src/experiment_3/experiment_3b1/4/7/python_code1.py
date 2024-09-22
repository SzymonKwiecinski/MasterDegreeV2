import pulp
import json

# Given data
data = json.loads('{"X0": 0, "V0": 0, "XT": 1, "VT": 0, "T": 20}')
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']
M = 10  # Assume a maximum thrust capacity

# Create a linear programming problem
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1), lowBound=None)
v = pulp.LpVariable.dicts("v", range(T + 1), lowBound=None)
a = pulp.LpVariable.dicts("a", range(T + 1), lowBound=-M, upBound=M)

# Objective function: minimize the maximum thrust required
max_accel = pulp.LpVariable("max_accel", lowBound=None)
problem += max_accel

# Constraints
problem += (x[0] == x_0, "Initial_Position")
problem += (v[0] == v_0, "Initial_Velocity")
problem += (x[T] == x_T, "Target_Position")
problem += (v[T] == v_T, "Target_Velocity")

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t], f"Position_Constraint_{t}")
    problem += (v[t + 1] == v[t] + a[t], f"Velocity_Constraint_{t}")
    problem += (max_accel >= a[t], f"Max_Accel_Constraint_Upper_{t}")
    problem += (max_accel >= -a[t], f"Max_Accel_Constraint_Lower_{t}")

# Solve the problem
problem.solve()

# Collect results
result = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T + 1)],
    "fuel_spend": None  # Fuel consumption details not specified
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')