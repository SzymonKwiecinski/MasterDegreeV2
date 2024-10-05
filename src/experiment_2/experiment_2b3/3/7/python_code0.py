import pulp

# Input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the LP problem
problem = pulp.LpProblem("RocketTrajectory", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T))
delta = pulp.LpVariable("delta", lowBound=0)

# Set the initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Add constraints for each time step
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] <= delta)
    problem += (a[t] >= -delta)

# Set the final conditions
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Objective function: Minimize the maximum absolute thrust
problem += delta

# Solve the optimization problem
problem.solve()

# Output results
result = {
    "x": [x[t].varValue for t in range(1, T+1)],
    "v": [v[t].varValue for t in range(1, T+1)],
    "a": [a[t].varValue for t in range(T)],
    "fuel_spend": sum(abs(a[t].varValue) for t in range(T)),
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')