import pulp

# Data
data = {
    'n_steel_quant': 1000,
    'mn_percent': 0.45,
    'si_min': 3.25,
    'si_max': 5.0,
    'contsi': [4.0, 1.0, 0.6],
    'contmn': [0.45, 0.5, 0.4],
    'mang_price': 8.0,
    'cost': [21, 25, 15],
    'sell_price': 0.45,
    'melt_price': 0.005
}

# Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
K = len(data['contsi'])
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # amount of mineral k melted
y = pulp.LpVariable("y", lowBound=0)  # amount of Manganese added

# Objective Function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          pulp.lpSum((data['cost'][k] / 1000) * x[k] + data['melt_price'] * x[k] for k in range(K)) - 
          data['mang_price'] * y)

problem += profit, "Total_Profit"

# Constraints
# Manganese content constraint
problem += (pulp.lpSum(data['contmn'][k] * x[k] for k in range(K)) + y) >= (data['mn_percent'] / 100) * data['n_steel_quant'], "Mn_Content_Constraint"

# Silicon content constraints
problem += (pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) / data['n_steel_quant']) >= (data['si_min'] / 100), "Si_Min_Constraint"
problem += (pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) / data['n_steel_quant']) <= (data['si_max'] / 100), "Si_Max_Constraint"

# Solve the problem
problem.solve()

# Printing the outcome
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')