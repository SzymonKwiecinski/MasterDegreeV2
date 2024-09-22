import pulp

# Parse input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
required_staff = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(required_staff)

# Calculate the total cycle length
total_cycle_length = n_working_days + n_resting_days

# Create the problem instance
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Create variables for each starting day for each employee
x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(total_cycle_length)]

# Objective: Minimize the total number of employees
problem += pulp.lpSum(x)

# Constraints:
for day in range(N):
    sum_of_employees_working_on_day = 0
    for start_day in range(total_cycle_length):
        shift = (day - start_day) % total_cycle_length
        if 0 <= shift < n_working_days:
            sum_of_employees_working_on_day += x[start_day]
    problem += (sum_of_employees_working_on_day >= required_staff[day], f"Staff_requirement_day_{day}")

# Solve the problem
problem.solve()

# Gather the results
total_number = int(pulp.value(problem.objective))
is_work = []

for start_day in range(total_cycle_length):
    if x[start_day].varValue == 1:
        work_schedule = [0] * N
        for day in range(N):
            shift = (day - start_day) % total_cycle_length
            if 0 <= shift < n_working_days:
                work_schedule[day] = 1
        is_work.append(work_schedule)

# Prepare the output data
output_data = {
    "total_number": total_number,
    "is_work": is_work
}

print(output_data)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')