import pulp

# Problem data based on given JSON
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

# Extracting data values
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create a Linear Programming Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision variable for the total number of employees
T = pulp.LpVariable('T', lowBound=0, cat='Integer')

# Decision variables for employees working on a particular day
x = pulp.LpVariable.dicts("x", ((n, i) for n in range(N) for i in range(100)), cat='Binary')

# Objective: Minimize the total number of employees
problem += T

# Constraints: Ensure enough employees are working per day
for n in range(N):
    problem += pulp.lpSum(x[n, i] for i in range(100)) >= num[n]

# Constraints: Working and resting schedule
for i in range(100):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(x[n + k, i] for k in range(n_working_days)) <= n_working_days

    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(x[n + n_working_days + k, i] for k in range(n_resting_days)) == 0

# Linking T with the actual number of employees required
for i in range(100):
    problem += pulp.lpSum(x[n, i] for n in range(N)) <= T * N  # To limit by T

# Solve the problem
problem.solve()

# Gathering output
total_number = int(pulp.value(T))
is_work = [[int(pulp.value(x[n, i])) for i in range(total_number)] for n in range(N)]

# Printing the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("{")
print(f"  total_number: {total_number},")
print(f"  is_work: {is_work}")
print("}")