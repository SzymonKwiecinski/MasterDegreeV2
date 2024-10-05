import pulp

# Define Constants
K = 3  # Number of industries
T = 5  # Number of years

# Data from the JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Indices
industries = range(K)
years = range(T)

# Problem
problem = pulp.LpProblem("Economy_of_Interdependent_Industries", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("Produce", (industries, years), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", (industries, years), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", (industries, years), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t]
                      for k in industries for t in years)

# Constraints
for k in industries:
    problem += stockhold[k][0] == data['stock'][k]
    problem += pulp.LpConstraint(produce[k][0], sense=pulp.LpConstraintEQ, rhs=data['stock'][k])

    for t in years:
        if t > 0:
            problem += produce[k][t] <= data['capacity'][k] + pulp.lpSum(stockhold[j][t-1] * data['inputone'][j][k] for j in industries)
            problem += produce[k][t] >= data['demand'][k]
            
            if t >= 2:
                problem += data['capacity'][k] == data['capacity'][k] + buildcapa[k][t-2]
            
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in industries) - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t] for j in industries)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')