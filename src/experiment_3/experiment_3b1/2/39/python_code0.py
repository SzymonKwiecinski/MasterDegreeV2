import pulp

# Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

N = len(data['num'])  # Total number of days
num_n = data['num']  # Employees required on each day
n_working_days = data['n_working_days']  # Consecutive working days
n_resting_days = data['n_resting_days']  # Consecutive resting days
T = n_working_days + n_resting_days  # Total cycle length

# Problem Definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')  # Total employees
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Assume a maximum of 100 employees for initial setup

# Objective Function
problem += total_number, "Minimize_Total_Employees"

# Constraints for minimum employees required
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Req_Employees_Day_{n+1}"

# Constraints for working/resting schedule
for i in range(100):  # For each employee
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[n+k][i] for k in range(n_working_days)) == n_working_days, f"Working_Days_Employee_{i}_Start_{n+1}"
    
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(is_work[n + n_working_days + k][i] for k in range(n_resting_days)) == 0, f"Resting_Days_Employee_{i}_Start_{n+1}"

# Calculate the total number of employees used
for i in range(100):
    problem += pulp.lpSum(is_work[n][i] for n in range(N)) <= total_number

# Solve the problem
problem.solve()

# Output
print(f'Total Employees Hired: {pulp.value(problem.objective)}')
for n in range(N):
    for i in range(100):
        if pulp.value(is_work[n][i]) == 1:
            print(f'Employee {i} works on day {n+1}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')