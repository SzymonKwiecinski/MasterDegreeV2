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
\begin{itemize}
    \item $n_{\text{steel\_quant}}$: required tons of steel
    \item $mn_{\text{percent}}$: minimum percentage of manganese (Mn)
    \item $si_{\text{min}}$: minimum percentage of silicon (Si)
    \item $si_{\text{max}}$: maximum percentage of silicon (Si)
    \item $contsi_k$: percentage of silicon in mineral $k$
    \item $contmn_k$: percentage of manganese in mineral $k$
    \item $mang_{\text{price}}$: price of manganese per ton (million euros)
    \item $cost_k$: cost of mineral $k$ per thousand tons (million euros)
    \item $sell_{\text{price}}$: selling price of steel per ton (million euros)
    \item $melt_{\text{price}}$: cost of smelting per ton of mineral (million euros)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_k$: amount of mineral $k$ melted (in tons)
    \item $num_{\text{mang}}$: amount of manganese added (in tons)
\end{itemize}

\subsection*{Objective Function}
Maximize the profit: 
\[
Z = \left( sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} + melt_{\text{price}} \right) \cdot amount_k - mang_{\text{price}} \cdot num_{\text{mang}} \right) \cdot n_{\text{steel\_quant}}
\]

\subsection*{Constraints}
1. Total steel produced must equal the required steel:
\[
\frac{1}{100} \sum_{k=1}^{K} contsi_k \cdot amount_k + num_{\text{mang}} \cdot \frac{mn_{\text{percent}}}{100} \geq n_{\text{steel\_quant}} 
\]

2. Manganese constraint:
\[
\frac{num_{\text{mang}}}{n_{\text{steel\_quant}}} \geq \frac{mn_{\text{percent}}}{100}
\]

3. Silicon percentage constraints:
\[
\frac{1}{100} \sum_{k=1}^{K} contsi_k \cdot amount_k \geq si_{\text{min}} \cdot n_{\text{steel\_quant}} 
\]
\[
\frac{1}{100} \sum_{k=1}^{K} contsi_k \cdot amount_k \leq si_{\text{max}} \cdot n_{\text{steel\_quant}} 
\]

4. Non-negativity constraints:
\[
amount_k \geq 0 \quad \forall k = 1, \ldots, K
\]
\[
num_{\text{mang}} \geq 0
\]

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
\begin{itemize}
    \item $n_{\text{steel\_quant}}$: required tons of steel
    \item $mn_{\text{percent}}$: minimum percentage of manganese (Mn)
    \item $si_{\text{min}}$: minimum percentage of silicon (Si)
    \item $si_{\text{max}}$: maximum percentage of silicon (Si)
    \item $contsi_k$: percentage of silicon in mineral $k$
    \item $contmn_k$: percentage of manganese in mineral $k$
    \item $mang_{\text{price}}$: price of manganese per ton (million euros)
    \item $cost_k$: cost of mineral $k$ per thousand tons (million euros)
    \item $sell_{\text{price}}$: selling price of steel per ton (million euros)
    \item $melt_{\text{price}}$: cost of smelting per ton of mineral (million euros)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_k$: amount of mineral $k$ melted (in tons)
    \item $num_{\text{mang}}$: amount of manganese added (in tons)
\end{itemize}

\subsection*{Objective Function}
Maximize the profit: 
\[
Z = \left( sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} + melt_{\text{price}} \right) \cdot amount_k - mang_{\text{price}} \cdot num_{\text{mang}} \right) \cdot n_{\text{steel\_quant}}
\]

\subsection*{Constraints}
1. Total steel produced must equal the required steel:
\[
\frac{1}{100} \sum_{k=1}^{K} contsi_k \cdot amount_k + num_{\text{mang}} \cdot \frac{mn_{\text{percent}}}{100} \geq n_{\text{steel\_quant}} 
\]

2. Manganese constraint:
\[
\frac{num_{\text{mang}}}{n_{\text{steel\_quant}}} \geq \frac{mn_{\text{percent}}}{100}
\]

3. Silicon percentage constraints:
\[
\frac{1}{100} \sum_{k=1}^{K} contsi_k \cdot amount_k \geq si_{\text{min}} \cdot n_{\text{steel\_quant}} 
\]
\[
\frac{1}{100} \sum_{k=1}^{K} contsi_k \cdot amount_k \leq si_{\text{max}} \cdot n_{\text{steel\_quant}} 
\]

4. Non-negativity constraints:
\[
amount_k \geq 0 \quad \forall k = 1, \ldots, K
\]
\[
num_{\text{mang}} \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Here's the Python code using the Pulp library to create a linear programming model based on the provided mathematical model and data.

```python
import pulp

#### Data from the input JSON
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

#### Problem definition
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  #### amounts of minerals
num_mang = pulp.LpVariable("num_mang", lowBound=0)  #### amount of manganese added

#### Objective function
profit = (data['sell_price'] - pulp.lpSum((data['cost'][k] / 1000 + data['melt_price']) * amount[k] for k in range(K)) - data['mang_price'] * num_mang) * data['n_steel_quant']
problem += profit, "Total_Profit"

#### Constraints
#### Total steel produced must equal the required steel
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / 100 + num_mang * (data['mn_percent'] / 100) >= data['n_steel_quant']), "Steel_Production"

#### Manganese constraint
problem += (num_mang / data['n_steel_quant'] >= data['mn_percent'] / 100), "Manganese_Constraint"

#### Silicon percentage constraints
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / 100 >= data['si_min'] * data['n_steel_quant']), "Silicon_Min_Constraint"
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / 100 <= data['si_max'] * data['n_steel_quant']), "Silicon_Max_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This script defines a linear programming problem with the necessary constraints and the objective function for maximizing profit. It then solves the problem using the Pulp library and prints the calculated objective value.

