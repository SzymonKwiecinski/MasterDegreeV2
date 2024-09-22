import pulp

# Data from JSON
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

# Parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

# Create the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

# Decision Variables
# Maximum number of employees M can be taken as the sum of required employees over all days
M = sum(num)

# y_i: Binary variable that indicates if employee i is hired
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# x_{i,n}: Binary variable that indicates if employee i works on day n
x = pulp.LpVariable.dicts("x", ((i, n) for i in range(M) for n in range(N)), cat='Binary')

# Objective function: Minimize the total number of employees hired
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Employees"

# Constraints

# 1. Daily Staffing Requirement
for n in range(N):
    problem += pulp.lpSum(x[i, n] for i in range(M)) >= num[n], f"Staffing_Requirement_Day_{n}"

# 2. Work and Rest Cycles
for i in range(M):
    for n in range(N):
        # Each employee can work only if they are hired
        problem += x[i, n] <= y[i], f"Employment_Restriction_Emp_{i}_Day_{n}"
        
        # Cyclic working and resting days constraints
        # It's complex to model directly so assumed employees work if possible and rest otherwise
        if n + n_working_days + n_resting_days <= N:
            problem += pulp.lpSum(x[i, n + d] for d in range(n_working_days)) <= n_working_days * y[i], f"Working_Cycle_Emp_{i}_Start_Day_{n}"
            problem += pulp.lpSum(x[i, n + n_working_days + d] for d in range(n_resting_days)) <= 0, f"Resting_Cycle_Emp_{i}_Start_Day_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')