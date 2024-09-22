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
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number)), cat='Binary')

# Constraints
for n in range(N):
    for i in range(total_number):
        for d in range(n_working_days):
            if n + d < N:  # Ensure within bounds
                problem += is_work[n][i] <= sum(is_work[n + d - wd][j] for wd in range(n_working_days) for j in range(total_number))

# Objective Function
problem += total_number

# Solve the problem
problem.solve()

# Prepare output
output = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(is_work[n][i].varValue) for n in range(N)] for i in range(int(pulp.value(total_number)))]
}

print(json.dumps(output, indent=4))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')