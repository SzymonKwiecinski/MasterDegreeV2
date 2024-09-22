import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

# Initialize the problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

# Objective Function
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_n[n]

# Adding constraints for working and resting days
for i in range(total_number):
    for k in range(N):
        if k + n_working_days <= N:  # Ensure we don't go out of bounds
            for j in range(n_working_days):
                problem += is_work[(k + j, i)] == 1
            for j in range(n_resting_days):
                if k + n_working_days + j < N:  # Ensure we don't go out of bounds
                    problem += is_work[(k + n_working_days + j, i)] == 0

# Solve the problem
problem.solve()

# Output the results
print(f'Total Employees Required: {total_number.varValue}')
schedule = [[is_work[(n, i)].value() for i in range(int(total_number.varValue))] for n in range(N)]
print(f'Work Schedule: {schedule}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')