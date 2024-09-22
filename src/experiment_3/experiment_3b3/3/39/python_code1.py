import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num_days = len(data['num'])
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
T = n_working_days + n_resting_days

# Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable('x', lowBound=0, cat='Integer')  # Total number of employees to hire

# is_work binary variables
is_work = {(n, i): pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for n in range(num_days) for i in range(num_days)}

# Objective Function
problem += x

# Constraints
for n in range(num_days):
    problem += (pulp.lpSum(is_work[n, i] for i in range(num_days)) >= num_n[n]), f"Demand_Day_{n}"

# Enforce working and resting pattern
for i in range(num_days):
    for n in range(0, num_days, T):
        if n + n_working_days - 1 < num_days:
            problem += (pulp.lpSum(is_work[n + k, i] for k in range(n_working_days)) == n_working_days), f"Work_Pattern_{i}_{n}"
            
        if n + n_working_days + n_resting_days - 1 < num_days:
            problem += (pulp.lpSum(is_work[n + n_working_days + k, i] for k in range(n_resting_days)) == 0), f"Rest_Pattern_{i}_{n}"

# Solve the problem
problem.solve()

# Print Objective Value