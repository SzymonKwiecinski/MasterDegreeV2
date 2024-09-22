import pulp
import json

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

# Problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
amount_k = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(len(data['contsi']))]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

# Objective Function
profit = (
    data['sell_price'] * data['n_steel_quant'] -
    pulp.lpSum((data['cost'][k] * (amount_k[k] / 1000) + data['melt_price'] * amount_k[k] + data['mang_price'] * num_mang) for k in range(len(data['contsi'])))
)
problem += profit, "Total_Profit"

# Constraints
problem += pulp.lpSum(amount_k) + num_mang == data['n_steel_quant'], "Total_Weight"

problem += (
    pulp.lpSum(data['contmn'][k] * amount_k[k] for k in range(len(data['contsi']))) + num_mang >= data['mn_percent'] * data['n_steel_quant'] / 100,
    "Manganese_Content"
)

problem += (
    pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(len(data['contsi']))) >= data['si_min'] * data['n_steel_quant'] / 100,
    "Silicon_Min_Content"
)

problem += (
    pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(len(data['contsi']))) <= data['si_max'] * data['n_steel_quant'] / 100,
    "Silicon_Max_Content"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')