import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat=pulp.LpInteger)

# Objective Function
problem += pulp.lpSum(x[j] for j in range(T))

# Define IsWorking function
def is_working(j, i, period, T):
    # Check if nurse starting on day j is working on day i
    if (i >= j and i < j + period) or (j + period > T and i < (j + period) % T):
        return 1
    return 0

# Constraints
for i in range(T):
    problem += pulp.lpSum(x[j] * is_working(j, i, period, T) for j in range(T)) >= demand[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')