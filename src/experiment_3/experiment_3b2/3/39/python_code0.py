import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
N = len(data['num'])
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Problem definition
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("employee", range(N), cat='Binary')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(x[i] for i in range(N)), "TotalEmployees"

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(N)) >= num[n], f"StaffingRequirement_day_{n+1}"

for i in range(N):
    for k in range((N + n_working_days + n_resting_days - 1) // (n_working_days + n_resting_days)):
        for j in range(n_working_days):
            day_index = k * (n_working_days + n_resting_days) + j
            if day_index < N:
                problem += is_work[day_index][i] <= x[i], f"WorkConstraint_day_{day_index+1}_employee_{i+1}"
        
        for j in range(n_resting_days):
            day_index = k * (n_working_days + n_resting_days) + n_working_days + j
            if day_index < N:
                problem += is_work[day_index][i] == 0, f"RestConstraint_day_{day_index+1}_employee_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')