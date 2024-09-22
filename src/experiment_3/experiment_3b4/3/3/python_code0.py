import pulp

# Define data
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

T = data['T']
Demand = data['Demand']
OilCap = data['OilCap']
CoalCost = data['CoalCost']
NukeCost = data['NukeCost']
MaxNuke = data['MaxNuke']
CoalLife = data['CoalLife']
NukeLife = data['NukeLife']

# Initialize problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_add = [pulp.LpVariable(f"coal_add_{t}", lowBound=0, cat='Continuous') for t in range(T)]
nuke_add = [pulp.LpVariable(f"nuke_add_{t}", lowBound=0, cat='Continuous') for t in range(T)]

# Objective Function
Z = pulp.lpSum([CoalCost * coal_add[t] + NukeCost * nuke_add[t] for t in range(T)])
problem += Z

# Constraints
for t in range(T):
    # Demand Satisfaction Constraint
    problem += (
        OilCap[t] + 
        sum(coal_add[i] for i in range(max(0, t - CoalLife + 1), t + 1)) + 
        sum(nuke_add[j] for j in range(max(0, t - NukeLife + 1), t + 1)) 
        >= Demand[t]
    )
    
    # Nuclear Capacity Constraint
    problem += (
        sum(nuke_add[j] for j in range(max(0, t - NukeLife + 1), t + 1)) 
        <= MaxNuke / 100 * (
            OilCap[t] + 
            sum(coal_add[i] for i in range(max(0, t - CoalLife + 1), t + 1)) + 
            sum(nuke_add[j] for j in range(max(0, t - NukeLife + 1), t + 1))
        )
    )

# Solve problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')