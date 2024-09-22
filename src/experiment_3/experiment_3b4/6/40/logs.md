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
To solve the problem, we need to establish a linear programming model with the objective to maximize the profit from producing steel. The decision variables are the amounts of each mineral melted and the amount of Manganese directly added. The objective function will consider the revenue from selling the steel and the costs associated with minerals, Manganese, and smelting.

Here's the formulation of the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{align*}
    n_{\text{steel\_quant}} & \quad \text{(Tons of steel required)} \\
    \text{mn\_percent} & \quad \text{Minimum percentage of Mn required in steel} \\
    \text{si\_min} & \quad \text{Minimum percentage of Si allowed in steel} \\
    \text{si\_max} & \quad \text{Maximum percentage of Si allowed in steel} \\
    \text{contsi}_k & \quad \text{Percentage of Si in mineral $k$} \\
    \text{contmn}_k & \quad \text{Percentage of Mn in mineral $k$} \\
    \text{mang\_price} & \quad \text{Cost in million euros per ton of Mn} \\
    \text{cost}_k & \quad \text{Cost in million euros per thousand tons of mineral $k$} \\
    \text{sell\_price} & \quad \text{Selling price in million euros per ton of steel} \\
    \text{melt\_price} & \quad \text{Smelting cost in million euros per ton of mineral} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    \text{amount}_k & \quad \text{Amount of mineral $k$ melted (in tons)} \\
    \text{num\_mang} & \quad \text{Amount of Mn directly added (in tons)}
\end{align*}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Maximize} \quad Z = \text{sell\_price} \times n_{\text{steel\_quant}} - \sum_{k} \left( \frac{\text{cost}_k}{1000} \times \text{amount}_k \right) - \text{mang\_price} \times \text{num\_mang} - \text{melt\_price} \times \sum_k \text{amount}_k
\]

\subsection*{Constraints}
\begin{align*}
    \sum_k \left( \text{amount}_k \times \frac{\text{contmn}_k}{100} \right) + \text{num\_mang} &\geq \frac{\text{mn\_percent}}{100} \times n_{\text{steel\_quant}} \quad \text{(Mn content constraint)} \\
    \text{si\_min} \times n_{\text{steel\_quant}} &\leq \sum_k \left( \text{amount}_k \times \frac{\text{contsi}_k}{100} \right) \leq \text{si\_max} \times n_{\text{steel\_quant}} \quad \text{(Si content constraint)} \\
    \sum_k \text{amount}_k + \text{num\_mang} &= n_{\text{steel\_quant}} \quad \text{(Total quantity constraint)} \\
    \text{amount}_k &\geq 0 \quad \forall k \\
    \text{num\_mang} &\geq 0
\end{align*}
\end{document}
```

This model maximizes the profit by considering the revenue and subtracting the costs of minerals, Manganese, and smelting. The constraints ensure that the final steel meets the required composition in terms of Mn and Si while producing the desired quantity.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{align*}
    n_{\text{steel\_quant}} & \quad \text{(Tons of steel required)} \\
    \text{mn\_percent} & \quad \text{Minimum percentage of Mn required in steel} \\
    \text{si\_min} & \quad \text{Minimum percentage of Si allowed in steel} \\
    \text{si\_max} & \quad \text{Maximum percentage of Si allowed in steel} \\
    \text{contsi}_k & \quad \text{Percentage of Si in mineral $k$} \\
    \text{contmn}_k & \quad \text{Percentage of Mn in mineral $k$} \\
    \text{mang\_price} & \quad \text{Cost in million euros per ton of Mn} \\
    \text{cost}_k & \quad \text{Cost in million euros per thousand tons of mineral $k$} \\
    \text{sell\_price} & \quad \text{Selling price in million euros per ton of steel} \\
    \text{melt\_price} & \quad \text{Smelting cost in million euros per ton of mineral} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    \text{amount}_k & \quad \text{Amount of mineral $k$ melted (in tons)} \\
    \text{num\_mang} & \quad \text{Amount of Mn directly added (in tons)}
\end{align*}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Maximize} \quad Z = \text{sell\_price} \times n_{\text{steel\_quant}} - \sum_{k} \left( \frac{\text{cost}_k}{1000} \times \text{amount}_k \right) - \text{mang\_price} \times \text{num\_mang} - \text{melt\_price} \times \sum_k \text{amount}_k
\]

\subsection*{Constraints}
\begin{align*}
    \sum_k \left( \text{amount}_k \times \frac{\text{contmn}_k}{100} \right) + \text{num\_mang} &\geq \frac{\text{mn\_percent}}{100} \times n_{\text{steel\_quant}} \quad \text{(Mn content constraint)} \\
    \text{si\_min} \times n_{\text{steel\_quant}} &\leq \sum_k \left( \text{amount}_k \times \frac{\text{contsi}_k}{100} \right) \leq \text{si\_max} \times n_{\text{steel\_quant}} \quad \text{(Si content constraint)} \\
    \sum_k \text{amount}_k + \text{num\_mang} &= n_{\text{steel\_quant}} \quad \text{(Total quantity constraint)} \\
    \text{amount}_k &\geq 0 \quad \forall k \\
    \text{num\_mang} &\geq 0
\end{align*}
\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parsing the data
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

#### Problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(len(contsi))]
num_mang = pulp.LpVariable('num_mang', lowBound=0)

#### Objective Function
profit = sell_price * n_steel_quant - sum((cost[k]/1000) * amount[k] for k in range(len(contsi))) \
         - mang_price * num_mang - melt_price * sum(amount[k] for k in range(len(contsi)))

problem += profit

#### Constraints
#### Mn content constraint
problem += sum(amount[k] * (contmn[k]/100) for k in range(len(contmn))) + num_mang >= (mn_percent/100) * n_steel_quant

#### Si content constraint
problem += si_min * n_steel_quant <= sum(amount[k] * (contsi[k]/100) for k in range(len(contsi)))
problem += sum(amount[k] * (contsi[k]/100) for k in range(len(contsi))) <= si_max * n_steel_quant

#### Total quantity constraint
problem += sum(amount) + num_mang == n_steel_quant

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

