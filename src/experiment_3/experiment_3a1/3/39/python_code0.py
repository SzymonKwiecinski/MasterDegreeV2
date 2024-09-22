import pulp

# Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

# Decision variable: total number of employees to hire
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

# Decision variables: is_work[n][i] for whether employee i works on day n
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Assuming a max of 100 employees

# Objective Function: Minimize total_number
problem += total_number

# Constraints to ensure enough staff each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n]

# Constraints for each employee's working/resting cycle
for i in range(100):
    for k in range((N // (n_working_days + n_resting_days)) + 1):  # Determine the maximum k
        for j in range(n_working_days):
            day_index = k * (n_working_days + n_resting_days) + j
            if day_index < N:
                problem += is_work[day_index][i] == 1

        for j in range(n_working_days, n_working_days + n_resting_days):
            day_index = k * (n_working_days + n_resting_days) + j
            if day_index < N:
                problem += is_work[day_index][i] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')