import pulp

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
N = len(data['num'])
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Create the Linear Programming problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

# Define the total number of employees (to be determined)
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

# Define the binary decision variables
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), 
                                             cat='Binary')

# Objective function: Minimize the total number of employees
problem += total_number, "Total_Employees"

# Constraints for staff requirement each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_n[n], f"Staff_requirement_day_{n}"

# Work-rest cycle constraints for each employee
for i in range(total_number):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[(n + j, i)] for j in range(n_working_days)) == n_working_days, f"Work_cycle_{n}_{i}"

    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(is_work[(n + n_working_days + j, i)] for j in range(n_resting_days)) == 0, f"Rest_cycle_{n}_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')