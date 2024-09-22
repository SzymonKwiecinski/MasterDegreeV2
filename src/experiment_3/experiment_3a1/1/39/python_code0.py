import pulp
import numpy as np

# Data from JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)  # Number of days

# Create the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

# Objective Function
problem += total_number, "Minimize_Total_Employees"

# Constraints
# Ensure that the number of employees working meets the requirement for each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_n[n], f"Minimum_Employees_Day_{n}"

# Define the working and resting schedule for each employee
for i in range(total_number):
    for n in range(N):
        if n - (n_working_days + n_resting_days) >= 0:  # Check for bounds
            problem += is_work[(n, i)] <= pulp.lpSum(is_work[(n - j, i)] for j in range(n_working_days + n_resting_days)), f"Work_Rest_Schedule_{i}_{n}"

# Solve the problem
problem.solve()

# Output
total_employees = pulp.value(total_number)
is_work_matrix = np.array([[pulp.value(is_work[(n, i)]) for i in range(int(total_employees))] for n in range(N)])

print(f'Total Employees Hired: {total_employees}')
print('Work Schedule Matrix:')
print(is_work_matrix)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')