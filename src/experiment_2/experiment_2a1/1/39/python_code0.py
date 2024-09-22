import pulp
import json

# Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Extracting the values from the data
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Initialize the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Define variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts('is_work', [(n, i) for n in range(N) for i in range(total_number)], 
                                             cat='Binary')

# Objective Function: Minimize the total number of employees needed
problem += total_number

# Constraints
for n in range(N):
    for i in range(n_working_days):
        problem += pulp.lpSum(is_work[(day, employee) for day in range(max(0, n - n_working_days + 1), n + 1) 
                                       for employee in range(total_number) if (n - day < n_working_days)]) >= num[n]

# Solve the problem
problem.solve()

# Prepare output
output = {
    'total_number': int(pulp.value(total_number)),
    'is_work': [[int(is_work[(n, i)].varValue) for n in range(N)] for i in range(int(pulp.value(total_number)))]
}

# Display the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')