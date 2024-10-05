# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Steel Production}

\subsection*{Parameters}
\begin{align*}
n_{steel\_quant} & : \text{Tons of steel required} \\
mn_{percent} & : \text{Minimum percentage of Manganese (Mn)} \\
si_{min} & : \text{Minimum percentage of Silicon (Si)} \\
si_{max} & : \text{Maximum percentage of Silicon (Si)} \\
contsi_{k} & : \text{Percentage of Silicon in mineral } k \\
contmn_{k} & : \text{Percentage of Manganese in mineral } k \\
mang\_price & : \text{Price of Manganese (million euros per ton)} \\
cost_{k} & : \text{Cost of mineral } k \text{ (million euros per thousand tons)} \\
sell\_price & : \text{Selling price of steel (million euros per ton)} \\
melt\_price & : \text{Cost of smelting a ton of mineral (million euros)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
amount_{k} & : \text{Amount of mineral } k \text{ melted (in tons)} \\
num\_mang & : \text{Amount of Manganese added (in tons)}
\end{align*}

\subsection*{Objective Function}
The objective is to maximize profit, which can be expressed as:
\begin{align*}
\text{Maximize} \quad Z = & \left( sell\_price \cdot n_{steel\_quant} \right) \\
& - \left( \sum_{k=1}^{K} \left( \frac{cost_{k}}{1000} \cdot amount_{k} \right) + melt\_price \cdot \sum_{k=1}^{K} amount_{k} + mang\_price \cdot num\_mang \right)
\end{align*}

\subsection*{Constraints}
1. \text{Steel production constraint (total mass of steel)}:
\begin{align*}
\sum_{k=1}^{K} amount_{k} + num\_mang = & n_{steel\_quant}
\end{align*}

2. \text{Manganese percentage constraint}:
\begin{align*}
\frac{\sum_{k=1}^{K} (contmn_{k} \cdot amount_{k}) + num\_mang}{n_{steel\_quant}} \geq & \frac{mn_{percent}}{100}
\end{align*}

3. \text{Silicon percentage constraints}:
\begin{align*}
si_{min} \leq & \frac{\sum_{k=1}^{K} (contsi_{k} \cdot amount_{k})}{n_{steel\_quant}} \leq si_{max}
\end{align*}

4. \text{Non-negativity constraints}:
\begin{align*}
amount_{k} \geq & 0 \quad \forall k \\
num\_mang \geq & 0
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Steel Production}

\subsection*{Parameters}
\begin{align*}
n_{steel\_quant} & : \text{Tons of steel required} \\
mn_{percent} & : \text{Minimum percentage of Manganese (Mn)} \\
si_{min} & : \text{Minimum percentage of Silicon (Si)} \\
si_{max} & : \text{Maximum percentage of Silicon (Si)} \\
contsi_{k} & : \text{Percentage of Silicon in mineral } k \\
contmn_{k} & : \text{Percentage of Manganese in mineral } k \\
mang\_price & : \text{Price of Manganese (million euros per ton)} \\
cost_{k} & : \text{Cost of mineral } k \text{ (million euros per thousand tons)} \\
sell\_price & : \text{Selling price of steel (million euros per ton)} \\
melt\_price & : \text{Cost of smelting a ton of mineral (million euros)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
amount_{k} & : \text{Amount of mineral } k \text{ melted (in tons)} \\
num\_mang & : \text{Amount of Manganese added (in tons)}
\end{align*}

\subsection*{Objective Function}
The objective is to maximize profit, which can be expressed as:
\begin{align*}
\text{Maximize} \quad Z = & \left( sell\_price \cdot n_{steel\_quant} \right) \\
& - \left( \sum_{k=1}^{K} \left( \frac{cost_{k}}{1000} \cdot amount_{k} \right) + melt\_price \cdot \sum_{k=1}^{K} amount_{k} + mang\_price \cdot num\_mang \right)
\end{align*}

\subsection*{Constraints}
1. \text{Steel production constraint (total mass of steel)}:
\begin{align*}
\sum_{k=1}^{K} amount_{k} + num\_mang = & n_{steel\_quant}
\end{align*}

2. \text{Manganese percentage constraint}:
\begin{align*}
\frac{\sum_{k=1}^{K} (contmn_{k} \cdot amount_{k}) + num\_mang}{n_{steel\_quant}} \geq & \frac{mn_{percent}}{100}
\end{align*}

3. \text{Silicon percentage constraints}:
\begin{align*}
si_{min} \leq & \frac{\sum_{k=1}^{K} (contsi_{k} \cdot amount_{k})}{n_{steel\_quant}} \leq si_{max}
\end{align*}

4. \text{Non-negativity constraints}:
\begin{align*}
amount_{k} \geq & 0 \quad \forall k \\
num\_mang \geq & 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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

#### Number of different minerals
num_minerals = len(data['contsi'])

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(num_minerals)]
num_mang = pulp.LpVariable('num_mang', lowBound=0, cat='Continuous')

#### Objective Function
revenue = data['sell_price'] * data['n_steel_quant']
cost_minerals = pulp.lpSum((data['cost'][k] / 1000) * amount[k] for k in range(num_minerals))
cost_melting = data['melt_price'] * pulp.lpSum(amount[k] for k in range(num_minerals))
cost_manganese = data['mang_price'] * num_mang
total_cost = cost_minerals + cost_melting + cost_manganese
problem += revenue - total_cost, "Profit"

#### Constraints
#### Steel production constraint
problem += pulp.lpSum(amount[k] for k in range(num_minerals)) + num_mang == data['n_steel_quant'], "Steel_Production"

#### Manganese percentage constraint
problem += (pulp.lpSum(data['contmn'][k] * amount[k] for k in range(num_minerals)) + num_mang) / data['n_steel_quant'] >= data['mn_percent'] / 100, "Mn_Percentage"

#### Silicon percentage constraints
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(num_minerals)) / data['n_steel_quant'] >= data['si_min'], "Si_Min_Constraint"
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(num_minerals)) / data['n_steel_quant'] <= data['si_max'], "Si_Max_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

