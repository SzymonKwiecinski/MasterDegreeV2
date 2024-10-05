import pulp

# Data provided in the problem
data = {
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    "strength": [2000, 1500, 1000], 
    "lessonewaste": [0.25, 0.2, 0.1], 
    "moreonewaste": [0.1, 0.05, 0.05], 
    "recruit": [500, 800, 500], 
    "costredundancy": [200, 500, 500], 
    "num_overman": 150, 
    "costoverman": [1500, 2000, 3000], 
    "num_shortwork": 50, 
    "costshort": [500, 400, 400]
}

# Extracting data
requirement = data["requirement"]
strength = data["strength"]
lessonewaste = data["lessonewaste"]
moreonewaste = data["moreonewaste"]
recruit_max = data["recruit"]
costredundancy = data["costredundancy"]
num_overman = data["num_overman"]
costoverman = data["costoverman"]
num_shortwork = data["num_shortwork"]
costshort = data["costshort"]

K = len(requirement)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Defining the problem
problem = pulp.LpProblem('Minimize_Costs', pulp.LpMinimize)

# Decision variables
recruit_vars = [[pulp.LpVariable(f'recruit_{k}_{i}', 0, recruit_max[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning_vars = [[pulp.LpVariable(f'overmanning_{k}_{i}', 0, num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short_vars = [[pulp.LpVariable(f'short_{k}_{i}', 0, num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function: Minimizing total costs
cost_terms = []
for k in range(K):
    for i in range(I):
        # Initial manpower for the first year
        if i == 0:
            manpower = strength[k]
        else:
            manpower = (1 - lessonewaste[k]) * recruit_vars[k][i - 1] + (1 - moreonewaste[k]) * strength[k]

        # Calculating costs in the objective function
        redundancy_cost = costredundancy[k] * pulp.lpSum([manpower - requirement[k][i]])
        overmanning_cost = costoverman[k] * overmanning_vars[k][i]
        shortworking_cost = costshort[k] * short_vars[k][i]

        cost_terms.append(redundancy_cost + overmanning_cost + shortworking_cost)

# Add to the objective
problem += pulp.lpSum(cost_terms)

# Constraints
for k in range(K):
    for i in range(I):
        manpower = (strength[k] if i == 0 else 
                     (1 - lessonewaste[k]) * recruit_vars[k][i - 1] + 
                     (1 - moreonewaste[k]) * manpower)

        problem += (
            recruit_vars[k][i] + (manpower + overmanning_vars[k][i] + short_vars[k][i] / 2) >= requirement[k][i],
            f'Manpower_requirement_{k}_{i}'
        )

# Solve the problem
problem.solve()

# Output the optimized values
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')