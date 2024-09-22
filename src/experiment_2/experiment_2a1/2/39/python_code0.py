import pulp
import json

# Given data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Problem Definition
N = len(num)  # Number of days
total_days = N  # Total number of days we need to cover
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')  # Total number of employees to hire

# Create a problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision variables: whether employee i is working on day n
is_work = pulp.LpVariable.dicts("is_work", (range(total_days), range(total_number)), cat='Binary')

# Objective Function
problem += total_number, "Minimize_Employees"

# Constraints: Ensure sufficient staff for each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num[n], f"Staff_requirement_day_{n}"

# Constraints: Employee working structure
for i in range(total_number):
    for n in range(total_days):
        for k in range(n_working_days):
            if n + k < total_days:
                problem += is_work[n + k][i] == 1  # Employee works for n_working_days
        for k in range(n_resting_days):
            if n + n_working_days + k < total_days:
                problem += is_work[n + n_working_days + k][i] == 0  # Employee rests for n_resting_days

# Solve the problem
problem.solve()

# Collecting results
total_employees = int(pulp.value(total_number))
is_work_schedule = [[int(pulp.value(is_work[n][i])) for n in range(total_days)] for i in range(total_employees)]

# Output results
output = {
    "total_number": total_employees,
    "is_work": is_work_schedule
}

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print output
print(json.dumps(output))