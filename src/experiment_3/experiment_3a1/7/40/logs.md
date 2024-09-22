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
    \item $n_{steel\_quant}$: tons of steel required
    \item $mn_{percent}$: minimum percentage of manganese (Mn)
    \item $si_{min}$: minimum percentage of silicon (Si)
    \item $si_{max}$: maximum percentage of silicon (Si)
    \item $cont_{si_k}$: percentage of silicon in mineral $k$
    \item $cont_{mn_k}$: percentage of manganese in mineral $k$
    \item $mang_{price}$: price of Manganese (million euros per ton)
    \item $cost_k$: cost of mineral $k$ (million euros per thousand tons)
    \item $sell_{price}$: selling price of steel (million euros per ton)
    \item $melt_{price}$: cost of smelting a ton of mineral (million euros)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_k$: amount of mineral $k$ melted (in tons)
    \item $num_{mang}$: amount of Manganese directly added (in tons)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = (sell_{price} - melt_{price}) \cdot n_{steel\_quant} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k \right) - mang_{price} \cdot num_{mang}
\]

\textbf{Subject to:}
\begin{align}
    \sum_{k=1}^{K} (cont_{si_k} \cdot amount_k) + num_{mang} & \geq \frac{mn_{percent}}{100} \cdot n_{steel\_quant} \quad \text{(Mn requirement)} \\
    si_{min} \cdot n_{steel\_quant} & \leq \sum_{k=1}^{K} (cont_{si_k} \cdot amount_k) + num_{mang} \leq si_{max} \cdot n_{steel\_quant} \quad \text{(Si requirement)} \\
    amount_k & \geq 0 \quad \forall k \in \{1, \ldots, K\} \\
    num_{mang} & \geq 0
\end{align}

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
    \item $n_{steel\_quant}$: tons of steel required
    \item $mn_{percent}$: minimum percentage of manganese (Mn)
    \item $si_{min}$: minimum percentage of silicon (Si)
    \item $si_{max}$: maximum percentage of silicon (Si)
    \item $cont_{si_k}$: percentage of silicon in mineral $k$
    \item $cont_{mn_k}$: percentage of manganese in mineral $k$
    \item $mang_{price}$: price of Manganese (million euros per ton)
    \item $cost_k$: cost of mineral $k$ (million euros per thousand tons)
    \item $sell_{price}$: selling price of steel (million euros per ton)
    \item $melt_{price}$: cost of smelting a ton of mineral (million euros)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $amount_k$: amount of mineral $k$ melted (in tons)
    \item $num_{mang}$: amount of Manganese directly added (in tons)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = (sell_{price} - melt_{price}) \cdot n_{steel\_quant} - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot amount_k \right) - mang_{price} \cdot num_{mang}
\]

\textbf{Subject to:}
\begin{align}
    \sum_{k=1}^{K} (cont_{si_k} \cdot amount_k) + num_{mang} & \geq \frac{mn_{percent}}{100} \cdot n_{steel\_quant} \quad \text{(Mn requirement)} \\
    si_{min} \cdot n_{steel\_quant} & \leq \sum_{k=1}^{K} (cont_{si_k} \cdot amount_k) + num_{mang} \leq si_{max} \cdot n_{steel\_quant} \quad \text{(Si requirement)} \\
    amount_k & \geq 0 \quad \forall k \in \{1, \ldots, K\} \\
    num_{mang} & \geq 0
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
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

#### Initialize the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision variables
K = len(data['contsi'])
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0, cat='Continuous')
num_mang = pulp.LpVariable("num_mang", lowBound=0, cat='Continuous')

#### Objective function
problem += (
    (data['sell_price'] - data['melt_price']) * data['n_steel_quant'] -
    pulp.lpSum((data['cost'][k] / 1000) * amount_k[k] for k in range(K)) -
    data['mang_price'] * num_mang,
    "Total_Profit"
)

#### Constraints
problem += (
    pulp.lpSum(data['contmn'][k] * amount_k[k] for k in range(K)) + num_mang >= 
    (data['mn_percent'] / 100) * data['n_steel_quant'],
    "Mn_Requirement"
)

problem += (
    (data['si_min'] * data['n_steel_quant'] <= 
     pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) + num_mang) &
     (pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) + num_mang <= 
     data['si_max'] * data['n_steel_quant']),
    "Si_Requirement"
)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

