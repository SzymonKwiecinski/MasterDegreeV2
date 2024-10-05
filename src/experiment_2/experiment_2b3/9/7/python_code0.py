import pulp

# Create a Linear Programming problem
problem = pulp.LpProblem("Rocket_Control", pulp.LpMinimize)

# Extract data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
max_a = pulp.LpVariable("max_a", lowBound=0, cat='Continuous')

# Objective: Minimize the maximum thrust required
problem += max_a

# Constraints
problem += x[0] == x_0
problem += v[0] == v_0
problem += x[T] == x_T
problem += v[T] == v_T

for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]
    problem += a[t] <= max_a
    problem += -a[t] <= max_a  # equivalent to |a_t| <= max_a

# Solve the problem
problem.solve()

# Extract results
x_values = [pulp.value(x[t]) for t in range(T+1)]
v_values = [pulp.value(v[t]) for t in range(T+1)]
a_values = [pulp.value(a[t]) for t in range(T)]

fuel_spent = sum(abs(a_i) for a_i in a_values)

output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')