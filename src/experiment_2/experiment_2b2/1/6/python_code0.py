import pulp

def minimize_fuel_consumption(data):
    # Extracting data
    x_0 = data['InitialPosition']
    v_0 = data['InitialVelocity']
    x_T = data['FinalPosition']
    v_T = data['FinalVelocity']
    T = data['TotalTime']

    # Problem definition
    problem = pulp.LpProblem("RocketTrajectory", pulp.LpMinimize)

    # Decision Variables
    x = pulp.LpVariable.dicts("x", range(T+1), lowBound=None)
    v = pulp.LpVariable.dicts("v", range(T+1), lowBound=None)
    a = pulp.LpVariable.dicts("a", range(T), lowBound=None)
    abs_a = pulp.LpVariable.dicts("abs_a", range(T), lowBound=0)

    # Objective Function: minimize total absolute acceleration (fuel used)
    problem += pulp.lpSum(abs_a[t] for t in range(T))

    # Constraints
    for t in range(T):
        problem += x[t+1] == x[t] + v[t], f"Position_Update_{t}"
        problem += v[t+1] == v[t] + a[t], f"Velocity_Update_{t}"
        problem += abs_a[t] >= a[t], f"Abs_Constraint_Pos_{t}"
        problem += abs_a[t] >= -a[t], f"Abs_Constraint_Neg_{t}"

    # Initial conditions
    problem += x[0] == x_0, "Initial_Position"
    problem += v[0] == v_0, "Initial_Velocity"

    # Final conditions
    problem += x[T] == x_T, "Final_Position"
    problem += v[T] == v_T, "Final_Velocity"

    # Solve the problem
    problem.solve()

    # Collect the results
    rocket_trajectory = {
        "x": [pulp.value(x[t]) for t in range(T+1)],
        "v": [pulp.value(v[t]) for t in range(T+1)],
        "a": [pulp.value(a[t]) for t in range(T)],
        "fuel_spend": sum(abs(pulp.value(a[t])) for t in range(T))
    }

    print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
    
    return rocket_trajectory

# Input data
data = {'InitialPosition': 0, 'InitialVelocity': 0, 'FinalPosition': 1, 'FinalVelocity': 0, 'TotalTime': 20}

# Solve the problem
output_data = minimize_fuel_consumption(data)
output_data