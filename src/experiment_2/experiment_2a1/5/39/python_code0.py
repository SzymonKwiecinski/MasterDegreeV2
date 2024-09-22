import json
import pulp

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variable: number of employees to hire
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

# Decision variables for each employee and each day
is_work = [[pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for i in range(int(total_number) + 1)] for n in range(N)]

# Objective function: minimize the total number of employees
problem += total_number, "Minimize_Employees"

# Constraints to ensure required staff is met
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(int(total_number))) >= num[n], f"Staff_Requirement_Day_{n+1}"

# Constraints to enforce working and resting days
for i in range(int(total_number)):
    for n in range(N):
        working_days = [is_work[(n + d) % N][i] for d in range(n_working_days)]
        resting_days = [is_work[(n + d) % N][i] for d in range(n_working_days, n_working_days + n_resting_days)]
        problem += pulp.lpSum(working_days) <= n_working_days, f"Employee_{i+1}_Working_Days_{n+1}"
        problem += pulp.lpSum(resting_days) == 0, f"Employee_{i+1}_Resting_Days_{n+1}"

# Solve the problem
problem.solve()

# Prepare output
result = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(is_work[n][i].value()) for n in range(N)] for i in range(int(pulp.value(total_number)))]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')