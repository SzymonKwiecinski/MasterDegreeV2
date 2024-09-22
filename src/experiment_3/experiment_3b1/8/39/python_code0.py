import pulp

# Data from JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)

# Create the problem
problem = pulp.LpProblem("Cafeteria_Employee_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable('x', lowBound=0, cat='Integer')  # Total number of employees
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # 100 is arbitrary for maximum employees

# Objective function
problem += x, "Minimize_Employees"

# Constraints for the required number of employees each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Employee_Requirement_Day_{n+1}"

# Constraints for working/resting schedule
for i in range(100):
    for j in range(N - n_working - n_resting + 1):
        # Working days
        for k in range(n_working):
            problem += is_work[j + k][i] == 1, f"Working_Days_Employee_{i+1}_Start_{j+1}"
        
        # Resting days
        for k in range(n_resting):
            problem += is_work[j + n_working + k][i] == 0, f"Resting_Days_Employee_{i+1}_After_Work_{j+1}"

# Solve the problem
problem.solve()

# Output the results
total_number = int(pulp.value(x))
print(f'Total number of employees hired: {total_number}')

is_work_matrix = [[int(is_work[n][i].value()) for i in range(100)] for n in range(N)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')