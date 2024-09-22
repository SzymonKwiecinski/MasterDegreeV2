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
To model this problem as a linear programming problem, we will define decision variables, an objective function, and constraints based on the problem description provided.

######### Decision Variables
- Let \( x_k \) denote the amount (in thousands of tons) of mineral \( k \) used.
- Let \( y \) denote the amount (in tons) of manganese (Mn) directly added.

######### Objective Function
The objective is to maximize the profit, which is the revenue from selling the steel minus the costs of the minerals, manganese, and smelting.

\[
\text{Profit} = \text{Revenue} - \text{Cost of Minerals} - \text{Cost of Manganese} - \text{Cost of Smelting}
\]

\[
\text{Profit} = n_{\text{steel\_quant}} \times \text{sell\_price} - \sum_{k=1}^{K} \left( x_k \times \text{cost}_k \right) - y \times \text{mang\_price} - \sum_{k=1}^{K} \left( x_k \times \text{melt\_price} \right)
\]

######### Constraints
1. **Steel Production Constraint**: The total tons of steel produced should be equal to the order size.
   \[
   \sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
   \]

2. **Manganese Content Constraint**: The manganese content must be at least the specified percentage.
   \[
   \sum_{k=1}^{K} \left( x_k \times \frac{\text{contmn}_k}{1000} \right) + y \geq \frac{\text{mn\_percent}}{100} \times n_{\text{steel\_quant}}
   \]

3. **Silicon Content Constraints**: The silicon content must be within the specified range.
   \[
   \frac{\text{si\_min}}{100} \times n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \left( x_k \times \frac{\text{contsi}_k}{1000} \right) \leq \frac{\text{si\_max}}{100} \times n_{\text{steel\_quant}}
   \]

4. **Non-negativity Constraint**: All variables must be non-negative.
   \[
   x_k \geq 0 \quad \forall k = 1, \ldots, K
   \]
   \[
   y \geq 0
   \]

Here is the complete \(\LaTeX\) code:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_k &: \text{Amount of mineral } k \text{ used (in thousands of tons), for } k = 1, \ldots, K \\
y &: \text{Amount of manganese directly added (in tons)}
\end{align*}

\subsection*{Objective Function}
Maximize the profit:
\begin{align*}
\text{Profit} = n_{\text{steel\_quant}} \times \text{sell\_price} - \sum_{k=1}^{K} \left( x_k \times \text{cost}_k \right) - y \times \text{mang\_price} - \sum_{k=1}^{K} \left( x_k \times \text{melt\_price} \right)
\end{align*}

\subsection*{Constraints}
1. Total steel production:
\begin{align*}
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\end{align*}

2. Manganese content:
\begin{align*}
\sum_{k=1}^{K} \left( x_k \times \frac{\text{contmn}_k}{1000} \right) + y \geq \frac{\text{mn\_percent}}{100} \times n_{\text{steel\_quant}}
\end{align*}

3. Silicon content:
\begin{align*}
\frac{\text{si\_min}}{100} \times n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \left( x_k \times \frac{\text{contsi}_k}{1000} \right) \leq \frac{\text{si\_max}}{100} \times n_{\text{steel\_quant}}
\end{align*}

4. Non-negativity:
\begin{align*}
x_k \geq 0 \quad \forall k = 1, \ldots, K \\
y \geq 0
\end{align*}

\end{document}
```

This linear programming model aims to determine the optimal amounts of minerals and manganese that maximize the profit while fulfilling all the constraints.

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

\subsection*{Decision Variables}
\begin{align*}
x_k &: \text{Amount of mineral } k \text{ used (in thousands of tons), for } k = 1, \ldots, K \\
y &: \text{Amount of manganese directly added (in tons)}
\end{align*}

\subsection*{Objective Function}
Maximize the profit:
\begin{align*}
\text{Profit} = n_{\text{steel\_quant}} \times \text{sell\_price} - \sum_{k=1}^{K} \left( x_k \times \text{cost}_k \right) - y \times \text{mang\_price} - \sum_{k=1}^{K} \left( x_k \times \text{melt\_price} \right)
\end{align*}

\subsection*{Constraints}
1. Total steel production:
\begin{align*}
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\end{align*}

2. Manganese content:
\begin{align*}
\sum_{k=1}^{K} \left( x_k \times \frac{\text{contmn}_k}{1000} \right) + y \geq \frac{\text{mn\_percent}}{100} \times n_{\text{steel\_quant}}
\end{align*}

3. Silicon content:
\begin{align*}
\frac{\text{si\_min}}{100} \times n_{\text{steel\_quant}} \leq \sum_{k=1}^{K} \left( x_k \times \frac{\text{contsi}_k}{1000} \right) \leq \frac{\text{si\_max}}{100} \times n_{\text{steel\_quant}}
\end{align*}

4. Non-negativity:
\begin{align*}
x_k \geq 0 \quad \forall k = 1, \ldots, K \\
y \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"n_steel_quant": 1000, "mn_percent": 0.45, "si_min": 3.25, "si_max": 5.0, "contsi": [4.0, 1.0, 0.6], "contmn": [0.45, 0.5, 0.4], "mang_price": 8.0, "cost": [21, 25, 15], "sell_price": 0.45, "melt_price": 0.005}')

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
K = len(cost)

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Amount of mineral k used
y = pulp.LpVariable("y", lowBound=0)                  #### Amount of manganese added

#### Objective function
profit = n_steel_quant * sell_price - pulp.lpSum([x[k] * cost[k] for k in range(K)]) - y * mang_price - pulp.lpSum([x[k] * melt_price for k in range(K)])
problem += profit

#### Constraints
#### Total steel production
problem += pulp.lpSum([x[k] for k in range(K)]) + y == n_steel_quant, "SteelProduction"

#### Manganese content
problem += pulp.lpSum([x[k] * (contmn[k] / 1000) for k in range(K)]) + y >= (mn_percent / 100) * n_steel_quant, "ManganeseContent"

#### Silicon content
problem += (si_min / 100) * n_steel_quant <= pulp.lpSum([x[k] * (contsi[k] / 1000) for k in range(K)]) <= (si_max / 100) * n_steel_quant, "SiliconContent"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

