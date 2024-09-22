import pulp
import json

# Load the data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)
total_number = len(num)  # One employee per day for simplicity

T = n_working_days + n_resting_days

# Create the problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("work", (range(total_number), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum([1 for i in range(total_number)])

# Constraints for required staff per day
for n in range(N):
    problem += pulp.lpSum([x[i][n] for i in range(total_number)]) >= num[n], f"StaffRequirement_day_{n+1}"

# Constraints for employee work/rest cycles
for i in range(total_number):
    for k in range((N // T) + 1):  # Integer k for T cycles
        # Working days
        for n in range(k * T + 1, k * T + n_working_days + 1):
            if n < N:  # Ensure n does not exceed the number of days
                problem += x[i][n] == 1
        # Rest days
        for n in range(k * T + n_working_days + 1, (k + 1) * T + 1):
            if n < N:  # Ensure n does not exceed the number of days
                problem += x[i][n] == 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')