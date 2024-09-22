import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters extraction
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the LP problem
problem = pulp.LpProblem("Cafeteria_Employee_Scheduling", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')

# Constraints
for n in range(N):
    # Sum of employees working on day n should be >= num[n]
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num[n]

# Each employee works n_working_days then rests n_resting_days
for i in range(100):  # Assume a maximum of 100 employees for indexing
    for n in range(N):
        if n >= n_working_days:
            problem += is_work[n][i] + pulp.lpSum(is_work[j][i] for j in range(n - n_working_days, n)) <= 1
        else:
            problem += is_work[n][i] <= 1

# Objective Function
problem += total_number, "Total Number of Employees"

# Solve the problem
problem.solve()

# Prepare the output
total_number_value = pulp.value(total_number)
is_work_matrix = [[pulp.value(is_work[n][i]) for n in range(N)] for i in range(100) if pulp.value(is_work[0][i]) is not None]

# Output
output = {
    "total_number": total_number_value,
    "is_work": is_work_matrix
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')