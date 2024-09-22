import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
N = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

# Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Define variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')  # Number of employees

# Create work schedule variables
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(1, total_number+1)), cat='Binary')

# Objective function: minimize total_number
problem += total_number

# Constraints to ensure the required staff is met
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(1, total_number+1) 
                          if (i-1) % (n_working_days + n_resting_days) < n_working_days) >= data['num'][n]

# Solve the problem
problem.solve()

# Prepare the output
result_is_work = [[int(is_work[n][i].value()) for n in range(N)] for i in range(1, int(total_number.value()) + 1)]

output = {
    "total_number": int(total_number.value()),
    "is_work": result_is_work
}

# Print the objective value and the output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output, indent=4))