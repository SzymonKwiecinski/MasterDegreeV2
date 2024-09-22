import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the problem
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Define variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

# Objective function: Minimize the number of employees
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number) if i < total_number) >= num[n]
    
for i in range(total_number):
    for n in range(N):
        for d in range(n_working_days):
            if n + d < N:
                problem += is_work[(n + d, i)] <= 1  # An employee can work only one shift per day

# Solve the problem
problem.solve()

# Get results
result_total_number = int(pulp.value(total_number))
result_is_work = [[int(is_work[(n, i)].varValue) for n in range(N)] for i in range(result_total_number)]

# Output results
output_data = {
    "total_number": result_total_number,
    "is_work": result_is_work
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')