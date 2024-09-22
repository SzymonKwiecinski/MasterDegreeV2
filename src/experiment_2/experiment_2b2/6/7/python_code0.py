import pulp

# Parse the input data
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Set the parameters
x_0 = data['X0']
v_0 = data['V0']
x_T = data['XT']
v_T = data['VT']
T = data['T']

# Create the LP problem
problem = pulp.LpProblem("Rocket_Path_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1))
v = pulp.LpVariable.dicts("v", range(T + 1))
a = pulp.LpVariable.dicts("a", range(T))
max_a = pulp.LpVariable("max_a", lowBound=0)

# Objective function: minimize the maximum thrust required
problem += max_a

# Constraints
problem += (x[0] == x_0)
problem += (v[0] == v_0)
problem += (x[T] == x_T)
problem += (v[T] == v_T)

for t in range(T):
    problem += (x[t + 1] == x[t] + v[t])
    problem += (v[t + 1] == v[t] + a[t])
    problem += (a[t] <= max_a)
    problem += (-a[t] <= max_a)

# Solve the problem
problem.solve()

# Gather the results
x_result = [pulp.value(x[i]) for i in range(T + 1)]
v_result = [pulp.value(v[i]) for i in range(T + 1)]
a_result = [pulp.value(a[i]) for i in range(T)]

fuel_spent = sum(abs(a_i) for a_i in a_result)

# Output the results in the required format
output = {
    "x": x_result,
    "v": v_result,
    "a": a_result,
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')