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
    \item $n_{\text{steel\_quant}}$: Tons of steel to produce
    \item $mn_{\text{percent}}$: Minimum percentage of manganese (Mn)
    \item $si_{\text{min}}$: Minimum percentage of silicon (Si)
    \item $si_{\text{max}}$: Maximum percentage of silicon (Si)
    \item $contsi_k$: Percentage of silicon in mineral $k$
    \item $contmn_k$: Percentage of manganese in mineral $k$
    \item $mang_{\text{price}}$: Price of manganese per ton (in million euros)
    \item $cost_k$: Cost of mineral $k$ per thousand tons (in million euros)
    \item $sell_{\text{price}}$: Selling price of steel per ton (in million euros)
    \item $melt_{\text{price}}$: Cost of smelting mineral per ton (in million euros)
\end{itemize}

\subsection*{Variables}

\begin{itemize}
    \item $amount_k$: Amount of mineral $k$ melted (in tons)
    \item $num_{\text{mang}}$: Amount of manganese directly added (in tons)
\end{itemize}

\subsection*{Objective Function}

Maximize profit:

\[
\text{Maximize } Z = n_{\text{steel\_quant}} \cdot sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k + melt_{\text{price}} \cdot amount_k \right) - mang_{\text{price}} \cdot num_{\text{mang}}
\]

\subsection*{Constraints}

1. **Steel Production Requirement**:
\[
\sum_{k=1}^{K} \left( contsi_k \cdot amount_k \right) + num_{\text{mang}} \cdot 0 \geq n_{\text{steel\_quant}} \cdot \left( \frac{si_{\text{min}}}{100} \right)
\]
\[
\sum_{k=1}^{K} \left( contsi_k \cdot amount_k \right) + num_{\text{mang}} \cdot 0 \leq n_{\text{steel\_quant}} \cdot \left( \frac{si_{\text{max}}}{100} \right)
\]

2. **Manganese Requirement**:
\[
\sum_{k=1}^{K} \left( contmn_k \cdot amount_k \right) + num_{\text{mang}} \geq n_{\text{steel\_quant}} \cdot \left( \frac{mn_{\text{percent}}}{100} \right)
\]

3. **Non-negativity Constraints**:
\[
amount_k \geq 0 \quad \forall k
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
    \item $n_{\text{steel\_quant}}$: Tons of steel to produce
    \item $mn_{\text{percent}}$: Minimum percentage of manganese (Mn)
    \item $si_{\text{min}}$: Minimum percentage of silicon (Si)
    \item $si_{\text{max}}$: Maximum percentage of silicon (Si)
    \item $contsi_k$: Percentage of silicon in mineral $k$
    \item $contmn_k$: Percentage of manganese in mineral $k$
    \item $mang_{\text{price}}$: Price of manganese per ton (in million euros)
    \item $cost_k$: Cost of mineral $k$ per thousand tons (in million euros)
    \item $sell_{\text{price}}$: Selling price of steel per ton (in million euros)
    \item $melt_{\text{price}}$: Cost of smelting mineral per ton (in million euros)
\end{itemize}

\subsection*{Variables}

\begin{itemize}
    \item $amount_k$: Amount of mineral $k$ melted (in tons)
    \item $num_{\text{mang}}$: Amount of manganese directly added (in tons)
\end{itemize}

\subsection*{Objective Function}

Maximize profit:

\[
\text{Maximize } Z = n_{\text{steel\_quant}} \cdot sell_{\text{price}} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k + melt_{\text{price}} \cdot amount_k \right) - mang_{\text{price}} \cdot num_{\text{mang}}
\]

\subsection*{Constraints}

1. **Steel Production Requirement**:
\[
\sum_{k=1}^{K} \left( contsi_k \cdot amount_k \right) + num_{\text{mang}} \cdot 0 \geq n_{\text{steel\_quant}} \cdot \left( \frac{si_{\text{min}}}{100} \right)
\]
\[
\sum_{k=1}^{K} \left( contsi_k \cdot amount_k \right) + num_{\text{mang}} \cdot 0 \leq n_{\text{steel\_quant}} \cdot \left( \frac{si_{\text{max}}}{100} \right)
\]

2. **Manganese Requirement**:
\[
\sum_{k=1}^{K} \left( contmn_k \cdot amount_k \right) + num_{\text{mang}} \geq n_{\text{steel\_quant}} \cdot \left( \frac{mn_{\text{percent}}}{100} \right)
\]

3. **Non-negativity Constraints**:
\[
amount_k \geq 0 \quad \forall k
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

#### Data from the JSON format
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

#### Number of minerals
K = len(contsi)

#### Create the problem variable
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

#### Objective function
profit = n_steel_quant * sell_price - pulp.lpSum((cost[k] / 1000) * amount[k] + melt_price * amount[k] for k in range(K)) - mang_price * num_mang
problem += profit, "Total_Profit"

#### Constraints
#### Steel production requirement
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) >= n_steel_quant * (si_min / 100), "Steel_Production_Min"
problem += pulp.lpSum(contsi[k] * amount[k] for k in range(K)) <= n_steel_quant * (si_max / 100), "Steel_Production_Max"

#### Manganese requirement
problem += pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang >= n_steel_quant * (mn_percent / 100), "Manganese_Requirement"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

