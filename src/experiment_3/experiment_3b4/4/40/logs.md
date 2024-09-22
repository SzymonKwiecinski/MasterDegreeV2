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
To model this problem as a linear programming (LP) problem, we will define the decision variables, constraints, and the objective function to maximize the profit of the foundry.

######### Decision Variables

- \( x_k \): Amount (in thousand tons) of mineral \( k \) melted, for \( k = 1, \ldots, K \).
- \( y \): Amount (in tons) of Manganese directly added.

######### Parameters

- \( n_{\text{steel\_quant}} \): Required amount of steel (in tons).
- \( \text{mn\_percent} \): Minimum percentage of Mn required in the steel.
- \( \text{si\_min} \), \( \text{si\_max} \): Minimum and maximum percentage of Si allowed in the steel.
- \( \text{contsi}_k \): Percentage of Si in mineral \( k \).
- \( \text{contmn}_k \): Percentage of Mn in mineral \( k \).
- \( \text{mang\_price} \): Price per ton of directly added Manganese.
- \( \text{cost}_k \): Cost per thousand tons of mineral \( k \).
- \( \text{sell\_price} \): Sale price per ton of steel.
- \( \text{melt\_price} \): Cost of smelting a ton of mineral.

######### Objective Function

Maximize profit:

\[
\text{Profit} = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} (x_k \cdot (\text{cost}_k + \text{melt\_price})) - y \cdot \text{mang\_price}
\]

######### Constraints

1. **Steel Quantity Constraint**: Total output should meet the steel quantity requirement.

   \[
   \sum_{k=1}^{K} x_k \cdot 1000 + y = n_{\text{steel\_quant}}
   \]

2. **Manganese Content Constraint**: Total Mn in the steel should meet the minimum requirement.

   \[
   \sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contmn}_k}{100}\right) + y \geq n_{\text{steel\_quant}} \cdot \left(\frac{\text{mn\_percent}}{100}\right)
   \]

3. **Silicon Content Constraints**: Total Si in the steel should be within specified bounds.

   \[
   \sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contsi}_k}{100}\right) \geq n_{\text{steel\_quant}} \cdot \left(\frac{\text{si\_min}}{100}\right)
   \]

   \[
   \sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contsi}_k}{100}\right) \leq n_{\text{steel\_quant}} \cdot \left(\frac{\text{si\_max}}{100}\right)
   \]

4. **Non-negativity Constraints**: Non-negativity of decision variables.

   \[
   x_k \geq 0, \quad \text{for all } k
   \]

   \[
   y \geq 0
   \]

######### Complete LaTeX Model

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit in Steel Production}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{Amount (in thousand tons) of mineral } k \text{ melted, for } k = 1, \ldots, K. \\
y & : \text{Amount (in tons) of Manganese directly added.}
\end{align*}

\subsection*{Objective Function}
Maximize the profit:
\begin{align*}
\text{Profit} = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} (x_k \cdot (\text{cost}_k + \text{melt\_price})) - y \cdot \text{mang\_price}
\end{align*}

\subsection*{Constraints}
1. Steel Quantity Constraint:
\begin{align*}
\sum_{k=1}^{K} x_k \cdot 1000 + y &= n_{\text{steel\_quant}}
\end{align*}

2. Manganese Content Constraint:
\begin{align*}
\sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contmn}_k}{100}\right) + y &\geq n_{\text{steel\_quant}} \cdot \left(\frac{\text{mn\_percent}}{100}\right)
\end{align*}

3. Silicon Content Constraints:
\begin{align*}
\sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contsi}_k}{100}\right) &\geq n_{\text{steel\_quant}} \cdot \left(\frac{\text{si\_min}}{100}\right) \\
\sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contsi}_k}{100}\right) &\leq n_{\text{steel\_quant}} \cdot \left(\frac{\text{si\_max}}{100}\right)
\end{align*}

4. Non-negativity Constraints:
\begin{align*}
x_k &\geq 0, \quad \text{for all } k \\
y &\geq 0
\end{align*}

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

\section*{Linear Programming Model for Maximizing Profit in Steel Production}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{Amount (in thousand tons) of mineral } k \text{ melted, for } k = 1, \ldots, K. \\
y & : \text{Amount (in tons) of Manganese directly added.}
\end{align*}

\subsection*{Objective Function}
Maximize the profit:
\begin{align*}
\text{Profit} = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} (x_k \cdot (\text{cost}_k + \text{melt\_price})) - y \cdot \text{mang\_price}
\end{align*}

\subsection*{Constraints}
1. Steel Quantity Constraint:
\begin{align*}
\sum_{k=1}^{K} x_k \cdot 1000 + y &= n_{\text{steel\_quant}}
\end{align*}

2. Manganese Content Constraint:
\begin{align*}
\sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contmn}_k}{100}\right) + y &\geq n_{\text{steel\_quant}} \cdot \left(\frac{\text{mn\_percent}}{100}\right)
\end{align*}

3. Silicon Content Constraints:
\begin{align*}
\sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contsi}_k}{100}\right) &\geq n_{\text{steel\_quant}} \cdot \left(\frac{\text{si\_min}}{100}\right) \\
\sum_{k=1}^{K} x_k \cdot 1000 \cdot \left(\frac{\text{contsi}_k}{100}\right) &\leq n_{\text{steel\_quant}} \cdot \left(\frac{\text{si\_max}}{100}\right)
\end{align*}

4. Non-negativity Constraints:
\begin{align*}
x_k &\geq 0, \quad \text{for all } k \\
y &\geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define the data
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

#### Number of minerals
K = len(data['cost'])

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit_Steel_Production", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

#### Objective function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          pulp.lpSum([x[k] * (data['cost'][k] + data['melt_price']) for k in range(K)]) -
          y * data['mang_price'])

problem += profit

#### Constraints
#### Steel Quantity Constraint
problem += (pulp.lpSum([x[k] * 1000 for k in range(K)]) + y == data['n_steel_quant'])

#### Manganese Content Constraint
problem += (pulp.lpSum([x[k] * 1000 * (data['contmn'][k] / 100) for k in range(K)]) + y >= 
            data['n_steel_quant'] * (data['mn_percent'] / 100))

#### Silicon Content Constraints
problem += (pulp.lpSum([x[k] * 1000 * (data['contsi'][k] / 100) for k in range(K)]) >= 
            data['n_steel_quant'] * (data['si_min'] / 100))

problem += (pulp.lpSum([x[k] * 1000 * (data['contsi'][k] / 100) for k in range(K)]) <= 
            data['n_steel_quant'] * (data['si_max'] / 100))

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

