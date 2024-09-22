import pulp

# Given data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

N = len(data['num'])  # Total number of days
num_n = data['num']  # Number of employees required each day
n_working = data['n_working_days']  # Number of consecutive working days
n_resting = data['n_resting_days']  # Number of consecutive resting days
T = n_working + n_resting  # Total cycle length

# Create the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable("total_employees", lowBound=0, cat='Integer')  # Total number of employees hired
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Assume a max of 100 employees

# Objective Function
problem += x, "Minimize total number of employees"

# Constraints - Staffing requirements
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Staffing_requirement_day_{n+1}"

# Employee working pattern constraints
for i in range(100):
    for k in range((N // T) + 1):  # Calculate how many full cycles fit in N
        for w in range(n_working):
            if k * T + w < N:
                problem += is_work[k * T + w][i] == 1, f"Employee_{i+1}_working_day_{k*T+w+1}"
        for r in range(n_resting):
            if k * T + n_working + r < N:
                problem += is_work[k * T + n_working + r][i] == 0, f"Employee_{i+1}_resting_day_{k*T+n_working+r+1}"

# Solve the problem
problem.solve()

# Output
total_number = int(pulp.value(x))
is_work_matrix = [[int(is_work[n][i].varValue) for i in range(total_number)] for n in range(N)]

print(f'Total number of employees to hire: {total_number}')
print('Working status matrix (days x employees):')
for row in is_work_matrix:
    print(row)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')