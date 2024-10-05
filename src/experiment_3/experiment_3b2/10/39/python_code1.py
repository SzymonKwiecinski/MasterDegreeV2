import pulp

# Input Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

# Create the problem
problem = pulp.LpProblem("Minimum_Employee_Hiring_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', range(N), cat='Binary')  # Employee hired
y = pulp.LpVariable.dicts('y', (range(N), range(N)), cat='Binary')  # Employee working on day

# Objective Function
problem += pulp.lpSum(x[i] for i in range(N)), "Minimize_Hired_Employees"

# Constraints
# Daily Staffing Requirement
for n in range(N):
    problem += pulp.lpSum(y[n][i] for i in range(N)) >= num_n[n], f"Staffing_Requirement_{n}"

# Employee Work Cycle Constraints
for i in range(N):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(y[n + j][i] for j in range(n_working_days)) == n_working_days * x[i], f"Work_Cycle_{i}_{n}"
    
    for n in range(N - n_working_days): 
        problem += pulp.lpSum(y[n + n_working_days + j][i] for j in range(n_resting_days) if n + n_working_days + j < N) == 0, f"Rest_Cycle_{i}_{n}"

# Solve the problem
problem.solve()

# Outputs
total_number = pulp.value(problem.objective)
is_work = {(n, i): pulp.value(y[n][i]) for n in range(N) for i in range(N)}

print(f' (Objective Value): <OBJ>{total_number}</OBJ>')