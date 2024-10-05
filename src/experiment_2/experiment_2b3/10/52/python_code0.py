import pulp

# Parsing the data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)  # number of power plants
C = len(demand)  # number of cities

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(send[(p, c)] * transmission_costs[p][c] for p in range(P) for c in range(C))
problem += total_cost

# Constraints
# Each power plant should not exceed its supply capacity
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_Plant_{p}"

# Each city demand must be met
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_City_{c}"

# Solve the problem
problem.solve()

# Prepare the output
send_data = [[pulp.value(send[(p, c)]) for c in range(C)] for p in range(P)]
total_cost_value = pulp.value(problem.objective)

result = {
    "send": send_data,
    "total_cost": total_cost_value
}
print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')