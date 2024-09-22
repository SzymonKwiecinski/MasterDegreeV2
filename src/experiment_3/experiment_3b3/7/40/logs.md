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
    \item Let \( x_k \) be the amount of mineral \( k \) melted (in tons).
    \item Let \( y \) be the amount of Manganese added (in tons).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( n_{\text{steel\_quant}} \): total tons of steel to be produced
    \item \( mn_{\text{percent}} \): minimum percentage of Manganese in the steel
    \item \( si_{\text{min}}, si_{\text{max}} \): bounds on the percentage of Silicon in the steel
    \item \( contsi_k \): percentage of Silicon in mineral \( k \)
    \item \( contmn_k \): percentage of Manganese in mineral \( k \)
    \item \( mang_{\text{price}} \): price of Manganese (in million euros per ton)
    \item \( cost_k \): cost of mineral \( k \) (in million euros per thousand tons)
    \item \( sell_{\text{price}} \): selling price of steel (in million euros per ton)
    \item \( melt_{\text{price}} \): cost of melting a ton of mineral (in million euros)
\end{itemize}

\textbf{Objective Function:}
Maximize profit:
\[
\text{Maximize } Z = n_{\text{steel\_quant}} \cdot sell_{\text{price}} - \sum_{k=1}^{K} \left( \left(\frac{cost_k}{1000} + melt_{\text{price}}\right) x_k \right) - mang_{\text{price}} \cdot y
\]

\textbf{Constraints:}
\begin{itemize}
    \item Total steel production:
    \[
    \sum_{k=1}^{K} \left( x_k \cdot \frac{contsi_k}{100} \right) + y \geq n_{\text{steel\_quant}} \cdot \frac{si_{\text{min}}}{100}
    \]
    \item Silicon content must be within bounds:
    \[
    \sum_{k=1}^{K} \left( x_k \cdot \frac{contsi_k}{100} \right) + y \leq n_{\text{steel\_quant}} \cdot \frac{si_{\text{max}}}{100}
    \]
    \item Manganese content:
    \[
    \sum_{k=1}^{K} \left( x_k \cdot \frac{contmn_k}{100} \right) + y \geq n_{\text{steel\_quant}} \cdot \frac{mn_{\text{percent}}}{100}
    \]
    \item Non-negativity:
    \[
    x_k \geq 0 \quad \text{for } k = 1,\ldots,K
    \]
    \[
    y \geq 0
    \]
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
    \item Let \( x_k \) be the amount of mineral \( k \) melted (in tons).
    \item Let \( y \) be the amount of Manganese added (in tons).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( n_{\text{steel\_quant}} \): total tons of steel to be produced
    \item \( mn_{\text{percent}} \): minimum percentage of Manganese in the steel
    \item \( si_{\text{min}}, si_{\text{max}} \): bounds on the percentage of Silicon in the steel
    \item \( contsi_k \): percentage of Silicon in mineral \( k \)
    \item \( contmn_k \): percentage of Manganese in mineral \( k \)
    \item \( mang_{\text{price}} \): price of Manganese (in million euros per ton)
    \item \( cost_k \): cost of mineral \( k \) (in million euros per thousand tons)
    \item \( sell_{\text{price}} \): selling price of steel (in million euros per ton)
    \item \( melt_{\text{price}} \): cost of melting a ton of mineral (in million euros)
\end{itemize}

\textbf{Objective Function:}
Maximize profit:
\[
\text{Maximize } Z = n_{\text{steel\_quant}} \cdot sell_{\text{price}} - \sum_{k=1}^{K} \left( \left(\frac{cost_k}{1000} + melt_{\text{price}}\right) x_k \right) - mang_{\text{price}} \cdot y
\]

\textbf{Constraints:}
\begin{itemize}
    \item Total steel production:
    \[
    \sum_{k=1}^{K} \left( x_k \cdot \frac{contsi_k}{100} \right) + y \geq n_{\text{steel\_quant}} \cdot \frac{si_{\text{min}}}{100}
    \]
    \item Silicon content must be within bounds:
    \[
    \sum_{k=1}^{K} \left( x_k \cdot \frac{contsi_k}{100} \right) + y \leq n_{\text{steel\_quant}} \cdot \frac{si_{\text{max}}}{100}
    \]
    \item Manganese content:
    \[
    \sum_{k=1}^{K} \left( x_k \cdot \frac{contmn_k}{100} \right) + y \geq n_{\text{steel\_quant}} \cdot \frac{mn_{\text{percent}}}{100}
    \]
    \item Non-negativity:
    \[
    x_k \geq 0 \quad \text{for } k = 1,\ldots,K
    \]
    \[
    y \geq 0
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parameters
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

#### Initialize the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(len(data['contsi']))]
y = pulp.LpVariable('y', lowBound=0)

#### Objective Function
profit = (data['n_steel_quant'] * data['sell_price'] - 
          sum(((data['cost'][k] / 1000) + data['melt_price']) * x[k] for k in range(len(x))) - 
          data['mang_price'] * y)

problem += profit

#### Constraints
#### Total steel production (Silicon lower bound)
problem += (sum(x[k] * (data['contsi'][k] / 100) for k in range(len(x))) + y 
            >= data['n_steel_quant'] * (data['si_min'] / 100))

#### Silicon content within bounds (Silicon upper bound)
problem += (sum(x[k] * (data['contsi'][k] / 100) for k in range(len(x))) + y 
            <= data['n_steel_quant'] * (data['si_max'] / 100))

#### Manganese content
problem += (sum(x[k] * (data['contmn'][k] / 100) for k in range(len(x))) + y 
            >= data['n_steel_quant'] * (data['mn_percent'] / 100))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

