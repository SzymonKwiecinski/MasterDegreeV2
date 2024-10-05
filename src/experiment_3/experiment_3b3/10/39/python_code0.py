import pulp

# Data provided
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
n_days = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
d_c = n_working_days + n_resting_days

# Problem Definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

# Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
# Binary Decision Variables for each day and each employee
x = pulp.LpVariable.dicts("x", ((n, i) for n in range(n_days) for i in range(100)),
                          cat='Binary')

# Objective Function
problem += total_number, "Minimize Total Number of Employees"

# Constraints
for n in range(n_days):
    problem += (pulp.lpSum(x[n, i] for i in range(100)) >= data['num'][n], 
                f"NumEmployees_day{n+1}")

# Setting up cycle constraints
for n in range(n_days):
    for i in range(100):
        if n + n_working_days <= n_days:
            problem += (pulp.lpSum(x[n + k, i] for k in range(n_working_days)) == n_working_days,
                        f"WorkCycle_start{n+1}_emp{i+1}")
        
        if n + d_c <= n_days:
            problem += (pulp.lpSum(x[n + n_working_days + k, i] for k in range(n_resting_days)) == 0,
                        f"RestCycle_start{n+1}_emp{i+1}")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')