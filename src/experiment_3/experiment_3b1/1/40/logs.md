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
    \item $n_{steel\_quant}$: Total tons of steel to be produced
    \item $mn_{percent}$: Minimum percentage of manganese (Mn) required
    \item $si_{min}$: Minimum percentage of silicon (Si) required
    \item $si_{max}$: Maximum percentage of silicon (Si) allowed
    \item $contsi_k$: Percentage of silicon in mineral $k$
    \item $contmn_k$: Percentage of manganese in mineral $k$
    \item $mang\_price$: Cost of manganese (in million euros per ton)
    \item $cost_k$: Cost of mineral $k$ (in million euros per thousand tons)
    \item $sell\_price$: Selling price of the produced steel (in million euros per ton)
    \item $melt\_price$: Cost of smelting a ton of mineral (in million euros)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_k$: Amount of mineral $k$ melted (in tons)
    \item $num\_mang$: Amount of manganese added (in tons)
\end{itemize}

\textbf{Objective Function:} \\
Maximize Profit $Z$:
\[
Z = (sell\_price - mang\_price - melt\_price - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k \right)) \cdot n_{steel\_quant}
\]

\textbf{Constraints:}
\begin{itemize}
    \item Silicon content constraint:
    \[
    \sum_{k=1}^{K} (contsi_k \cdot amount_k) + \frac{si_{min}}{100} \cdot n_{steel\_quant} \leq n_{steel\_quant} \cdot si_{max}
    \]
    
    \item Manganese content constraint:
    \[
    \sum_{k=1}^{K} (contmn_k \cdot amount_k) + num\_mang \geq \frac{mn_{percent}}{100} \cdot n_{steel\_quant}
    \]
    
    \item Non-negativity constraints:
    \[
    amount_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
    \]
    \[
    num\_mang \geq 0
    \]
    
\end{itemize}

\textbf{Output:}
The optimal amounts of each mineral melted and the amount of manganese added can be represented as:
\[
\text{Output: } \{amount: [amount_k \text{ for } k \in \{1,\ldots,K\}], num\_mang: num\_mang\}
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

\textbf{Parameters:}
\begin{itemize}
    \item $n_{steel\_quant}$: Total tons of steel to be produced
    \item $mn_{percent}$: Minimum percentage of manganese (Mn) required
    \item $si_{min}$: Minimum percentage of silicon (Si) required
    \item $si_{max}$: Maximum percentage of silicon (Si) allowed
    \item $contsi_k$: Percentage of silicon in mineral $k$
    \item $contmn_k$: Percentage of manganese in mineral $k$
    \item $mang\_price$: Cost of manganese (in million euros per ton)
    \item $cost_k$: Cost of mineral $k$ (in million euros per thousand tons)
    \item $sell\_price$: Selling price of the produced steel (in million euros per ton)
    \item $melt\_price$: Cost of smelting a ton of mineral (in million euros)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_k$: Amount of mineral $k$ melted (in tons)
    \item $num\_mang$: Amount of manganese added (in tons)
\end{itemize}

\textbf{Objective Function:} \\
Maximize Profit $Z$:
\[
Z = (sell\_price - mang\_price - melt\_price - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k \right)) \cdot n_{steel\_quant}
\]

\textbf{Constraints:}
\begin{itemize}
    \item Silicon content constraint:
    \[
    \sum_{k=1}^{K} (contsi_k \cdot amount_k) + \frac{si_{min}}{100} \cdot n_{steel\_quant} \leq n_{steel\_quant} \cdot si_{max}
    \]
    
    \item Manganese content constraint:
    \[
    \sum_{k=1}^{K} (contmn_k \cdot amount_k) + num\_mang \geq \frac{mn_{percent}}{100} \cdot n_{steel\_quant}
    \]
    
    \item Non-negativity constraints:
    \[
    amount_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
    \]
    \[
    num\_mang \geq 0
    \]
    
\end{itemize}

\textbf{Output:}
The optimal amounts of each mineral melted and the amount of manganese added can be represented as:
\[
\text{Output: } \{amount: [amount_k \text{ for } k \in \{1,\ldots,K\}], num\_mang: num\_mang\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
data_json = '''{
    "n_steel_quant": 1000,
    "mn_percent": 0.45,
    "si_min": 3.25,
    "si_max": 5.0,
    "contsi": [4.0, 1.0, 0.6],
    "contmn": [0.45, 0.5, 0.4],
    "mang_price": 8.0,
    "cost": [21, 25, 15],
    "sell_price": 0.45,
    "melt_price": 0.005
}'''

data = json.loads(data_json)

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

K = len(contsi)  #### Number of minerals

#### Problem definition
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0)  #### Amount of each mineral
num_mang = pulp.LpVariable("num_mang", lowBound=0)  #### Amount of manganese added

#### Objective Function
profit = (sell_price - mang_price - melt_price - pulp.lpSum((cost[k] / 1000) * amount_k[k] for k in range(K))) * n_steel_quant
problem += profit, "Total_Profit"

#### Constraints
#### Silicon content constraint
problem += (pulp.lpSum(contsi[k] * amount_k[k] for k in range(K)) + (si_min / 100) * n_steel_quant <= n_steel_quant * si_max), "Silicon_Content_Constraint"

#### Manganese content constraint
problem += (pulp.lpSum(contmn[k] * amount_k[k] for k in range(K)) + num_mang >= (mn_percent / 100) * n_steel_quant), "Manganese_Content_Constraint"

#### Solve the problem
problem.solve()

#### Output results
amounts = [amount_k[k].varValue for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amounts of minerals melted: {amounts}')
print(f'Amount of manganese added: {num_mang.varValue}')
```

