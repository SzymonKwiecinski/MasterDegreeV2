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
To formulate the given Linear Programming (LP) problem in LaTeX, we'll define the decision variables, objective function, and constraints based on the provided problem statement.

Let's assume that:

- \( x_k \) is the amount (in thousand tons) of mineral \( k \) used.
- \( y \) is the amount (in tons) of Manganese directly added.

The objective is to maximize profit. The revenue comes from selling the steel, whereas costs arise from purchasing minerals, adding manganese, and melting.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Foundry Steel Production}

\subsection*{Given Data}
\begin{itemize}
    \item $n_{\text{steel\_quant}}$: Quantity of steel to be produced (tons)
    \item $mn_{\text{percent}}$: Minimum percentage of manganese required in steel
    \item $si_{\text{min}}$: Minimum percentage of silicon allowed in steel
    \item $si_{\text{max}}$: Maximum percentage of silicon allowed in steel
    \item $contsi_k$: Silicon content percentage in mineral $k$
    \item $contmn_k$: Manganese content percentage in mineral $k$
    \item $mang_{\text{price}}$: Cost of direct manganese addition (million euros per ton)
    \item $cost_k$: Cost of mineral $k$ (million euros per thousand tons)
    \item $sell_{\text{price}}$: Selling price of steel (million euros per ton)
    \item $melt_{\text{price}}$: Melting cost per ton of mineral (million euros)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Amount of mineral $k$ used (in thousand tons)
    \item $y$: Amount of manganese directly added (in tons)
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, given by the difference between revenue and costs:

\[
\text{Maximize} \quad Z = n_{\text{steel\_quant}} \times sell_{\text{price}} - \sum_{k=1}^{K} \left( x_k \times cost_k + x_k \times 1000 \times melt_{\text{price}} \right) - y \times mang_{\text{price}}
\]

\subsection*{Constraints}
\begin{align}
\sum_{k=1}^{K} x_k \times 1000 + y &= n_{\text{steel\_quant}} \quad \text{(Total steel production requirement)} \\
\frac{\sum_{k=1}^{K} x_k \times 1000 \times contmn_k + y}{n_{\text{steel\_quant}}} &\geq mn_{\text{percent}} \quad \text{(Manganese percentage constraint)} \\
si_{\text{min}} \times n_{\text{steel\_quant}} &\leq \sum_{k=1}^{K} x_k \times 1000 \times contsi_k \quad \text{(Minimum Silicon constraint)} \\
si_{\text{max}} \times n_{\text{steel\_quant}} &\geq \sum_{k=1}^{K} x_k \times 1000 \times contsi_k \quad \text{(Maximum Silicon constraint)} \\
x_k &\geq 0 \quad \text{for all } k \quad \text{(Non-negativity constraint for $x_k$)} \\
y &\geq 0 \quad \text{(Non-negativity constraint for $y$)}
\end{align}

\end{document}
```

This Linear Programming model helps to determine the optimal amounts of each mineral and directly added manganese in order to maximize the foundry's profit while adhering to the specified constraints on manganese and silicon content in the steel.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Foundry Steel Production}

\subsection*{Given Data}
\begin{itemize}
    \item $n_{\text{steel\_quant}}$: Quantity of steel to be produced (tons)
    \item $mn_{\text{percent}}$: Minimum percentage of manganese required in steel
    \item $si_{\text{min}}$: Minimum percentage of silicon allowed in steel
    \item $si_{\text{max}}$: Maximum percentage of silicon allowed in steel
    \item $contsi_k$: Silicon content percentage in mineral $k$
    \item $contmn_k$: Manganese content percentage in mineral $k$
    \item $mang_{\text{price}}$: Cost of direct manganese addition (million euros per ton)
    \item $cost_k$: Cost of mineral $k$ (million euros per thousand tons)
    \item $sell_{\text{price}}$: Selling price of steel (million euros per ton)
    \item $melt_{\text{price}}$: Melting cost per ton of mineral (million euros)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Amount of mineral $k$ used (in thousand tons)
    \item $y$: Amount of manganese directly added (in tons)
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, given by the difference between revenue and costs:

\[
\text{Maximize} \quad Z = n_{\text{steel\_quant}} \times sell_{\text{price}} - \sum_{k=1}^{K} \left( x_k \times cost_k + x_k \times 1000 \times melt_{\text{price}} \right) - y \times mang_{\text{price}}
\]

\subsection*{Constraints}
\begin{align}
\sum_{k=1}^{K} x_k \times 1000 + y &= n_{\text{steel\_quant}} \quad \text{(Total steel production requirement)} \\
\frac{\sum_{k=1}^{K} x_k \times 1000 \times contmn_k + y}{n_{\text{steel\_quant}}} &\geq mn_{\text{percent}} \quad \text{(Manganese percentage constraint)} \\
si_{\text{min}} \times n_{\text{steel\_quant}} &\leq \sum_{k=1}^{K} x_k \times 1000 \times contsi_k \quad \text{(Minimum Silicon constraint)} \\
si_{\text{max}} \times n_{\text{steel\_quant}} &\geq \sum_{k=1}^{K} x_k \times 1000 \times contsi_k \quad \text{(Maximum Silicon constraint)} \\
x_k &\geq 0 \quad \text{for all } k \quad \text{(Non-negativity constraint for $x_k$)} \\
y &\geq 0 \quad \text{(Non-negativity constraint for $y$)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
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

#### Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision variables
K = len(data['contsi'])
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Amount of mineral k used (in thousand tons)
y = pulp.LpVariable("y", lowBound=0)  #### Amount of manganese directly added (in tons)

#### Objective Function
profit = data['n_steel_quant'] * data['sell_price'] - \
         pulp.lpSum(x[k] * data['cost'][k] + x[k] * 1000 * data['melt_price'] for k in range(K)) - \
         y * data['mang_price']

problem += profit

#### Constraints
#### Total steel production requirement
problem += pulp.lpSum(x[k] * 1000 for k in range(K)) + y == data['n_steel_quant'], "Total_Production_Requirement"

#### Manganese percentage constraint
problem += (pulp.lpSum(x[k] * 1000 * data['contmn'][k] for k in range(K)) + y) / data['n_steel_quant'] >= data['mn_percent'], "Manganese_Percentage_Constraint"

#### Minimum Silicon constraint
problem += pulp.lpSum(x[k] * 1000 * data['contsi'][k] for k in range(K)) >= data['si_min'] * data['n_steel_quant'], "Min_Silicon_Constraint"

#### Maximum Silicon constraint
problem += pulp.lpSum(x[k] * 1000 * data['contsi'][k] for k in range(K)) <= data['si_max'] * data['n_steel_quant'], "Max_Silicon_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

