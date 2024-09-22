import pulp

# Data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Problem
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]
max_thrust = pulp.LpVariable("max_thrust", lowBound=0, cat='Continuous')

# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Target conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Constraints for motion equations
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (max_thrust >= a[t])
    problem += (max_thrust >= -a[t])

# Objective
problem += max_thrust

# Solve
problem.solve()

# Output
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]
fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))

result = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')