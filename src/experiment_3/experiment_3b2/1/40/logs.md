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
To solve this problem, we need to formulate a Linear Programming (LP) model to maximize the profit of the foundry while satisfying the constraints on the composition of the steel.

Let's define the decision variables:
- \( x_k \): the amount of mineral \( k \) melted (in thousand tons) for \( k = 1, \ldots, K \).
- \( y \): the amount of Manganese directly added (in tons).

The objective function is to maximize profit, which is the revenue from selling the steel minus the costs of minerals, Manganese, and smelting. 

The constraints include:
1. The total steel produced must be exactly \( n_{\text{steel\_quant}} \) tons.
2. The percentage of Manganese in the steel must be at least \( \text{mn\_percent} \).
3. The percentage of Silicon in the steel must be between \( \text{si\_min} \) and \( \text{si\_max} \).

Let's formulate the LP model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{amount of mineral } k \text{ melted (in thousand tons), for } k = 1, \ldots, K \\
y & : \text{amount of Manganese directly added (in tons)}
\end{align*}

\subsection*{Objective Function}
The objective is to maximize profit:
\[
\text{Maximize } \quad \text{Profit} = \text{sell\_price} \cdot n_{\text{steel\_quant}} - \sum_{k=1}^{K} \text{cost}_k \cdot x_k - \text{mang\_price} \cdot y - \text{melt\_price} \cdot \sum_{k=1}^{K} x_k
\]

\subsection*{Constraints}
\begin{align}
\sum_{k=1}^{K} x_k + y & = n_{\text{steel\_quant}} \quad \text{(Total steel)} \\
\frac{\sum_{k=1}^{K} \text{contmn}_k \cdot x_k + y}{n_{\text{steel\_quant}}} & \geq \frac{\text{mn\_percent}}{100} \quad \text{(Manganese percentage)} \\
\frac{\sum_{k=1}^{K} \text{contsi}_k \cdot x_k}{n_{\text{steel\_quant}}} & \geq \frac{\text{si\_min}}{100} \quad \text{(Minimum Silicon percentage)} \\
\frac{\sum_{k=1}^{K} \text{contsi}_k \cdot x_k}{n_{\text{steel\_quant}}} & \leq \frac{\text{si\_max}}{100} \quad \text{(Maximum Silicon percentage)}
\end{align}

\subsection*{Non-negativity Constraints}
\begin{align*}
x_k & \geq 0 \quad \text{for } k = 1, \ldots, K \\
y & \geq 0 
\end{align*}

\end{document}
```

This formulation includes all necessary constraints and objectives to maximize the profit while ensuring the steel composition meets the specified requirements. The LP can then be solved using an appropriate optimization solver.

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
x_k & : \text{amount of mineral } k \text{ melted (in thousand tons), for } k = 1, \ldots, K \\
y & : \text{amount of Manganese directly added (in tons)}
\end{align*}

\subsection*{Objective Function}
The objective is to maximize profit:
\[
\text{Maximize } \quad \text{Profit} = \text{sell\_price} \cdot n_{\text{steel\_quant}} - \sum_{k=1}^{K} \text{cost}_k \cdot x_k - \text{mang\_price} \cdot y - \text{melt\_price} \cdot \sum_{k=1}^{K} x_k
\]

\subsection*{Constraints}
\begin{align}
\sum_{k=1}^{K} x_k + y & = n_{\text{steel\_quant}} \quad \text{(Total steel)} \\
\frac{\sum_{k=1}^{K} \text{contmn}_k \cdot x_k + y}{n_{\text{steel\_quant}}} & \geq \frac{\text{mn\_percent}}{100} \quad \text{(Manganese percentage)} \\
\frac{\sum_{k=1}^{K} \text{contsi}_k \cdot x_k}{n_{\text{steel\_quant}}} & \geq \frac{\text{si\_min}}{100} \quad \text{(Minimum Silicon percentage)} \\
\frac{\sum_{k=1}^{K} \text{contsi}_k \cdot x_k}{n_{\text{steel\_quant}}} & \leq \frac{\text{si\_max}}{100} \quad \text{(Maximum Silicon percentage)}
\end{align}

\subsection*{Non-negativity Constraints}
\begin{align*}
x_k & \geq 0 \quad \text{for } k = 1, \ldots, K \\
y & \geq 0 
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"n_steel_quant": 1000, "mn_percent": 0.45, "si_min": 3.25, "si_max": 5.0, "contsi": [4.0, 1.0, 0.6], "contmn": [0.45, 0.5, 0.4], "mang_price": 8.0, "cost": [21, 25, 15], "sell_price": 0.45, "melt_price": 0.005}')

#### Model parameters
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
K = len(cost)

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts('x', range(K), lowBound=0)  #### Amount of mineral k melted
y = pulp.LpVariable('y', lowBound=0)  #### Amount of Manganese added

#### Objective Function
profit = sell_price * n_steel_quant - pulp.lpSum(cost[k] * x[k] for k in range(K)) \
         - mang_price * y - melt_price * pulp.lpSum(x[k] for k in range(K))
problem += profit

#### Constraints
problem += pulp.lpSum(x[k] for k in range(K)) + y == n_steel_quant  #### Total steel
problem += (pulp.lpSum(contmn[k] * x[k] for k in range(K)) + y) / n_steel_quant >= mn_percent / 100  #### Manganese percentage
problem += pulp.lpSum(contsi[k] * x[k] for k in range(K)) / n_steel_quant >= si_min / 100  #### Minimum Silicon percentage
problem += pulp.lpSum(contsi[k] * x[k] for k in range(K)) / n_steel_quant <= si_max / 100  #### Maximum Silicon percentage

#### Solve the problem
problem.solve()

#### Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

