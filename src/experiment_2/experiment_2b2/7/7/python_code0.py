import pulp

def solve_rocket_problem(data):
    # Extract input data
    x_0 = data['X0']
    v_0 = data['V0']
    x_T = data['XT']
    v_T = data['VT']
    T = data['T']

    # Define the LP problem
    problem = pulp.LpProblem("Rocket_Thrust_Minimization", pulp.LpMinimize)

    # Decision variables
    x = [pulp.LpVariable(f"x_{t}", cat='Continuous') for t in range(T+1)]
    v = [pulp.LpVariable(f"v_{t}", cat='Continuous') for t in range(T+1)]
    a = [pulp.LpVariable(f"a_{t}", cat='Continuous') for t in range(T)]

    # Objective function: Minimize the maximum absolute acceleration
    max_abs_a = pulp.LpVariable("max_abs_a", lowBound=0, cat='Continuous')
    problem += max_abs_a

    # Constraints
    problem += (x[0] == x_0, "Initial_Position")
    problem += (v[0] == v_0, "Initial_Velocity")
    problem += (x[T] == x_T, "Final_Position")
    problem += (v[T] == v_T, "Final_Velocity")
    
    for t in range(T):
        # Discrete-time model equations
        problem += (x[t+1] == x[t] + v[t], f"Position_Update_{t}")
        problem += (v[t+1] == v[t] + a[t], f"Velocity_Update_{t}")
        # Maximum thrust constraint
        problem += (a[t] <= max_abs_a, f"Max_Thrust_Positive_{t}")
        problem += (-a[t] <= max_abs_a, f"Max_Thrust_Negative_{t}")

    # Solve the problem
    problem.solve()

    # Extract the results
    positions = [pulp.value(x[t]) for t in range(1, T+1)]
    velocities = [pulp.value(v[t]) for t in range(1, T+1)]
    accelerations = [pulp.value(a[t]) for t in range(T)]
    fuel_spent = sum(abs(pulp.value(a[t])) for t in range(T))
    
    # Print the objective value
    print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
    
    return {
        "x": positions,
        "v": velocities,
        "a": accelerations,
        "fuel_spend": fuel_spent,
    }

# Data input
data_input = {'X0': 0, 'V0': 0, 'XT': 1, 'VT': 0, 'T': 20}

# Solve the problem
output = solve_rocket_problem(data_input)
output