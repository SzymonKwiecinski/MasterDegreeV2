import pulp

# Define the problem
problem = pulp.LpProblem("Rocket_Problem", pulp.LpMinimize)

# Extract Input Data
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1))
v = pulp.LpVariable.dicts("v", range(T+1))
a = pulp.LpVariable.dicts("a", range(T))

# Objective Function: Minimize total fuel, which is the sum of absolute values of a_t
# To account for absolute values, we introduce additional variables
a_pos = pulp.LpVariable.dicts("a_pos", range(T), lowBound=0)
a_neg = pulp.LpVariable.dicts("a_neg", range(T), lowBound=0)

for t in range(T):
    problem += (a[t] == a_pos[t] - a_neg[t])  # Equation to express a_t in terms of a_pos and a_neg
    problem += (a_pos[t] >= 0)  # a_t should be equal to the positive part
    problem += (a_neg[t] >= 0)  # a_t should be equal to the negative part

problem += pulp.lpSum(a_pos[t] + a_neg[t] for t in range(T))  # Objective function

# Constraints
# Initial conditions
problem += (x[0] == x_0)
problem += (v[0] == v_0)

# Final constraints
problem += (x[T] == x_T)
problem += (v[T] == v_T)

# Dynamic Constraints
for t in range(T):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])

# Solve the problem
problem.solve()

# Prepare Output
output = {
    "x": [pulp.value(x[t]) for t in range(T+1)],
    "v": [pulp.value(v[t]) for t in range(T+1)],
    "a": [pulp.value(a[t]) for t in range(T)],
    "fuel_spend": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')