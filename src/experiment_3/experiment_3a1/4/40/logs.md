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

Let:
\begin{itemize}
    \item \( n \): total tons of steel required
    \item \( mn \): minimum percentage of manganese required in the steel
    \item \( si_{min} \): minimum percentage of silicon required in the steel
    \item \( si_{max} \): maximum percentage of silicon allowed in the steel
    \item \( K \): number of different minerals available
    \item \( contsi_k \): percentage of silicon in mineral \( k \)
    \item \( contmn_k \): percentage of manganese in mineral \( k \)
    \item \( mang\_price \): price of manganese in million euros per ton
    \item \( cost_k \): cost of mineral \( k \) in million euros per thousand tons
    \item \( sell\_price \): selling price of the produced steel in million euros per ton
    \item \( melt\_price \): cost of smelting a ton of mineral in million euros
\end{itemize}

\textbf{Decision Variables}:
\begin{itemize}
    \item \( amount_k \): amount of mineral \( k \) melted (in tons)
    \item \( num\_mang \): amount of manganese added (in tons)
\end{itemize}

\textbf{Objective Function}:
Maximize profit:
\[
Z = n \cdot sell\_price - \left( \sum_{k=1}^{K} ( \frac{cost_k}{1000} \cdot amount_k ) + melt\_price \cdot \sum_{k=1}^{K} amount_k + mang\_price \cdot num\_mang \right)
\]

\textbf{Constraints}:

1. Total quantity of steel produced with respect to manganese:
\[
\frac{\sum_{k=1}^{K} (contmn_k \cdot amount_k) + num\_mang}{n} \geq \frac{mn}{100}
\]

2. Total quantity of steel produced with respect to silicon:
\[
si_{min} \leq \frac{\sum_{k=1}^{K} (contsi_k \cdot amount_k)}{n} \leq si_{max}
\]

3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]
\[
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

Let:
\begin{itemize}
    \item \( n \): total tons of steel required
    \item \( mn \): minimum percentage of manganese required in the steel
    \item \( si_{min} \): minimum percentage of silicon required in the steel
    \item \( si_{max} \): maximum percentage of silicon allowed in the steel
    \item \( K \): number of different minerals available
    \item \( contsi_k \): percentage of silicon in mineral \( k \)
    \item \( contmn_k \): percentage of manganese in mineral \( k \)
    \item \( mang\_price \): price of manganese in million euros per ton
    \item \( cost_k \): cost of mineral \( k \) in million euros per thousand tons
    \item \( sell\_price \): selling price of the produced steel in million euros per ton
    \item \( melt\_price \): cost of smelting a ton of mineral in million euros
\end{itemize}

\textbf{Decision Variables}:
\begin{itemize}
    \item \( amount_k \): amount of mineral \( k \) melted (in tons)
    \item \( num\_mang \): amount of manganese added (in tons)
\end{itemize}

\textbf{Objective Function}:
Maximize profit:
\[
Z = n \cdot sell\_price - \left( \sum_{k=1}^{K} ( \frac{cost_k}{1000} \cdot amount_k ) + melt\_price \cdot \sum_{k=1}^{K} amount_k + mang\_price \cdot num\_mang \right)
\]

\textbf{Constraints}:

1. Total quantity of steel produced with respect to manganese:
\[
\frac{\sum_{k=1}^{K} (contmn_k \cdot amount_k) + num\_mang}{n} \geq \frac{mn}{100}
\]

2. Total quantity of steel produced with respect to silicon:
\[
si_{min} \leq \frac{\sum_{k=1}^{K} (contsi_k \cdot amount_k)}{n} \leq si_{max}
\]

3. Non-negativity constraints:
\[
amount_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]
\[
num\_mang \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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

#### Create the linear programming problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
K = len(data['contsi'])  #### Number of different minerals
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0)  #### Amount of mineral k
num_mang = pulp.LpVariable("num_mang", lowBound=0)  #### Amount of manganese

#### Objective Function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          pulp.lpSum((data['cost'][k] / 1000) * amount_k[k] for k in range(K)) - 
          data['melt_price'] * pulp.lpSum(amount_k[k] for k in range(K)) - 
          data['mang_price'] * num_mang)

problem += profit, "Profit"

#### Constraints
#### Manganese constraint
problem += (pulp.lpSum(data['contmn'][k] * amount_k[k] for k in range(K)) + num_mang) >= data['mn_percent'] * data['n_steel_quant'], "Manganese_Constraint"

#### Silicon constraints
problem += (pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) / data['n_steel_quant']) >= data['si_min'], "Silicon_Min_Constraint"
problem += (pulp.lpSum(data['contsi'][k] * amount_k[k] for k in range(K)) / data['n_steel_quant']) <= data['si_max'], "Silicon_Max_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

