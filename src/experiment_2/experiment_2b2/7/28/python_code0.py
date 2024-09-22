import pulp

def fit_line(data):
    y = data["Y"]
    x = data["X"]
    K = data["K"]

    # Initialize the problem
    problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

    # Decision Variables
    intercept = pulp.LpVariable('Intercept', lowBound=None)
    slope = pulp.LpVariable('Slope', lowBound=None)
    deviations = [pulp.LpVariable(f'Deviation_{i}', lowBound=0) for i in range(K)]

    # Objective Function: Minimize the sum of absolute deviations
    problem += pulp.lpSum(deviations)

    # Constraints: Calculate absolute deviations
    for k in range(K):
        problem += (intercept + slope * x[k] - y[k] <= deviations[k])
        problem += (-(intercept + slope * x[k] - y[k]) <= deviations[k])

    # Solve the problem
    problem.solve()

    # Output the results
    output = {
        "intercept": pulp.value(intercept),
        "slope": pulp.value(slope)
    }
    
    print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
    return output

data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
result = fit_line(data)
print(result)