import pulp

# Data from JSON
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

# Parameters
T = data['T']
demand = data['Demand']
oil = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Capacity Expansion Problem", pulp.LpMinimize)

# Decision Variables
x_coal = [pulp.LpVariable(f"x_coal_{t}", lowBound=0, cat='Continuous') for t in range(T)]
x_nuke = [pulp.LpVariable(f"x_nuke_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective Function
problem += pulp.lpSum(coal_cost * x_coal[t] + nuke_cost * x_nuke[t] for t in range(T))

# Constraints

# Demand Satisfaction
for t in range(T):
    coal_capacity = pulp.lpSum(x_coal[k] for k in range(max(0, t - coal_life + 1), t + 1))
    nuke_capacity = pulp.lpSum(x_nuke[k] for k in range(max(0, t - nuke_life + 1), t + 1))
    problem += coal_capacity + nuke_capacity + oil[t] >= demand[t]

# Nuclear Capacity Limit
for t in range(T):
    nuke_capacity_sum = pulp.lpSum(x_nuke[k] for k in range(max(0, t - nuke_life + 1), t + 1))
    total_capacity = pulp.lpSum(x_coal[k] for k in range(max(0, t - coal_life + 1), t + 1))
    total_capacity += nuke_capacity_sum + oil[t]
    
    if total_capacity != 0:  # Avoid division by zero
        problem += nuke_capacity_sum <= max_nuke / 100 * total_capacity

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')