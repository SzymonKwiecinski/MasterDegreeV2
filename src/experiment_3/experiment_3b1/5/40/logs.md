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
& n_{\text{steel\_quant}} \text{ : tons of steel required} \\
& mn_{\text{percent}} \text{ : minimum percentage of Manganese (Mn)} \\
& si_{\text{min}} \text{ : minimum percentage of Silicon (Si)} \\
& si_{\text{max}} \text{ : maximum percentage of Silicon (Si)} \\
& contsi_k \text{ : percentage of Silicon in mineral } k \\
& contmn_k \text{ : percentage of Manganese in mineral } k \\
& mang_{\text{price}} \text{ : price of Manganese in million euros per ton} \\
& cost_k \text{ : cost of mineral } k \text{ in million euros per thousand tons} \\
& sell_{\text{price}} \text{ : selling price of steel in million euros per ton} \\
& melt_{\text{price}} \text{ : cost of melting a ton of mineral in million euros}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{amount}_k \text{ : amount of mineral } k \text{ to melt (in tons)} \\
& num_{\text{mang}} \text{ : amount of Manganese added (in tons)}
\end{align*}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \left( sell_{\text{price}} - \frac{1}{1000} \sum_{k=1}^{K} cost_k \cdot \text{amount}_k - mang_{\text{price}} \cdot num_{\text{mang}} - melt_{\text{price}} \sum_{k=1}^{K} \text{amount}_k \right) n_{\text{steel\_quant}}
\]

\subsection*{Constraints}
1. Ensure the required weight of steel:
\[
\sum_{k=1}^{K} contsi_k \cdot \text{amount}_k + num_{\text{mang}} \geq mn_{\text{percent}} \cdot n_{\text{steel\_quant}}
\]

2. Ensure Silicon content is within bounds:
\[
si_{\text{min}} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} contsi_k \cdot \text{amount}_k \leq si_{\text{max}} \cdot n_{\text{steel\_quant}}
\]

3. Non-negativity constraints:
\[
\text{amount}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
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
\begin{align*}
& n_{\text{steel\_quant}} \text{ : tons of steel required} \\
& mn_{\text{percent}} \text{ : minimum percentage of Manganese (Mn)} \\
& si_{\text{min}} \text{ : minimum percentage of Silicon (Si)} \\
& si_{\text{max}} \text{ : maximum percentage of Silicon (Si)} \\
& contsi_k \text{ : percentage of Silicon in mineral } k \\
& contmn_k \text{ : percentage of Manganese in mineral } k \\
& mang_{\text{price}} \text{ : price of Manganese in million euros per ton} \\
& cost_k \text{ : cost of mineral } k \text{ in million euros per thousand tons} \\
& sell_{\text{price}} \text{ : selling price of steel in million euros per ton} \\
& melt_{\text{price}} \text{ : cost of melting a ton of mineral in million euros}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{amount}_k \text{ : amount of mineral } k \text{ to melt (in tons)} \\
& num_{\text{mang}} \text{ : amount of Manganese added (in tons)}
\end{align*}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \left( sell_{\text{price}} - \frac{1}{1000} \sum_{k=1}^{K} cost_k \cdot \text{amount}_k - mang_{\text{price}} \cdot num_{\text{mang}} - melt_{\text{price}} \sum_{k=1}^{K} \text{amount}_k \right) n_{\text{steel\_quant}}
\]

\subsection*{Constraints}
1. Ensure the required weight of steel:
\[
\sum_{k=1}^{K} contsi_k \cdot \text{amount}_k + num_{\text{mang}} \geq mn_{\text{percent}} \cdot n_{\text{steel\_quant}}
\]

2. Ensure Silicon content is within bounds:
\[
si_{\text{min}} \cdot n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} contsi_k \cdot \text{amount}_k \leq si_{\text{max}} \cdot n_{\text{steel\_quant}}
\]

3. Non-negativity constraints:
\[
\text{amount}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]
\[
num_{\text{mang}} \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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

#### Create the linear programming problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)  #### amount_k
num_mang = pulp.LpVariable("num_mang", lowBound=0)  #### num_mang

#### Objective Function
profit = (data['sell_price'] - (1/1000) * pulp.lpSum(data['cost'][k] * amount[k] for k in range(K)) - \
          data['mang_price'] * num_mang - \
          data['melt_price'] * pulp.lpSum(amount[k] for k in range(K))) * data['n_steel_quant']

problem += profit

#### Constraints

#### 1. Ensure the required weight of steel
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) + num_mang >= data['mn_percent'] * data['n_steel_quant']

#### 2. Ensure Silicon content is within bounds
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) >= data['si_min'] * data['n_steel_quant']
problem += pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) <= data['si_max'] * data['n_steel_quant']

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

