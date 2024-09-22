import json
import pulp

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')  # Total number of employees

# Using a variable for total_number to create is_work variables correctly
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # 100 is a large upper limit for employees

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n]  # At least 'num[n]' employees should work on day 'n'

# Ensure that the working pattern of each employee is respected
for i in range(100):  # Assuming a maximum of 100 employees
    for d in range(N):
        for wd in range(n_working_days):
            if d + wd < N:
                problem += is_work[d + wd][i] <= 1  # Employee i can work on day d+wd

# Objective Function
problem += total_number

# Solve the problem
problem.solve()

# Prepare output
output = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(is_work[n][i].varValue) for n in range(N)] for i in range(100) if int(is_work[0][i].varValue) > 0]
}

print(json.dumps(output, indent=4))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')