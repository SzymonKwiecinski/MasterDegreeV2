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

\textbf{Parameters:}
\begin{itemize}
    \item $n\_steel\_quant$: tons of steel required
    \item $mn\_percent$: minimum percentage of manganese (Mn)
    \item $si\_min$: minimum percentage of silicon (Si)
    \item $si\_max$: maximum percentage of silicon (Si)
    \item $contsi_k$: percentage of silicon in mineral $k$
    \item $contmn_k$: percentage of manganese in mineral $k$
    \item $mang\_price$: price of manganese in million euros per ton
    \item $cost_k$: cost of mineral $k$ in million euros per thousand tons
    \item $sell\_price$: selling price of steel in million euros per ton
    \item $melt\_price$: cost of melting one ton of mineral in million euros
    \item $K$: number of different minerals available
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_k$: amount of mineral $k$ melted (in thousands of tons)
    \item $num\_mang$: amount of manganese directly added (in tons)
\end{itemize}

\textbf{Objective Function:}
Maximize profit:
\[
Z = sell\_price \cdot n\_steel\_quant - \sum_{k=1}^{K} \left( cost_k \cdot amount_k + melt\_price \cdot amount_k \right) - mang\_price \cdot num\_mang
\]

\textbf{Constraints:}
\begin{align}
    \text{Manganese Constraint:} & \quad \frac{\sum_{k=1}^{K} (contmn_k \cdot amount_k) + num\_mang}{n\_steel\_quant} \geq \frac{mn\_percent}{100} \\
    \text{Silicon Minimum Constraint:} & \quad \frac{\sum_{k=1}^{K} (contsi_k \cdot amount_k)}{n\_steel\_quant} \geq \frac{si\_min}{100} \\
    \text{Silicon Maximum Constraint:} & \quad \frac{\sum_{k=1}^{K} (contsi_k \cdot amount_k)}{n\_steel\_quant} \leq \frac{si\_max}{100} \\
    \text{Non-negativity Constraints:} & \quad amount_k \geq 0 \quad \forall k \in \{1, \ldots, K\} \\
    & \quad num\_mang \geq 0 
\end{align}

\textbf{Output:}
\begin{itemize}
    \item $amount = [amount_1, amount_2, \ldots, amount_K]$
    \item $num\_mang$
\end{itemize}

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

\textbf{Parameters:}
\begin{itemize}
    \item $n\_steel\_quant$: tons of steel required
    \item $mn\_percent$: minimum percentage of manganese (Mn)
    \item $si\_min$: minimum percentage of silicon (Si)
    \item $si\_max$: maximum percentage of silicon (Si)
    \item $contsi_k$: percentage of silicon in mineral $k$
    \item $contmn_k$: percentage of manganese in mineral $k$
    \item $mang\_price$: price of manganese in million euros per ton
    \item $cost_k$: cost of mineral $k$ in million euros per thousand tons
    \item $sell\_price$: selling price of steel in million euros per ton
    \item $melt\_price$: cost of melting one ton of mineral in million euros
    \item $K$: number of different minerals available
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_k$: amount of mineral $k$ melted (in thousands of tons)
    \item $num\_mang$: amount of manganese directly added (in tons)
\end{itemize}

\textbf{Objective Function:}
Maximize profit:
\[
Z = sell\_price \cdot n\_steel\_quant - \sum_{k=1}^{K} \left( cost_k \cdot amount_k + melt\_price \cdot amount_k \right) - mang\_price \cdot num\_mang
\]

\textbf{Constraints:}
\begin{align}
    \text{Manganese Constraint:} & \quad \frac{\sum_{k=1}^{K} (contmn_k \cdot amount_k) + num\_mang}{n\_steel\_quant} \geq \frac{mn\_percent}{100} \\
    \text{Silicon Minimum Constraint:} & \quad \frac{\sum_{k=1}^{K} (contsi_k \cdot amount_k)}{n\_steel\_quant} \geq \frac{si\_min}{100} \\
    \text{Silicon Maximum Constraint:} & \quad \frac{\sum_{k=1}^{K} (contsi_k \cdot amount_k)}{n\_steel\_quant} \leq \frac{si\_max}{100} \\
    \text{Non-negativity Constraints:} & \quad amount_k \geq 0 \quad \forall k \in \{1, \ldots, K\} \\
    & \quad num\_mang \geq 0 
\end{align}

\textbf{Output:}
\begin{itemize}
    \item $amount = [amount_1, amount_2, \ldots, amount_K]$
    \item $num\_mang$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
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
K = len(contsi)

#### Create the LP problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

#### Objective Function
profit_expr = sell_price * n_steel_quant - pulp.lpSum((cost[k] + melt_price) * amount[k] for k in range(K)) - mang_price * num_mang
problem += profit_expr

#### Constraints
problem += (pulp.lpSum(contmn[k] * amount[k] for k in range(K)) + num_mang) >= mn_percent * n_steel_quant, "Manganese_Constraint"
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K))) >= si_min * n_steel_quant, "Silicon_Min_Constraint"
problem += (pulp.lpSum(contsi[k] * amount[k] for k in range(K))) <= si_max * n_steel_quant, "Silicon_Max_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
amount_values = [amount[k].varValue for k in range(K)]
num_mang_value = num_mang.varValue

print(f'Amount of minerals: {amount_values}')
print(f'Amount of manganese: {num_mang_value}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

