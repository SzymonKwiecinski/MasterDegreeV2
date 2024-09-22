import pulp

# Parse the input data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_max = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(requirement)  # number of manpower categories
I = len(requirement[0])  # number of years

# Define the LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Define decision variables
recruit = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=recruit_max[k], cat='Integer') for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=num_overman, cat='Integer') for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=num_shortwork, cat='Integer') for i in range(I)] for k in range(K)]
redundancy = [[pulp.LpVariable(f"redundancy_{k}_{i}", lowBound=0, cat='Integer') for i in range(I)] for k in range(K)]

# Objective function: Minimize the total cost
cost = pulp.lpSum(costredundancy[k] * redundancy[k][i] +
                  costoverman[k] * overmanning[k][i] +
                  costshort[k] * short[k][i]
                  for k in range(K) for i in range(I))
problem += cost

# Constraints
# Workforce balance for each manpower group and year
for k in range(K):
    for i in range(I):
        if i == 0:
            total_workforce = strength[k]
        else:
            # Retention of existing workers and recruitment from the previous year
            total_workforce = effective_new_recruits + \
                              (1 - moreonewaste[k]) * (strength[k] - effective_new_recruits)

        # New recruits in the year i
        effective_new_recruits = recruit[k][i] * (1 - lessonewaste[k])

        # Constraints must hold for each year
        problem += (total_workforce +
                    overmanning[k][i] +
                    short[k][i] -
                    redundancy[k][i]
                    >= requirement[k][i])

# Solve the problem
problem.solve()

# Extract results
recruit_result = [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)]
overmanning_result = [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)]
short_result = [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]

# Print the solution
output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')