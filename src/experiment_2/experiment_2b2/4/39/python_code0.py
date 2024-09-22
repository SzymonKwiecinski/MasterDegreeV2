import pulp

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Number of days
N = len(data['num'])

# Working and resting days configuration
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
total_cycle_days = n_working_days + n_resting_days

# Create the problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Decision variables: is_employee_i_working_on_day_n
max_possible_employees = sum(data['num'])  # Overestimate
is_work = pulp.LpVariable.dicts("is_work", ((i, n) for i in range(max_possible_employees) for n in range(N)), 
                                cat='Binary')

# Objective function: Minimize total employees
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
problem += total_number

# Constraints

# Ensure enough employees are working each day
for n in range(N):
    problem += pulp.lpSum(is_work[i, n] for i in range(max_possible_employees)) >= data['num'][n]

# Ensure each employee follows the working/resting cycle
for i in range(max_possible_employees):
    for n in range(N):
        if n + total_cycle_days <= N:
            problem += pulp.lpSum(is_work[i, m] for m in range(n, n + n_working_days)) >= n_working_days * is_work[i, n]

# Constraint to determine total number of employees used
for i in range(max_possible_employees):
    problem += pulp.lpSum(is_work[i, n] for n in range(N)) <= total_number * N

# Solve the problem
problem.solve()

# Extract results
final_total_number = int(pulp.value(total_number))
final_is_work = [[int(pulp.value(is_work[i, n])) for n in range(N)] for i in range(final_total_number)]

# Prepare output in required format
output = {
    "total_number": final_total_number,
    "is_work": final_is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')