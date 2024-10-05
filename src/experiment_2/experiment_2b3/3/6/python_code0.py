import pulp

# Data from JSON
data = {
    'InitialPosition': 0,
    'InitialVelocity': 0,
    'FinalPosition': 1,
    'FinalVelocity': 0,
    'TotalTime': 20
}

# Extract data
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Create a linear programming problem
problem = pulp.LpProblem("RocketOptimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T + 1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T + 1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), lowBound=None, cat='Continuous')
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(abs_a[t] for t in range(T))

# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# State update constraints
for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]
    
    # Absolute value constraints
    problem += abs_a[t] >= a[t]
    problem += abs_a[t] >= -a[t]

# Solve the problem
problem.solve()

# Prepare the solution
output = {
    "x": [pulp.value(x[i]) for i in range(T+1)],
    "v": [pulp.value(v[i]) for i in range(T+1)],
    "a": [pulp.value(a[i]) for i in range(T)],
    "fuel_spend": pulp.value(problem.objective),
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')