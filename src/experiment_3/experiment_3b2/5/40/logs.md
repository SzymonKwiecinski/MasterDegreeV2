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
To create a mathematical model for this linear programming problem, we will define the decision variables and set up the objective function and constraints based on the given information.

Let's define the decision variables:
- \( x_k \): the amount of mineral \( k \) used (in thousands of tons), for \( k = 1, \ldots, K \).
- \( m \): the amount of Manganese directly added (in tons).

The objective is to maximize profit. Profit is calculated as the difference between revenue from selling the steel and the costs of minerals, Manganese, and smelting costs.

Here is the linear programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Objective:} Maximize profit.

\begin{align*}
\text{Maximize:} \quad & P = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} (\text{cost}_k \times x_k) - \text{mang\_price} \times m - \text{melt\_price} \times \left( \sum_{k=1}^{K} x_k + m \right)
\end{align*}

\textbf{Subject to:}

\begin{align*}
& \sum_{k=1}^{K} x_k + m = \text{n\_steel\_quant} & \text{(Total amount of steel)}\\
& \sum_{k=1}^{K} \left(\text{contsi}_{k} \times x_k\right) \geq \text{si\_min} \times \text{n\_steel\_quant} & \text{(Minimum silicon requirement)}\\
& \sum_{k=1}^{K} \left(\text{contsi}_{k} \times x_k\right) \leq \text{si\_max} \times \text{n\_steel\_quant} & \text{(Maximum silicon requirement)}\\
& \sum_{k=1}^{K} \left(\text{contmn}_{k} \times x_k\right) + m \geq \frac{\text{mn\_percent}}{100} \times \text{n\_steel\_quant} & \text{(Minimum manganese requirement)}\\
& x_k \geq 0 \quad \forall k & \text{(Non-negativity)}\\
& m \geq 0 & \text{(Non-negativity)}
\end{align*}

\end{document}
```

In this model:
- The objective function \( P \) captures the profit by subtracting the production costs from the sales revenue.
- The constraints ensure that the steel contains the required percentage of manganese, has silicon within the specified range, and the total production matches the order quantity.
- Non-negativity constraints ensure that the amount of each mineral and manganese cannot be negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Objective:} Maximize profit.

\begin{align*}
\text{Maximize:} \quad & P = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} (\text{cost}_k \times x_k) - \text{mang\_price} \times m - \text{melt\_price} \times \left( \sum_{k=1}^{K} x_k + m \right)
\end{align*}

\textbf{Subject to:}

\begin{align*}
& \sum_{k=1}^{K} x_k + m = \text{n\_steel\_quant} & \text{(Total amount of steel)}\\
& \sum_{k=1}^{K} \left(\text{contsi}_{k} \times x_k\right) \geq \text{si\_min} \times \text{n\_steel\_quant} & \text{(Minimum silicon requirement)}\\
& \sum_{k=1}^{K} \left(\text{contsi}_{k} \times x_k\right) \leq \text{si\_max} \times \text{n\_steel\_quant} & \text{(Maximum silicon requirement)}\\
& \sum_{k=1}^{K} \left(\text{contmn}_{k} \times x_k\right) + m \geq \frac{\text{mn\_percent}}{100} \times \text{n\_steel\_quant} & \text{(Minimum manganese requirement)}\\
& x_k \geq 0 \quad \forall k & \text{(Non-negativity)}\\
& m \geq 0 & \text{(Non-negativity)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
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

#### Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
K = len(cost)
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### For steel types
m = pulp.LpVariable("m", lowBound=0)  #### For manganese

#### Objective function
profit = sell_price * n_steel_quant - pulp.lpSum(cost[k] * x[k] for k in range(K)) - mang_price * m - melt_price * (pulp.lpSum(x[k] for k in range(K)) + m)
problem += profit

#### Constraints
problem += pulp.lpSum(x[k] for k in range(K)) + m == n_steel_quant  #### Total amount of steel
problem += pulp.lpSum(contsi[k] * x[k] for k in range(K)) >= si_min * n_steel_quant  #### Minimum silicon requirement
problem += pulp.lpSum(contsi[k] * x[k] for k in range(K)) <= si_max * n_steel_quant  #### Maximum silicon requirement
problem += pulp.lpSum(contmn[k] * x[k] for k in range(K)) + m >= (mn_percent / 100) * n_steel_quant  #### Minimum manganese requirement

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

