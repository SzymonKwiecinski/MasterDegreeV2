import pulp

# Extract data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

num_days = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Define the problem
problem = pulp.LpProblem("Cafeteria_Employee_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, n) for i in range(num_days) for n in range(num_days)),
                          cat='Binary')

# Objective function: Minimize the total number of employees needed
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
problem += total_number

# Constraints
# Ensure enough employees each day
for n in range(num_days):
    problem += pulp.lpSum(x[i, n] for i in range(num_days)) >= data['num'][n]

# Working and resting schedule constraints
for i in range(num_days):
    for k in range(num_days - n_working_days - n_resting_days + 1):
        # If working for n_working_days
        for n in range(k, k + n_working_days):
            if n < num_days:
                problem += x[i, n] == 1

        # Then resting for n_resting_days
        for n_prime in range(k + n_working_days, k + n_working_days + n_resting_days):
            if n_prime < num_days:
                problem += x[i, n_prime] == 0

# The total_number should be at least the maximum active employees any day
for n in range(num_days):
    problem += total_number >= pulp.lpSum(x[i, n] for i in range(num_days))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')