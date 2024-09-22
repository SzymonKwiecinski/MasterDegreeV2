import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Parameters
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)
C = len(demand)

# Problem
problem = pulp.LpProblem("Electricity_Transmission_Problem", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send",
                             ((p, c) for p in range(P) for c in range(C)),
                             lowBound=0,
                             cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Demand satisfaction for each city
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_City_{c}"

# Supply capacity constraint for each power plant
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_Plant_{p}"

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')