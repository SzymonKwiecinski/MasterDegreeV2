import pulp
import json

# Load data from JSON format
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)
T = n_working + n_resting

# Create the problem
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

# Decision variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number)), cat='Binary')

# Objective function
problem += total_number, "Minimize_Total_Employees"

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num_n[n], f"Min_Employees_on_day_{n}"

for i in range(total_number):
    for n in range(N):
        if (n % T) < n_working:
            problem += is_work[n][i] == 1, f"Employee_{i}_works_on_day_{n}"
        else:
            problem += is_work[n][i] == 0, f"Employee_{i}_rests_on_day_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')