import pulp
import json

# Extract data from JSON format
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

# Create the linear programming problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

# Decision variable: total number of employees
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

# Decision variable: is_work[n][i]
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')

# Objective function
problem += total_number

# Constraints for the number of employees needed each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n]

# Constraints for each employee's working and resting schedule
for i in range(100):
    for n in range(N - n_working_days - n_resting_days + 1):
        # Working days constraint
        problem += pulp.lpSum(is_work[j][i] for j in range(n, n + n_working_days)) == n_working_days
        # Resting days constraint
        problem += pulp.lpSum(is_work[j][i] for j in range(n + n_working_days, n + n_working_days + n_resting_days)) == 0
        
# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')