import pulp

# Parse the input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Extract parameters
num = data["num"]
n_working_days = data["n_working_days"]
n_resting_days = data["n_resting_days"]
N = len(num)

# Problem definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Variables
# binary variables indicate if employee i starts working on day n
x = pulp.LpVariable.dicts("x", ((i, n) for i in range(N) for n in range(N)), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum(x[i, n] for i in range(N) for n in range(N)), "Minimize total employees hired"

# Constraints
for n in range(N):
    problem += (
        pulp.lpSum(x[i, (n - d) % N] for i in range(N) for d in range(n_working_days)) >= num[n],
        f"Requirement_Day_{n+1}"
    )

# Solve the problem
problem.solve()

# Retrieve the results
total_number = int(pulp.value(problem.objective))
is_work = [[0] * N for _ in range(total_number)]

for i in range(total_number):
    for n in range(N):
        start_day = pulp.value(x[i, n])
        if start_day > 0.5:  # If the start day variable is effectively 1
            for d in range(n_working_days):
                is_work[i][(n + d) % N] = 1

# Output the results
output = {
    "total_number": total_number,
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')