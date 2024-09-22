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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_k \) be the amount (in tons) of mineral \( k \) melted, for \( k = 1, \ldots, K \).
    \item Let \( y \) be the amount (in tons) of manganese added directly.
\end{itemize}

\textbf{Objective Function:}

The objective is to maximize profit, which can be expressed as:
\[
\text{Maximize } Z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} x_k \cdot \text{cost}_k \cdot 1000 - y \cdot \text{mang\_price} - \sum_{k=1}^{K} x_k \cdot \text{melt\_price}
\]

\textbf{Constraints:}

1. Total weight of steel produced must equal the order quantity:
\[
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\]

2. Manganese content constraint:
\[
\frac{\sum_{k=1}^{K} x_k \cdot \left( \frac{\text{contmn}_k}{100} \right) + y}{n_{\text{steel\_quant}}} \geq \frac{mn_{\text{percent}}}{100}
\]
This can be rearranged to:
\[
\sum_{k=1}^{K} x_k \cdot \text{contmn}_k + 100y \geq n_{\text{steel\_quant}} \cdot mn_{\text{percent}}
\]

3. Silicon content constraints:
\[
\sum_{k=1}^{K} x_k \cdot \left( \frac{\text{contsi}_k}{100} \right) \geq n_{\text{steel\_quant}} \cdot si_{\text{min}}
\]
\[
\sum_{k=1}^{K} x_k \cdot \left( \frac{\text{contsi}_k}{100} \right) \leq n_{\text{steel\_quant}} \cdot si_{\text{max}}
\]

4. Non-negativity constraints:
\[
x_k \geq 0 \quad \forall k \in \{1, \ldots, K\}
\]
\[
y \geq 0
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{amount} = [x_1, x_2, \ldots, x_K] \)
    \item \( \text{num\_mang} = y \)
\end{itemize}

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

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_k \) be the amount (in tons) of mineral \( k \) melted, for \( k = 1, \ldots, K \).
    \item Let \( y \) be the amount (in tons) of manganese added directly.
\end{itemize}

\textbf{Objective Function:}

The objective is to maximize profit, which can be expressed as:
\[
\text{Maximize } Z = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} x_k \cdot \text{cost}_k \cdot 1000 - y \cdot \text{mang\_price} - \sum_{k=1}^{K} x_k \cdot \text{melt\_price}
\]

\textbf{Constraints:}

1. Total weight of steel produced must equal the order quantity:
\[
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\]

2. Manganese content constraint:
\[
\frac{\sum_{k=1}^{K} x_k \cdot \left( \frac{\text{contmn}_k}{100} \right) + y}{n_{\text{steel\_quant}}} \geq \frac{mn_{\text{percent}}}{100}
\]
This can be rearranged to:
\[
\sum_{k=1}^{K} x_k \cdot \text{contmn}_k + 100y \geq n_{\text{steel\_quant}} \cdot mn_{\text{percent}}
\]

3. Silicon content constraints:
\[
\sum_{k=1}^{K} x_k \cdot \left( \frac{\text{contsi}_k}{100} \right) \geq n_{\text{steel\_quant}} \cdot si_{\text{min}}
\]
\[
\sum_{k=1}^{K} x_k \cdot \left( \frac{\text{contsi}_k}{100} \right) \leq n_{\text{steel\_quant}} \cdot si_{\text{max}}
\]

4. Non-negativity constraints:
\[
x_k \geq 0 \quad \forall k \in \{1, \ldots, K\}
\]
\[
y \geq 0
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{amount} = [x_1, x_2, \ldots, x_K] \)
    \item \( \text{num\_mang} = y \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
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

#### Set up the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Variables
K = len(data['cost'])
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Amount of mineral k melted
y = pulp.LpVariable("y", lowBound=0)  #### Amount of manganese added

#### Objective Function
profit = data['n_steel_quant'] * data['sell_price'] - \
         pulp.lpSum(x[k] * data['cost'][k] * 1000 for k in range(K)) - \
         y * data['mang_price'] - \
         pulp.lpSum(x[k] * data['melt_price'] for k in range(K))

problem += profit, "Total_Profit"

#### Constraints
#### 1. Total weight of steel produced must equal the order quantity
problem += pulp.lpSum(x[k] for k in range(K)) + y == data['n_steel_quant'], "Steel_Weight_Constraint"

#### 2. Manganese content constraint
problem += pulp.lpSum(x[k] * data['contmn'][k] for k in range(K)) + 100 * y >= data['n_steel_quant'] * data['mn_percent'], "Manganese_Content_Constraint"

#### 3. Silicon content constraints
problem += pulp.lpSum(x[k] * data['contsi'][k] for k in range(K)) >= data['n_steel_quant'] * data['si_min'], "Silicon_Min_Constraint"
problem += pulp.lpSum(x[k] * data['contsi'][k] for k in range(K)) <= data['n_steel_quant'] * data['si_max'], "Silicon_Max_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
amount = [pulp.value(x[k]) for k in range(K)]
num_mang = pulp.value(y)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Amount of minerals melted: {amount}')
print(f'Amount of manganese added: {num_mang}')
```

