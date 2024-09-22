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
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number)), cat='Binary')

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num[n]

for i in range(total_number):
    for n in range(N):
        for k in range(n_working_days):
            day = (n + k) % N
            problem += is_work[n][i] <= (1 if k < n_working_days else 0)
            
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