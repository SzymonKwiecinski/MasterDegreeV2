import pulp

# Data from JSON
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

# Problem parameters
N = len(data['num'])  # Total number of days

# Create the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(1000)),
                                cat='Binary')

# Objective function
problem += total_number, "Minimize_total_number_of_employees"

# Constraints
# (1) Sufficient employees each day
for n in range(N):
    problem += (
        pulp.lpSum(is_work[n, i] for i in range(1000)) >= data['num'][n], 
        f"Constraint_sufficient_employees_day_{n+1}"
    )

# (2) Working and (3) Resting days constraints
for i in range(1000):
    for j in range(N):
        # Enforce working days
        if j + data['n_working_days'] <= N:
            problem += (
                pulp.lpSum(is_work[j + k, i] for k in range(data['n_working_days'])) 
                - data['n_working_days'] * is_work[j, i] == 0, 
                f"Constraint_working_days_emp_{i}_from_day_{j+1}"
            )
        
        # Enforce resting days
        if j + data['n_working_days'] + data['n_resting_days'] <= N:
            problem += (
                pulp.lpSum(is_work[j + data['n_working_days'] + k, i] for k in range(data['n_resting_days']))
                <= data['n_resting_days'] * (1 - is_work[j, i]), 
                f"Constraint_resting_days_emp_{i}_from_day_{j+1}"
            )

# Solve the problem
problem.solve()

# Output results
total_employees_needed = sum(
    pulp.value(is_work[0, i]) for i in range(1000)
)

# Print the total number of employees needed and objective value
print(f"Total Number of Employees Hired: {total_employees_needed}")
print(f"Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>")