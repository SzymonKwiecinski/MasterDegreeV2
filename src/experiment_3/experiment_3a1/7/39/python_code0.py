import pulp

# Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)
T = n_working + n_resting

# Create the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number)), cat='Binary')

# Objective Function: Minimize the total number of employees hired
problem += total_number, "Minimize_Employees"

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num_n[n], f"Requirement_Day_{n+1}"

for i in range(total_number):
    for n in range(N):
        if n % T < n_working:
            problem += is_work[n][i] == 1, f"Working_Employee_{i+1}_Day_{n+1}"
        else:
            problem += is_work[n][i] == 0, f"Resting_Employee_{i+1}_Day_{n+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')