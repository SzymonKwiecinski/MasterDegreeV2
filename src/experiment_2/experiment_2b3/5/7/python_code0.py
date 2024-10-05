import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Problem
problem = pulp.LpProblem("Rocket_Optimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T))
M = pulp.LpVariable("M", lowBound=0)  # Maximum thrust

# Objective
problem += M

# Initial conditions
problem += (x[0] == X0, "Initial_Position")
problem += (v[0] == V0, "Initial_Velocity")

# Final conditions
problem += (x[T] == XT, "Final_Position")
problem += (v[T] == VT, "Final_Velocity")

# State transitions and max thrust constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
    problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
    problem += (a[t] <= M, f"Max_Thrust_Positive_{t}")
    problem += (a[t] >= -M, f"Max_Thrust_Negative_{t}")

# Solve
problem.solve()

# Collect results
x_values = [x[t].varValue for t in range(T+1)]
v_values = [v[t].varValue for t in range(T+1)]
a_values = [a[t].varValue for t in range(T)]

fuel_spent = sum(abs(a[t].varValue) for t in range(T))

result = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')