import pulp

# Data
data = {
    'X0': 0, 
    'V0': 0, 
    'XT': 1, 
    'VT': 0, 
    'T': 20
}

# Define the LP problem
problem = pulp.LpProblem("Minimize_M", pulp.LpMinimize)

# Define variables
x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(data['T'] + 1)]
v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(data['T'] + 1)]
a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(data['T'])]
M = pulp.LpVariable('M', lowBound=0, cat='Continuous')

# Objective function
problem += M

# Constraints
problem += (x[0] == data['X0'])
problem += (v[0] == data['V0'])
problem += (x[data['T']] == data['XT'])
problem += (v[data['T']] == data['VT'])

for t in range(data['T']):
    problem += (x[t+1] == x[t] + v[t])
    problem += (v[t+1] == v[t] + a[t])
    problem += (a[t] <= M)
    problem += (-a[t] <= M)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')