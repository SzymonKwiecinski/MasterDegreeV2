# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A foundry receives a specific order for \var{n_steel_quant} tons of steel. 
- This steel must meet the following characteristics: it must contain at least \var{mn_percent} percentage of manganese (Mn) while its percentage of silicon (SI) must be between \var{si_min} and \var{si_max}.
- To cast this steel, the foundry has limited quantities of several types of minerals.
- The contents expressed in percentage per mineral \var{k} are \var{contsi_{k}} for Si and \var{contmn_{k}} for Mn.
- The process for producing steel is such that direct addition of Mn is possible.
- This Manganese is available at a price of \var{mang_price} million euros per ton. 
- As for the minerals, it costs \var{cost_{k}} million euros per thousand tons for mineral \var{k}.
- The foundry plans to sell the steel produced at \var{sell_price} million euros per ton.
- The cost of smelting a ton of mineral is \var{melt_price} million euros.

INPUT FORMAT:

{
	"n_steel_quant": n_steel_quant,
	"mn_percent": mn_percent,
	"si_min": si_min,
	"si_max": si_max,
	"contsi": [contsi_{k} for k in 1,...,K]
	"contmn": [contmn_{k} for k in 1,...,K]
	"mang_price": mang_price,
	"cost": [cost_{k} for k in 1,...,K]
	"sell_price": sell_price,
	"melt_price": melt_price
}

OBJECTIVE: How should the manufacture manage the steel to maximize profit?

OUTPUT INFO:

- \var{amount} represents the amount of each mineral melted
- \var{num_mang} represents the amount of Manganese directly added

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
	"num_mang": [num_mang]
}
</DESCRIPTION>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
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

#### Setting up the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

#### Variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

#### Objective function: Maximize profit
revenue = data['n_steel_quant'] * data['sell_price']
costs = pulp.lpSum((data['cost'][k] * amount[k] / 1000) + (data['melt_price'] * amount[k]) for k in range(K)) + (data['mang_price'] * num_mang)
profit = revenue - costs
problem += profit

#### Constraints
#### Total weight of steel produced must be n_steel_quant
problem += pulp.lpSum((amount[k] * (data['contsi'][k] / 100)) for k in range(K)) + num_mang >= data['n_steel_quant'] * (data['mn_percent'] / 100), "Mn_Requirement"
problem += pulp.lpSum((amount[k] * (data['contsi'][k] / 100)) for k in range(K)) >= data['n_steel_quant'] * (data['si_min'] / 100), "Si_Min_Requirement"
problem += pulp.lpSum((amount[k] * (data['contsi'][k] / 100)) for k in range(K)) <= data['n_steel_quant'] * (data['si_max'] / 100), "Si_Max_Requirement"

#### Solve the problem
problem.solve()

#### Output the results
amount_solution = [amount[k].varValue for k in range(K)]
num_mang_solution = num_mang.varValue

output = {
    "amount": amount_solution,
    "num_mang": num_mang_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

