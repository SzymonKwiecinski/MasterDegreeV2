import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Define the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat=pulp.LpInteger)
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(100)), cat=pulp.LpBinary)

# Objective Function
problem += total_number

# Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(100)) >= num[n]

for i in range(100):
    for n in range(N):
        if n % (n_working_days + n_resting_days) < n_working_days:
            problem += is_work[n, i] == 1
        else:
            problem += is_work[n, i] == 0

problem += total_number >= pulp.lpSum(is_work[n, i] for n in range(N) for i in range(100)) / N

# Solve the LP problem
problem.solve()

# Output Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')