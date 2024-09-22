import pulp

# Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

# Problem Data
N = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
num_n = data['num']

# Create a problem instance
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')

is_work = pulp.LpVariable.dicts("is_work",
                                ((n, i) for n in range(N) for i in range(100)), # 100 is an arbitrary large number of potential employees
                                0, 1, cat='Binary')

# Objective Function
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(100)) >= num_n[n]

for i in range(100):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[n + j, i] for j in range(n_working_days)) <= n_working_days
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(is_work[n + n_working_days + j, i] for j in range(n_resting_days)) == 0

# Solve the problem
problem.solve()

# Print the result
print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optimal total number of employees
optimal_total_number = pulp.value(total_number)
print(f"Optimal Total Number of Employees: {optimal_total_number}")

# Schedule for each employee
for i in range(int(optimal_total_number)):
    schedule = [int(is_work[n, i].varValue) for n in range(N)]
    print(f'Employee {i+1} Schedule: {schedule}')