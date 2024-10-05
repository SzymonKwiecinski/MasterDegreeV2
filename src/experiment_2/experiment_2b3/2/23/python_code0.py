import pulp

# Data from JSON
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

# Problem definition
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Indices
K = len(data['strength'])  # number of manpower categories
I = len(data['requirement'][0])  # number of years

# Decision variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize total costs
costs = []
for k in range(K):
    for i in range(I):
        costs.append(data['costredundancy'][k] * overmanning[(k, i)])
        costs.append(data['costoverman'][k] * overmanning[(k, i)])
        costs.append(data['costshort'][k] * short[(k, i)])

problem += pulp.lpSum(costs)

# Constraints
for k in range(K):
    workers_prev = data['strength'][k]
    for i in range(I):
        recruitment = recruit[(k, i)]
        
        if i == 0:
            # Natural wastage for the initial strength
            workers_prev = workers_prev * (1 - data['moreonewaste'][k])
        
        # Calculating total workers available
        # Workers from previous year who have been for more than a year
        workers_more_one = workers_prev * (1 - data['moreonewaste'][k])
        
        # New recruits & short-time workers contribution to the workforce
        workers_less_one = recruitment * (1 - data['lessonewaste'][k])
        short_contribution = 0.5 * short[(k, i)]
        
        # Workers available this year
        workers_current = workers_more_one + workers_less_one + short_contribution
        
        # Constraint for meeting/managing requirements
        # Requirement - Overmanning - Short-time <= Workers available
        problem += workers_current >= data['requirement'][k][i] - overmanning[(k, i)]
        problem += overmanning[(k, i)] <= data['num_overman']
        problem += short[(k, i)] <= data['num_shortwork']
        
        # Limit on recruitment
        problem += recruitment <= data['recruit'][k]
        
        # Update the previous year's workforce for the next iteration
        workers_prev = workers_current

# Solving the problem
problem.solve()

# Output results
output = {
    "recruit": [[pulp.value(recruit[(k, i)]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[(k, i)]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[(k, i)]) for i in range(I)] for k in range(K)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')