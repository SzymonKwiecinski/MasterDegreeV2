import pulp

# Data
supply = [30, 25, 45]
demand = [40, 60]
transmission_costs = [[14, 22], [18, 12], [10, 16]]

# Indices
P = len(supply)
C = len(demand)

# Problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision Variables
send_vars = pulp.LpVariable.dicts(
    "send",
    ((p, c) for p in range(P) for c in range(C)),
    lowBound=0,
    cat='Continuous'
)

# Objective
problem += pulp.lpSum(
    transmission_costs[p][c] * send_vars[(p, c)]
    for p in range(P)
    for c in range(C)
)

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(
        send_vars[(p, c)] for c in range(C)
    ) <= supply[p], f"Supply_Constraint_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(
        send_vars[(p, c)] for p in range(P)
    ) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')