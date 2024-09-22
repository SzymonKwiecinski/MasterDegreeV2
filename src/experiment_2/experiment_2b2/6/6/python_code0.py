import pulp

# Data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}
x_0 = data['InitialPosition']
v_0 = data['InitialVelocity']
x_T = data['FinalPosition']
v_T = data['FinalVelocity']
T = data['TotalTime']

# Problem setup
problem = pulp.LpProblem("Rocket_Control_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T+1), cat='Continuous')
v = pulp.LpVariable.dicts("v", range(T+1), cat='Continuous')
a = pulp.LpVariable.dicts("a", range(T), cat='Continuous')
abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize the total fuel consumption
problem += pulp.lpSum(abs_a[t] for t in range(T))

# Constraints
# Initial conditions
problem += x[0] == x_0
problem += v[0] == v_0

# State equations
for t in range(T):
    problem += x[t+1] == x[t] + v[t]
    problem += v[t+1] == v[t] + a[t]
    # Absolute value constraints
    problem += abs_a[t] >= a[t]
    problem += abs_a[t] >= -a[t]

# Final conditions
problem += x[T] == x_T
problem += v[T] == v_T

# Solve the problem
problem.solve()

# Retrieve results
x_values = [x[t].varValue for t in range(T+1)]
v_values = [v[t].varValue for t in range(T+1)]
a_values = [a[t].varValue for t in range(T)]
fuel_spent = pulp.value(problem.objective)

# Output format
output = {
    "x": x_values,
    "v": v_values,
    "a": a_values,
    "fuel_spend": fuel_spent,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')