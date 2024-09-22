import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

N = len(num)
total_days = N

# Define the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variable for total number of employees
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')

# Decision variables for whether an employee works on day n
is_work = pulp.LpVariable.dicts("is_work", (range(total_days), range(100)), cat='Binary')

# Objective Function
problem += total_number

# Constraints
for n in range(total_days):
    problem += pulp.lpSum(is_work[n][i] 
                          for i in range(total_number) 
                          if (i // (n_working_days + n_resting_days)) * (n_working_days + n_resting_days) <= n) >= num[n]

# Additional constraint to relate total_number with the number of employed variables
problem += pulp.lpSum([is_work[n][i] for n in range(total_days) for i in range(100)]) <= total_number

# Solve the problem
problem.solve()

# Output result
actual_total_number = int(pulp.value(total_number))
result = {
    "total_number": actual_total_number,
    "is_work": [[int(pulp.value(is_work[n][i])) for i in range(actual_total_number)] for n in range(total_days)]
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')