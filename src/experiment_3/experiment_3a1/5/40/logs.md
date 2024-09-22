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

\begin{align*}
n & : \text{Steel quantity required (tons)} \\
mn & : \text{Minimum percentage of Manganese (Mn)} \\
si_{min} & : \text{Minimum percentage of Silicon (Si)} \\
si_{max} & : \text{Maximum percentage of Silicon (Si)} \\
K & : \text{Number of minerals} \\
contsi_{k} & : \text{Percentage of Silicon in mineral } k \\
contmn_{k} & : \text{Percentage of Manganese in mineral } k \\
mang\_price & : \text{Price of Manganese (million euros per ton)} \\
cost_{k} & : \text{Cost of mineral } k \text{ (million euros per thousand tons)} \\
sell\_price & : \text{Selling price of steel (million euros per ton)} \\
melt\_price & : \text{Cost of smelting a ton of mineral (million euros)}
\end{align*}

\textbf{Decision Variables:}

\begin{align*}
amount_{k} & : \text{Amount of mineral } k \text{ melted (in tons)} \quad \forall k \in \{1, \ldots, K\} \\
num\_mang & : \text{Amount of Manganese directly added (in tons)}
\end{align*}

\textbf{Objective Function:}

Maximize profit \( P \):

\[
P = sell\_price \cdot n - \left( \sum_{k=1}^{K} \left(\frac{cost_{k}}{1000} \cdot amount_{k}\right) + melt\_price \cdot \sum_{k=1}^{K} amount_{k} + mang\_price \cdot num\_mang \right)
\]

\textbf{Constraints:}

1. Manganese requirement:
\[
\sum_{k=1}^{K} contmn_{k} \cdot amount_{k} + num\_mang \geq \frac{mn}{100} \cdot n
\]

2. Silicon content limits:
\[
si_{min} \leq \frac{\sum_{k=1}^{K} contsi_{k} \cdot amount_{k}}{n} \leq si_{max}
\]

3. Non-negativity constraints:
\[
amount_{k} \geq 0 \quad \forall k \in \{1, \ldots, K\} \\
num\_mang \geq 0
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

\begin{align*}
n & : \text{Steel quantity required (tons)} \\
mn & : \text{Minimum percentage of Manganese (Mn)} \\
si_{min} & : \text{Minimum percentage of Silicon (Si)} \\
si_{max} & : \text{Maximum percentage of Silicon (Si)} \\
K & : \text{Number of minerals} \\
contsi_{k} & : \text{Percentage of Silicon in mineral } k \\
contmn_{k} & : \text{Percentage of Manganese in mineral } k \\
mang\_price & : \text{Price of Manganese (million euros per ton)} \\
cost_{k} & : \text{Cost of mineral } k \text{ (million euros per thousand tons)} \\
sell\_price & : \text{Selling price of steel (million euros per ton)} \\
melt\_price & : \text{Cost of smelting a ton of mineral (million euros)}
\end{align*}

\textbf{Decision Variables:}

\begin{align*}
amount_{k} & : \text{Amount of mineral } k \text{ melted (in tons)} \quad \forall k \in \{1, \ldots, K\} \\
num\_mang & : \text{Amount of Manganese directly added (in tons)}
\end{align*}

\textbf{Objective Function:}

Maximize profit \( P \):

\[
P = sell\_price \cdot n - \left( \sum_{k=1}^{K} \left(\frac{cost_{k}}{1000} \cdot amount_{k}\right) + melt\_price \cdot \sum_{k=1}^{K} amount_{k} + mang\_price \cdot num\_mang \right)
\]

\textbf{Constraints:}

1. Manganese requirement:
\[
\sum_{k=1}^{K} contmn_{k} \cdot amount_{k} + num\_mang \geq \frac{mn}{100} \cdot n
\]

2. Silicon content limits:
\[
si_{min} \leq \frac{\sum_{k=1}^{K} contsi_{k} \cdot amount_{k}}{n} \leq si_{max}
\]

3. Non-negativity constraints:
\[
amount_{k} \geq 0 \quad \forall k \in \{1, \ldots, K\} \\
num\_mang \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Create the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

#### Decision variables
K = len(data['contsi'])
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

#### Objective function
profit = (data['sell_price'] * data['n_steel_quant'] - 
          (pulp.lpSum((data['cost'][k] / 1000) * amount[k] for k in range(K)) + 
          data['melt_price'] * pulp.lpSum(amount[k] for k in range(K)) + 
          data['mang_price'] * num_mang))

problem += profit

#### Constraints
#### Manganese requirement
problem += (pulp.lpSum(data['contmn'][k] * amount[k] for k in range(K)) + num_mang >= 
             (data['mn_percent'] / 100) * data['n_steel_quant'])

#### Silicon content limits
problem += (data['si_min'] <= (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / data['n_steel_quant']))
problem += (pulp.lpSum(data['contsi'][k] * amount[k] for k in range(K)) / data['n_steel_quant'] <= data['si_max'])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

