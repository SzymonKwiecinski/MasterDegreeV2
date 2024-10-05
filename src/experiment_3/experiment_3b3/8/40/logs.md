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
n_{\text{steel quant}} & : \text{Total tons of steel required} \\
mn_{\text{percent}} & : \text{Minimum percentage of manganese (Mn)} \\
si_{\text{min}} & : \text{Minimum percentage of silicon (Si)} \\
si_{\text{max}} & : \text{Maximum percentage of silicon (Si)} \\
\text{contsi}_k & : \text{Percentage of Si in mineral } k \\
\text{contmn}_k & : \text{Percentage of Mn in mineral } k \\
mang_{\text{price}} & : \text{Price of Manganese (in million euros per ton)} \\
\text{cost}_k & : \text{Cost of mineral } k \text{ (in million euros per ton)} \\
sell_{\text{price}} & : \text{Selling price of steel (in million euros per ton)} \\
melt_{\text{price}} & : \text{Cost of smelting a ton of mineral (in million euros)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{amount}_k & : \text{Amount of mineral } k \text{ to be melted} \\
num_{\text{mang}} & : \text{Amount of Manganese to be added directly}
\end{align*}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \left( sell_{\text{price}} - (mang_{\text{price}} \cdot num_{\text{mang}} + \sum_{k=1}^{K} \left( \text{cost}_k \cdot \text{amount}_k + melt_{\text{price}} \cdot \text{amount}_k \right)) \right) \cdot n_{\text{steel quant}}
\]

\subsection*{Constraints}
\begin{align*}
\text{1. Si Content Constraint:} \\
\sum_{k=1}^{K} (\text{contsi}_k \cdot \text{amount}_k) + 0 & \geq si_{\text{min}} \cdot n_{\text{steel quant}} \\
\sum_{k=1}^{K} (\text{contsi}_k \cdot \text{amount}_k) + 0 & \leq si_{\text{max}} \cdot n_{\text{steel quant}} \\

\text{2. Mn Content Constraint:} \\
\sum_{k=1}^{K} (\text{contmn}_k \cdot \text{amount}_k) + num_{\text{mang}} & \geq mn_{\text{percent}} \cdot n_{\text{steel quant}} \\

\text{3. Non-negativity Constraints:} \\
\text{amount}_k & \geq 0, \quad \forall k = 1, \ldots, K \\
num_{\text{mang}} & \geq 0 
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
n_{\text{steel quant}} & : \text{Total tons of steel required} \\
mn_{\text{percent}} & : \text{Minimum percentage of manganese (Mn)} \\
si_{\text{min}} & : \text{Minimum percentage of silicon (Si)} \\
si_{\text{max}} & : \text{Maximum percentage of silicon (Si)} \\
\text{contsi}_k & : \text{Percentage of Si in mineral } k \\
\text{contmn}_k & : \text{Percentage of Mn in mineral } k \\
mang_{\text{price}} & : \text{Price of Manganese (in million euros per ton)} \\
\text{cost}_k & : \text{Cost of mineral } k \text{ (in million euros per ton)} \\
sell_{\text{price}} & : \text{Selling price of steel (in million euros per ton)} \\
melt_{\text{price}} & : \text{Cost of smelting a ton of mineral (in million euros)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{amount}_k & : \text{Amount of mineral } k \text{ to be melted} \\
num_{\text{mang}} & : \text{Amount of Manganese to be added directly}
\end{align*}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \left( sell_{\text{price}} - (mang_{\text{price}} \cdot num_{\text{mang}} + \sum_{k=1}^{K} \left( \text{cost}_k \cdot \text{amount}_k + melt_{\text{price}} \cdot \text{amount}_k \right)) \right) \cdot n_{\text{steel quant}}
\]

\subsection*{Constraints}
\begin{align*}
\text{1. Si Content Constraint:} \\
\sum_{k=1}^{K} (\text{contsi}_k \cdot \text{amount}_k) + 0 & \geq si_{\text{min}} \cdot n_{\text{steel quant}} \\
\sum_{k=1}^{K} (\text{contsi}_k \cdot \text{amount}_k) + 0 & \leq si_{\text{max}} \cdot n_{\text{steel quant}} \\

\text{2. Mn Content Constraint:} \\
\sum_{k=1}^{K} (\text{contmn}_k \cdot \text{amount}_k) + num_{\text{mang}} & \geq mn_{\text{percent}} \cdot n_{\text{steel quant}} \\

\text{3. Non-negativity Constraints:} \\
\text{amount}_k & \geq 0, \quad \forall k = 1, \ldots, K \\
num_{\text{mang}} & \geq 0 
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Constants
n_steel_quant = data['n_steel_quant']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']
K = len(contsi)  #### Number of different minerals

#### Problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision Variables
amount = [pulp.LpVariable(f"amount_{k}", lowBound=0, cat='Continuous') for k in range(K)]
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

#### Objective Function
profit = (sell_price - (
    mang_price * num_mang + 
    pulp.lpSum((cost[k] + melt_price) * amount[k] for k in range(K))
)) * n_steel_quant

problem += profit, "Maximize Profit"

#### Constraints

#### Si Content Constraints
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= si_min * n_steel_quant
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= si_max * n_steel_quant

#### Mn Content Constraint
problem += pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= mn_percent * n_steel_quant

#### Solve
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

