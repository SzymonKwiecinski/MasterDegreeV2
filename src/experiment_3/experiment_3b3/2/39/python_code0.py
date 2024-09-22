import pulp

# Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

# Parameters
N = len(data['num'])  # Total number of days
num_n = data['num']  # Number of employees required each day
n_working_days = data['n_working_days'] 
n_resting_days = data['n_resting_days'] 
T = n_working_days + n_resting_days  # Total cycle length

# Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts(
    'is_work', 
    ((n, i) for n in range(N) for i in range(100)), 
    cat='Binary'
)

# Objective Function
problem += total_number, "Minimize Total Number of Employees"

# Constraints
for n in range(N):
    problem += (
        pulp.lpSum(is_work[(n, i)] for i in range(100)) >= num_n[n],
        f"Minimum_Workers_Day_{n}"
    )

# Initial constraints setup in cycles
for i in range(100):
    for k in range((N + T - 1) // T):  # Ensuring all days are covered
        for day in range(n_working_days):
            if k * T + day < N:
                problem += (
                    is_work[(k * T + day, i)] == 1,
                    f"Work_Employee_{i}_Day_{k * T + day}"
                )
        for day in range(n_working_days, T):
            if k * T + day < N:
                problem += (
                    is_work[(k * T + day, i)] == 0,
                    f"Rest_Employee_{i}_Day_{k * T + day}"
                )

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')