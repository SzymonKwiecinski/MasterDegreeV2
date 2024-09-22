import pulp

# Data from JSON
data = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Extracting data
X0 = data['X0']
V0 = data['V0']
XT = data['XT']
VT = data['VT']
T = data['T']

# Define problem
problem = pulp.LpProblem("RocketMotionOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T + 1))
v = pulp.LpVariable.dicts("v", range(T + 1))
a = pulp.LpVariable.dicts("a", range(T), lowBound=None)

# Auxiliary variables for thrust
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0)

# Objective function: Minimize the maximum thrust required
max_abs_a = pulp.LpVariable("max_abs_a", lowBound=0)
problem += max_abs_a

# Constraints
for t in range(T):
    problem += x[t + 1] == x[t] + v[t], f"Position_dynamics_{t}"
    problem += v[t + 1] == v[t] + a[t], f"Velocity_dynamics_{t}"
    problem += abs_a[t] >= a[t], f"Positive_abs_a_{t}"
    problem += abs_a[t] >= -a[t], f"Negative_abs_a_{t}"
    problem += max_abs_a >= abs_a[t], f"Max_abs_a_constraint_{t}"

# Initial conditions
problem += x[0] == X0, "Initial_position"
problem += v[0] == V0, "Initial_velocity"

# Target conditions
problem += x[T] == XT, "Target_position"
problem += v[T] == VT, "Target_velocity"

# Solve the problem
problem.solve()

# Calculate total fuel spent
fuel_spent = sum(abs_a[t].varValue for t in range(T))

# Prepare output
output = {
    "x": [x[i].varValue for i in range(T + 1)],
    "v": [v[i].varValue for i in range(T + 1)],
    "a": [a[i].varValue for i in range(T)],
    "fuel_spend": fuel_spent
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')