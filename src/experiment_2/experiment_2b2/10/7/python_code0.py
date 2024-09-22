import pulp

# Define the problem
problem = pulp.LpProblem("Rocket Optimization", pulp.LpMinimize)

# Read the data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Define variables
x = pulp.LpVariable.dicts("x", (range(T+1)), cat='Continuous')
v = pulp.LpVariable.dicts("v", (range(T+1)), cat='Continuous')
a = pulp.LpVariable.dicts("a", (range(T)), cat='Continuous')
a_abs = pulp.LpVariable.dicts("a_abs", (range(T)), lowBound=0, cat='Continuous')
A_max = pulp.LpVariable("A_max", lowBound=0, cat='Continuous')

# Objective: Minimize the maximum thrust (A_max)
problem += A_max

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Constraints for each time step
for t in range(T):
    problem += x[t + 1] == x[t] + v[t]
    problem += v[t + 1] == v[t] + a[t]
    problem += a_abs[t] >= a[t]
    problem += a_abs[t] >= -a[t]

# Constraint for A_max
problem += A_max >= pulp.lpSum(a_abs[t] for t in range(T))

# Solve the problem
problem.solve()

# Collect outputs
x_out = [x[t].varValue for t in range(T+1)]
v_out = [v[t].varValue for t in range(T+1)]
a_out = [a[t].varValue for t in range(T)]
fuel_spent = sum(abs(a_t) for a_t in a_out)

# Print results
output = {
    "x": x_out,
    "v": v_out,
    "a": a_out,
    "fuel_spend": fuel_spent
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')