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
    \item $n_{\text{steel\_quant}}$: Tons of steel required
    \item $mn_{\text{percent}}$: Minimum percentage of Manganese (Mn)
    \item $si_{\text{min}}$: Minimum percentage of Silicon (Si)
    \item $si_{\text{max}}$: Maximum percentage of Silicon (Si)
    \item $contsi_k$: Percentage of Silicon in mineral $k$, for $k = 1, \ldots, K$
    \item $contmn_k$: Percentage of Manganese in mineral $k$, for $k = 1, \ldots, K$
    \item $mang_{\text{price}}$: Price of Manganese per ton (in million euros)
    \item $cost_k$: Cost of mineral $k$ per thousand tons (in million euros)
    \item $sell_{\text{price}}$: Selling price of produced steel per ton (in million euros)
    \item $melt_{\text{price}}$: Cost of smelting a ton of mineral (in million euros)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_k$: Amount of mineral $k$ melted, for $k = 1, \ldots, K$
    \item $num_{\text{mang}}$: Amount of Manganese added
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Profit} = n_{\text{steel\_quant}} \cdot sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k + melt_{\text{price}} \cdot amount_k \right) - mang_{\text{price}} \cdot num_{\text{mang}}
\]

\subsection*{Constraints}
1. Manganese content requirement:
\[
\sum_{k=1}^{K} \left( \frac{contmn_k}{100} \cdot amount_k \right) + num_{\text{mang}} \geq n_{\text{steel\_quant}} \cdot \frac{mn_{\text{percent}}}{100}
\]
2. Silicon content requirements:
\[
\frac{\sum_{k=1}^{K} \left( \frac{contsi_k}{100} \cdot amount_k \right)}{n_{\text{steel\_quant}}} \geq \frac{si_{\text{min}}}{100}
\]
\[
\frac{\sum_{k=1}^{K} \left( \frac{contsi_k}{100} \cdot amount_k \right)}{n_{\text{steel\_quant}}} \leq \frac{si_{\text{max}}}{100}
\]
3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \text{for } k = 1, \ldots, K
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
    \item $n_{\text{steel\_quant}}$: Tons of steel required
    \item $mn_{\text{percent}}$: Minimum percentage of Manganese (Mn)
    \item $si_{\text{min}}$: Minimum percentage of Silicon (Si)
    \item $si_{\text{max}}$: Maximum percentage of Silicon (Si)
    \item $contsi_k$: Percentage of Silicon in mineral $k$, for $k = 1, \ldots, K$
    \item $contmn_k$: Percentage of Manganese in mineral $k$, for $k = 1, \ldots, K$
    \item $mang_{\text{price}}$: Price of Manganese per ton (in million euros)
    \item $cost_k$: Cost of mineral $k$ per thousand tons (in million euros)
    \item $sell_{\text{price}}$: Selling price of produced steel per ton (in million euros)
    \item $melt_{\text{price}}$: Cost of smelting a ton of mineral (in million euros)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_k$: Amount of mineral $k$ melted, for $k = 1, \ldots, K$
    \item $num_{\text{mang}}$: Amount of Manganese added
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Profit} = n_{\text{steel\_quant}} \cdot sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k + melt_{\text{price}} \cdot amount_k \right) - mang_{\text{price}} \cdot num_{\text{mang}}
\]

\subsection*{Constraints}
1. Manganese content requirement:
\[
\sum_{k=1}^{K} \left( \frac{contmn_k}{100} \cdot amount_k \right) + num_{\text{mang}} \geq n_{\text{steel\_quant}} \cdot \frac{mn_{\text{percent}}}{100}
\]
2. Silicon content requirements:
\[
\frac{\sum_{k=1}^{K} \left( \frac{contsi_k}{100} \cdot amount_k \right)}{n_{\text{steel\_quant}}} \geq \frac{si_{\text{min}}}{100}
\]
\[
\frac{\sum_{k=1}^{K} \left( \frac{contsi_k}{100} \cdot amount_k \right)}{n_{\text{steel\_quant}}} \leq \frac{si_{\text{max}}}{100}
\]
3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \text{for } k = 1, \ldots, K
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

#### Parameters 
K = len(data['contsi'])

#### Define the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]
num_mang = pulp.LpVariable('num_mang', lowBound=0, cat='Continuous')

#### Objective Function
problem += (data['n_steel_quant'] * data['sell_price'] 
            - sum(data['cost'][k] / 1000 * amount[k] + data['melt_price'] * amount[k] for k in range(K))
            - data['mang_price'] * num_mang)

#### Manganese content constraint
problem += (sum(data['contmn'][k] / 100 * amount[k] for k in range(K)) + num_mang 
            >= data['n_steel_quant'] * data['mn_percent'] / 100)

#### Silicon content minimum constraint
problem += (sum(data['contsi'][k] / 100 * amount[k] for k in range(K)) 
            >= data['n_steel_quant'] * data['si_min'] / 100)

#### Silicon content maximum constraint
problem += (sum(data['contsi'][k] / 100 * amount[k] for k in range(K)) 
            <= data['n_steel_quant'] * data['si_max'] / 100)

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

