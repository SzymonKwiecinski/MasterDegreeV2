import pulp
import json

# Data provided in the JSON format
data_json = '''{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}'''
data = json.loads(data_json.replace("'", "\""))

# Extracting data from the parsed JSON
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

# Create the LP problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Decision variable: is_work[n][i]
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

# Objective function: Minimize total_number
problem += total_number, "Minimize_Total_Employees"

# Constraints for daily staff requirements
for n in range(N):
    problem += pulp.lpSum([is_work[(n, i)] for i in range(total_number)]) >= num_n[n], f"Daily_Staff_Requirement_{n}"

# Enforce work and rest schedule constraints
for i in range(total_number):
    for n in range(N - (n_working_days + n_resting_days) + 1):
        problem += pulp.lpSum([is_work[(d, i)] for d in range(n, n + n_working_days)]) <= n_working_days, f"Working_Days_Constraint_{i}_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')