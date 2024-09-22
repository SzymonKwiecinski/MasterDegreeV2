import pulp

# Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

N = len(data['num'])
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Define the problem
problem = pulp.LpProblem("Cafeteria Staffing Problem", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(1, 100)), cat='Binary')  # Assuming a max of 100 employees for simplicity

# Objective Function
problem += total_number, "Minimize number of employees hired"

# Constraints for the number of employees working each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(1, 100)) >= num_n[n], f"Day_{n+1}_employees_requirement"

# Constraints for the working/resting cycles of employees
for i in range(1, 100):
    for k in range(N):
        if k < (n_working_days + n_resting_days):
            if k < n_working_days:
                problem += is_work[(k, i)] == 1, f"Employee_{i}_works_day_{k}"
            else:
                problem += is_work[(k, i)] == 0, f"Employee_{i}_rests_day_{k}"
        else:
            problem += is_work[(k, i)] == (
                pulp.lpSum(is_work[(k - j, i)] for j in range(n_working_days)) >= n_working_days
            ), f"Employee_{i}_cycle_day_{k}"

# Total number of employees is the sum of all employed variables
problem += total_number == pulp.lpSum(is_work[(n, i)] for n in range(N) for i in range(1, 100)), "Total number of employees"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')