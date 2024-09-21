import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Demand = data['Demand']

# Problem Definition
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision Variable
N = pulp.LpVariable('N', lowBound=0, cat='Continuous')

# Objective Function
problem += N, "Minimize the number of nurses hired"

# Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_{t+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')