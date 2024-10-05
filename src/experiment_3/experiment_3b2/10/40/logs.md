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
To solve this linear programming problem, we aim to maximize the profit from selling the steel while ensuring it meets the material composition requirements. The profit can be calculated as the revenue from selling the steel minus the cost of the minerals, direct manganese, and smelting costs.

Let's break down the problem and form a mathematical model.

######### Decision Variables:
- \( x_k \): Amount of mineral \( k \) used (in tons) for \( k = 1, \ldots, K \).
- \( M \): Amount of manganese directly added (in tons).

######### Parameters:
- \( n_{\text{steel quant}} \): Total steel quantity required (in tons).
- \( \text{mn percent} \): Minimum percentage of manganese required.
- \( \text{si min} \), \( \text{si max} \): Minimum and maximum percentages of silicon allowed.
- \( \text{contsi}_k \): Percentage of silicon in mineral \( k \).
- \( \text{contmn}_k \): Percentage of manganese in mineral \( k \).
- \( \text{mang price} \): Price of manganese per ton (million euros).
- \( \text{cost}_k \): Cost of mineral \( k \) per thousand tons (million euros).
- \( \text{sell price} \): Selling price of steel per ton (million euros).
- \( \text{melt price} \): Smelting cost per ton (million euros).

######### Objective Function:
Maximize Profit:
\[
\text{Profit} = (\text{sell price} \times n_{\text{steel quant}}) - \left( \sum_{k=1}^{K} \frac{\text{cost}_k}{1000} x_k + \text{mang price} \times M + \text{melt price} \times \sum_{k=1}^{K} x_k \right)
\]

######### Constraints:
1. **Steel Quantity Constraint**:
   \[
   \sum_{k=1}^{K} x_k + M = n_{\text{steel quant}}
   \]
2. **Manganese Content Constraint**:
   \[
   \sum_{k=1}^{K} \text{contmn}_k x_k + M \geq \frac{\text{mn percent}}{100} \times n_{\text{steel quant}}
   \]
3. **Silicon Content Constraints**:
   \[
   \sum_{k=1}^{K} \text{contsi}_k x_k \geq \frac{\text{si min}}{100} \times n_{\text{steel quant}}
   \]
   \[
   \sum_{k=1}^{K} \text{contsi}_k x_k \leq \frac{\text{si max}}{100} \times n_{\text{steel quant}}
   \]
4. **Non-negativity Constraints**:
   \[
   x_k, M \geq 0 \quad \text{for all } k
   \]

The above model can be represented in \(\LaTeX\) as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective Function:}

Maximize Profit:
\[
\text{Profit} = (\text{sell price} \times n_{\text{steel quant}}) - \left( \sum_{k=1}^{K} \frac{\text{cost}_k}{1000} x_k + \text{mang price} \times M + \text{melt price} \times \sum_{k=1}^{K} x_k \right)
\]

\textbf{Subject to the Constraints:}

1. Steel Quantity Constraint:
\[
\sum_{k=1}^{K} x_k + M = n_{\text{steel quant}}
\]

2. Manganese Content Constraint:
\[
\sum_{k=1}^{K} \text{contmn}_k x_k + M \geq \frac{\text{mn percent}}{100} \times n_{\text{steel quant}}
\]

3. Silicon Content Constraints:
\[
\sum_{k=1}^{K} \text{contsi}_k x_k \geq \frac{\text{si min}}{100} \times n_{\text{steel quant}}
\]
\[
\sum_{k=1}^{K} \text{contsi}_k x_k \leq \frac{\text{si max}}{100} \times n_{\text{steel quant}}
\]

4. Non-negativity Constraints:
\[
x_k, M \geq 0 \quad \text{for all } k
\]

\end{document}
```

This model can now be implemented using any optimization solver software to determine the optimal amounts of each mineral to use and the amount of manganese to be added to maximize profit while meeting the compositional requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective Function:}

Maximize Profit:
\[
\text{Profit} = (\text{sell price} \times n_{\text{steel quant}}) - \left( \sum_{k=1}^{K} \frac{\text{cost}_k}{1000} x_k + \text{mang price} \times M + \text{melt price} \times \sum_{k=1}^{K} x_k \right)
\]

\textbf{Subject to the Constraints:}

1. Steel Quantity Constraint:
\[
\sum_{k=1}^{K} x_k + M = n_{\text{steel quant}}
\]

2. Manganese Content Constraint:
\[
\sum_{k=1}^{K} \text{contmn}_k x_k + M \geq \frac{\text{mn percent}}{100} \times n_{\text{steel quant}}
\]

3. Silicon Content Constraints:
\[
\sum_{k=1}^{K} \text{contsi}_k x_k \geq \frac{\text{si min}}{100} \times n_{\text{steel quant}}
\]
\[
\sum_{k=1}^{K} \text{contsi}_k x_k \leq \frac{\text{si max}}{100} \times n_{\text{steel quant}}
\]

4. Non-negativity Constraints:
\[
x_k, M \geq 0 \quad \text{for all } k
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

#### Number of materials
K = len(cost)

#### Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Amount of each material
M = pulp.LpVariable("M", lowBound=0)                  #### Amount of manganese

#### Objective function
profit = (sell_price * n_steel_quant) - (pulp.lpSum([cost[k] / 1000 * x[k] for k in range(K)]) + mang_price * M + melt_price * pulp.lpSum([x[k] for k in range(K)]))
problem += profit

#### Constraints
#### Steel Quantity Constraint
problem += (pulp.lpSum([x[k] for k in range(K)]) + M == n_steel_quant)

#### Manganese Content Constraint
problem += (pulp.lpSum([contmn[k] * x[k] for k in range(K)]) + M >= (mn_percent / 100) * n_steel_quant)

#### Silicon Content Constraints
problem += (pulp.lpSum([contsi[k] * x[k] for k in range(K)]) >= (si_min / 100) * n_steel_quant)
problem += (pulp.lpSum([contsi[k] * x[k] for k in range(K)]) <= (si_max / 100) * n_steel_quant)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

