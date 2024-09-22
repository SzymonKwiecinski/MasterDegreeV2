import pulp

# Data from the JSON input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num_days = len(data['num'])
I = 10  # Assume a maximum of 10 employees for the model

# Create the linear programming problem
problem = pulp.LpProblem("Employee_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(I), cat='Binary')  # Employee hired
y = pulp.LpVariable.dicts("y", (range(num_days), range(I)), cat='Binary')  # Employee working on day n

# Objective Function: Minimize the total number of employees hired
problem += pulp.lpSum(x[i] for i in range(I)), "Minimize_Employees"

# Constraints

# Employee requirement per day
for n in range(num_days):
    problem += pulp.lpSum(y[n][i] for i in range(I)) >= data['num'][n], f"Employee_Requirement_Day_{n}"

# Employee working days
for n in range(num_days):
    for i in range(I):
        problem += y[n][i] <= x[i], f"Working_Days_Employee_{i}_Day_{n}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')