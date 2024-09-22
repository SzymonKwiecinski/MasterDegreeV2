import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Extract data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the problem variable
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable("total_number", lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  # Assume a maximum of 100 employees for the sake of the variable creation

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n]  # Use 100 as a placeholder for the total_number

# Ensure each employee works for n_working_days and rests for n_resting_days
for i in range(100):  # Check assuming maximum of 100 employees
    for n in range(N):
        for k in range(n_working_days):
            day = (n + k) % N
            if day < N:
                problem += is_work[n][i] <= pulp.lpSum(is_work[(day + j) % N][i] for j in range(n_working_days))  # Limit working days

# Objective function
problem += total_number

# Solve the problem
problem.solve()

# Collecting the results
result = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(pulp.value(is_work[n][i])) for n in range(N)] for i in range(int(pulp.value(total_number)))]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')