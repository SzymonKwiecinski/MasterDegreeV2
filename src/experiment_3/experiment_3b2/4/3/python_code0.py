import pulp
import json

# Data input
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, T + 1), lowBound=0)
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, T + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(coal_cost * x_coal[t] + nuke_cost * x_nuke[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    # Demand Satisfaction Constraint
    problem += (oil_capacity[t - 1] + 
                 pulp.lpSum(x_coal[i] for i in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(x_nuke[i] for i in range(max(1, t - nuke_life + 1), t + 1)) >= demand[t - 1], 
                 f"Demand_Constraint_{t}")

    # Nuclear Capacity Limit
    problem += (pulp.lpSum(x_nuke[i] for i in range(max(1, t - nuke_life + 1), t + 1)) <= 
                 (max_nuke / 100) * (oil_capacity[t - 1] + 
                 pulp.lpSum(x_coal[i] for i in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(x_nuke[i] for i in range(max(1, t - nuke_life + 1), t + 1))),
                 f"Nuclear_Capacity_Constraint_{t}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')