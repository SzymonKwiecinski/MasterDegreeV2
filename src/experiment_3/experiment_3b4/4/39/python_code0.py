import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_days = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(num_days), cat='Binary') 
y = pulp.LpVariable.dicts("y", (range(num_days), range(num_days)), cat='Binary') 

# Objective
problem += pulp.lpSum(x[i] for i in range(num_days))

# Constraints
for n in range(num_days):
    # Ensure the number of employees working each day meets the requirement
    problem += pulp.lpSum(y[i][n] for i in range(num_days)) >= data['num'][n]

for i in range(num_days):
    for n in range(num_days):
        # An employee works only if they are employed
        problem += y[i][n] <= x[i]
        
        # Working/resting schedule constraints
        if (n % (n_working_days + n_resting_days)) >= n_working_days:
            problem += y[i][n] == 0

# Solve
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')