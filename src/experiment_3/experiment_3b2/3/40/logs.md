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
To solve this problem, we need to formulate a linear programming model to maximize profit while considering the constraints on mineral percentages, manganese percentage and balance constraints. Let's define the decision variables, objective function, and constraints for the model.

**Decision Variables:**
- \( x_k \): Amount of mineral \( k \) used (in tons)
- \( y \): Amount of Manganese added directly (in tons)

**Objective Function:**

Maximize profit given by the revenue from selling the steel minus the costs of minerals, added Manganese, and melting.

\[ \text{Profit} = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times x_k \right) - \text{mang\_price} \times y - \text{melt\_price} \times \text{n\_steel\_quant} \]

**Constraints:**

1. **Balance Constraint:** Total amount of steel produced should be equal to \( \text{n\_steel\_quant} \).

   \[ \sum_{k=1}^{K} x_k + y = \text{n\_steel\_quant} \]

2. **Manganese Constraint:** The percentage of Mn in steel should be at least \(\text{mn\_percent}\).

   \[ \frac{\sum_{k=1}^{K} \text{contmn}_k \times x_k + y}{\text{n\_steel\_quant}} \geq \frac{\text{mn\_percent}}{100} \]

3. **Silicon Constraints:** The percentage of Si in steel should be between \(\text{si\_min}\) and \(\text{si\_max}\).

   \[
   \frac{\text{si\_min}}{100} \times \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \times x_k \leq \frac{\text{si\_max}}{100} \times \text{n\_steel\_quant}
   \]

Let's write this mathematical model in a \( \LaTeX \) format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Objective Function}
\[
\text{Maximize } Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times x_k \right) - \text{mang\_price} \times y - \text{melt\_price} \times \text{n\_steel\_quant}
\]

\subsection*{Constraints}

\begin{align}
& \sum_{k=1}^{K} x_k + y = \text{n\_steel\_quant} \quad & \text{(Balance Constraint)} \\
& \frac{\sum_{k=1}^{K} \text{contmn}_k \times x_k + y}{\text{n\_steel\_quant}} \geq \frac{\text{mn\_percent}}{100} \quad & \text{(Manganese Constraint)} \\
& \frac{\text{si\_min}}{100} \times \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \times x_k \quad & \\
& \sum_{k=1}^{K} \text{contsi}_k \times x_k \leq \frac{\text{si\_max}}{100} \times \text{n\_steel\_quant} \quad & \text{(Silicon Constraints)} \\
& x_k \geq 0, \ y \geq 0 \quad \forall k
\end{align}

\end{document}
```

This mathematical model can be solved using linear programming techniques to determine the optimal amount of each mineral and the amount of Manganese to maximize profit while meeting the required constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Objective Function}
\[
\text{Maximize } Z = \text{sell\_price} \times \text{n\_steel\_quant} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \times x_k \right) - \text{mang\_price} \times y - \text{melt\_price} \times \text{n\_steel\_quant}
\]

\subsection*{Constraints}

\begin{align}
& \sum_{k=1}^{K} x_k + y = \text{n\_steel\_quant} \quad & \text{(Balance Constraint)} \\
& \frac{\sum_{k=1}^{K} \text{contmn}_k \times x_k + y}{\text{n\_steel\_quant}} \geq \frac{\text{mn\_percent}}{100} \quad & \text{(Manganese Constraint)} \\
& \frac{\text{si\_min}}{100} \times \text{n\_steel\_quant} \leq \sum_{k=1}^{K} \text{contsi}_k \times x_k \quad & \\
& \sum_{k=1}^{K} \text{contsi}_k \times x_k \leq \frac{\text{si\_max}}{100} \times \text{n\_steel\_quant} \quad & \text{(Silicon Constraints)} \\
& x_k \geq 0, \ y \geq 0 \quad \forall k
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data_json = '{"n_steel_quant": 1000, "mn_percent": 0.45, "si_min": 3.25, "si_max": 5.0, "contsi": [4.0, 1.0, 0.6], "contmn": [0.45, 0.5, 0.4], "mang_price": 8.0, "cost": [21, 25, 15], "sell_price": 0.45, "melt_price": 0.005}'
data = json.loads(data_json)

#### Variables
K = len(data['contsi'])
sell_price = data['sell_price']
n_steel_quant = data['n_steel_quant']
mang_price = data['mang_price']
melt_price = data['melt_price']
cost = data['cost']
contmn = data['contmn']
contsi = data['contsi']
mn_percent = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]
y = pulp.LpVariable('y', lowBound=0)

#### Objective Function
problem += (sell_price * n_steel_quant 
             - pulp.lpSum((cost[k] / 1000) * x[k] for k in range(K))
             - mang_price * y 
             - melt_price * n_steel_quant), "Total Profit"

#### Constraints
problem += (pulp.lpSum(x[k] for k in range(K)) + y == n_steel_quant, "Balance_Constraint")
problem += ((pulp.lpSum(contmn[k] * x[k] for k in range(K)) + y) / n_steel_quant >= mn_percent / 100, "Manganese_Constraint")
problem += (si_min / 100 * n_steel_quant <= pulp.lpSum(contsi[k] * x[k] for k in range(K)), "Silicon_Constraint_Min")
problem += (pulp.lpSum(contsi[k] * x[k] for k in range(K)) <= si_max / 100 * n_steel_quant, "Silicon_Constraint_Max")

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

