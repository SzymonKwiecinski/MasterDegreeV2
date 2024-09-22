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
To formulate the problem as a Linear Programming model, we will define the decision variables, objective function, and constraints based on the given information.

######### Decision Variables:
- \( x_k \): the amount (in thousands of tons) of mineral \( k \) used for \( k = 1, \ldots, K \).
- \( y \): the amount (in tons) of Manganese directly added.

######### Objective Function:
Maximize the profit, which is the revenue from selling the steel minus the cost of the minerals, the cost of Manganese added, and the smelting cost.

\[
\text{Maximize} \quad Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \text{cost}_k \times x_k - \text{mang\_price} \times y - \text{melt\_price} \times \sum_{k=1}^{K} x_k
\]

######### Constraints:
1. **Steel Quantity Constraint**:  
   Total weight of minerals and added Manganese must equal the required steel quantity:
   \[
   \sum_{k=1}^{K} x_k + y = \text{n\_steel\_quant}
   \]

2. **Manganese Content Constraint**:  
   The Mn content must be at least the required percentage:
   \[
   \sum_{k=1}^{K} \text{contmn}_k \times x_k + y \geq \frac{\text{mn\_percent}}{100} \times \text{n\_steel\_quant}
   \]

3. **Silicon Content Constraints**:  
   The Si content must be within the specified range:
   \[
   \sum_{k=1}^{K} \text{contsi}_k \times x_k \geq \frac{\text{si\_min}}{100} \times \text{n\_steel\_quant}
   \]
   \[
   \sum_{k=1}^{K} \text{contsi}_k \times x_k \leq \frac{\text{si\_max}}{100} \times \text{n\_steel\_quant}
   \]

4. **Non-negativity Constraints**:  
   \[
   x_k \geq 0 \quad \text{for all} \quad k = 1, \ldots, K
   \]
   \[
   y \geq 0
   \]

Here is the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} \\
Maximize profit, \( Z \):
\[
Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \text{cost}_k \times x_k - \text{mang\_price} \times y - \text{melt\_price} \times \sum_{k=1}^{K} x_k 
\]

\textbf{Subject to constraints:}

1. Total steel quantity:
\[
\sum_{k=1}^{K} x_k + y = \text{n\_steel\_quant}
\]

2. Manganese content:
\[
\sum_{k=1}^{K} \text{contmn}_k \times x_k + y \geq \frac{\text{mn\_percent}}{100} \times \text{n\_steel\_quant}
\]

3. Silicon content:
\[
\frac{\text{si\_min}}{100} \times \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \times x_k \leq \frac{\text{si\_max}}{100} \times \text{n\_steel\_quant}
\]

4. Non-negativity:
\[
x_k \geq 0 \quad \text{for all} \quad k = 1, \ldots, K
\]
\[
y \geq 0
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

\textbf{Objective:} \\
Maximize profit, \( Z \):
\[
Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \text{cost}_k \times x_k - \text{mang\_price} \times y - \text{melt\_price} \times \sum_{k=1}^{K} x_k 
\]

\textbf{Subject to constraints:}

1. Total steel quantity:
\[
\sum_{k=1}^{K} x_k + y = \text{n\_steel\_quant}
\]

2. Manganese content:
\[
\sum_{k=1}^{K} \text{contmn}_k \times x_k + y \geq \frac{\text{mn\_percent}}{100} \times \text{n\_steel\_quant}
\]

3. Silicon content:
\[
\frac{\text{si\_min}}{100} \times \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \times x_k \leq \frac{\text{si\_max}}{100} \times \text{n\_steel\_quant}
\]

4. Non-negativity:
\[
x_k \geq 0 \quad \text{for all} \quad k = 1, \ldots, K
\]
\[
y \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
K = len(data['cost'])
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(K)]  #### Non-negative
y = pulp.LpVariable('y', lowBound=0)  #### Non-negative

#### Objective function
problem += (
    data['sell_price'] * data['n_steel_quant'] 
    - pulp.lpSum(data['cost'][k] * x[k] for k in range(K)) 
    - data['mang_price'] * y 
    - data['melt_price'] * pulp.lpSum(x[k] for k in range(K))
), "Profit"

#### Constraints
#### Total steel quantity constraint
problem += pulp.lpSum(x[k] for k in range(K)) + y == data['n_steel_quant'], "Total_steel_quantity"

#### Manganese content constraint
problem += (
    pulp.lpSum(data['contmn'][k] * x[k] for k in range(K)) + y 
    >= (data['mn_percent'] / 100) * data['n_steel_quant']
), "Manganese_content"

#### Silicon content constraints
problem += (
    pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) 
    >= (data['si_min'] / 100) * data['n_steel_quant']
), "Silicon_min_content"

problem += (
    pulp.lpSum(data['contsi'][k] * x[k] for k in range(K)) 
    <= (data['si_max'] / 100) * data['n_steel_quant']
), "Silicon_max_content"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

