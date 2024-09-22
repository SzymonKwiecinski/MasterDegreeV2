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
To solve this problem using Linear Programming, we need to formulate an objective function and constraints based on the given data. The objective is to maximize profit, which can be defined as the revenue from selling the steel minus the cost of minerals, the cost of smelting, and the cost of directly added manganese.

Let's denote:
- \( x_k \) as the amount of mineral \( k \) used (in thousand tons).
- \( y \) as the amount of Manganese directly added (in tons).

The profit (\( P \)) is calculated as:

\[ 
P = \text{sell\_price} \times n\_steel\_quant - \sum_{k=1}^{K} \left( \text{cost}_{k} \times x_k \right) - y \times \text{mang\_price} - \sum_{k=1}^{K} \left( \text{melt\_price} \times x_k \right)
\]

**Objective Function:**

Maximize \( P \).

**Constraints:**

1. Total amount of steel produced (in tons):

\[
\sum_{k=1}^{K} \left(1000 \times x_k\right) + y = n\_steel\_quant
\]

2. Manganese content (in tons):

\[
\sum_{k=1}^{K} \left(1000 \times x_k \times \text{contmn}_{k}\right) + y \geq n\_steel\_quant \times \text{mn\_percent}
\]

3. Silicon content:

\[
\text{si\_min} \times n\_steel\_quant \leq \sum_{k=1}^{K} \left(1000 \times x_k \times \text{contsi}_{k}\right) \leq \text{si\_max} \times n\_steel\_quant
\]

4. Non-negativity constraints:

\[
x_k \geq 0, \quad y \geq 0 \quad \text{for all } k
\]

Here's the complete linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize \( P \):

\[
P = \text{sell\_price} \times n\_steel\_quant - \sum_{k=1}^{K} \text{cost}_{k} \times x_k - y \times \text{mang\_price} - \sum_{k=1}^{K} \text{melt\_price} \times x_k
\]

\textbf{Subject to:}

1. Total amount of steel:

\[
\sum_{k=1}^{K} 1000 \times x_k + y = n\_steel\_quant
\]

2. Manganese content:

\[
\sum_{k=1}^{K} 1000 \times x_k \times \text{contmn}_{k} + y \geq n\_steel\_quant \times \text{mn\_percent}
\]

3. Silicon content:

\[
\text{si\_min} \times n\_steel\_quant \leq \sum_{k=1}^{K} 1000 \times x_k \times \text{contsi}_{k} \leq \text{si\_max} \times n\_steel\_quant
\]

4. Non-negativity constraints:

\[
x_k \geq 0, \quad y \geq 0 \quad \text{for all } k
\]

\end{document}
```

This model can be solved using linear programming techniques, such as the Simplex method, to determine the optimal values of \( x_k \) and \( y \) that maximize the profit. The solution will provide the amount of each mineral melted and the amount of Manganese directly added to meet the steel requirements while maximizing profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize \( P \):

\[
P = \text{sell\_price} \times n\_steel\_quant - \sum_{k=1}^{K} \text{cost}_{k} \times x_k - y \times \text{mang\_price} - \sum_{k=1}^{K} \text{melt\_price} \times x_k
\]

\textbf{Subject to:}

1. Total amount of steel:

\[
\sum_{k=1}^{K} 1000 \times x_k + y = n\_steel\_quant
\]

2. Manganese content:

\[
\sum_{k=1}^{K} 1000 \times x_k \times \text{contmn}_{k} + y \geq n\_steel\_quant \times \text{mn\_percent}
\]

3. Silicon content:

\[
\text{si\_min} \times n\_steel\_quant \leq \sum_{k=1}^{K} 1000 \times x_k \times \text{contsi}_{k} \leq \text{si\_max} \times n\_steel\_quant
\]

4. Non-negativity constraints:

\[
x_k \geq 0, \quad y \geq 0 \quad \text{for all } k
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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

#### Number of types of alloys
K = len(data['contsi'])

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f"x{k}", lowBound=0) for k in range(K)]
y = pulp.LpVariable("y", lowBound=0)

#### Objective function
profit = (
    data['sell_price'] * data['n_steel_quant']
    - pulp.lpSum([data['cost'][k] * x[k] for k in range(K)])
    - y * data['mang_price']
    - pulp.lpSum([data['melt_price'] * x[k] for k in range(K)])
)
problem += profit

#### Constraints

#### 1. Total amount of steel
problem += (pulp.lpSum([1000 * x[k] for k in range(K)]) + y == data['n_steel_quant'])

#### 2. Manganese content
problem += (pulp.lpSum([1000 * x[k] * data['contmn'][k] for k in range(K)]) + y >= data['n_steel_quant'] * data['mn_percent'])

#### 3. Silicon content
problem += (data['si_min'] * data['n_steel_quant'] <= pulp.lpSum([1000 * x[k] * data['contsi'][k] for k in range(K)]) <= data['si_max'] * data['n_steel_quant'])

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

