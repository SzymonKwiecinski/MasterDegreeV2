import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

supply = data['supply']          # Supply capacities of power plants
demand = data['demand']          # Demand requirements of cities
transmission_costs = data['transmission_costs']  # Transmission cost matrix

# Create the LP problem
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)  # Amount sent from power plant p to city c

# Objective function: Minimize total transmission costs
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Prepare output
result_send = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": result_send,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')