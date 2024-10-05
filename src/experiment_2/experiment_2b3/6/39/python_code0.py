import pulp

# Data from the problem
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Problem parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Initialize the linear programming problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

# Decision Variables
# Binary variables indicating if employee i starts working on day n
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(x[n][i] for n in range(N) for i in range(N)), "Total_Employees"

# Constraints
# Ensure enough employees are working each day
for n in range(N):
    problem += (pulp.lpSum(x[i][((n-i) % N)] for i in range(N) if i <= n or i >= n-N+n_working_days) >= num[n]), f"Demand_Constraint_day_{n+1}"

# Solve the problem
problem.solve()

# Extract the total number of employees required
total_number = sum(pulp.value(x[n][i]) for n in range(N) for i in range(N))

# Extract working schedule
is_work = [[int(i == pulp.value(x[i][(n-i) % N])) for n in range(N)] for i in range(N)]

# Output the results in the specified format
output = {
    "total_number": int(total_number),
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')