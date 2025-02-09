import llm

from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

from lang import score_func, can_be_solution, verifier_feedback

from prompts import prompt, expansion_count, min_lines, check_fun

montecarlo = MonteCarlo(Node(prompt))

def generate_complete(text, montecarlo):
    text = llm.generate(text, 1)[0]
    score = score_func(text)
    if score is not None:
        if score > 0 and can_be_solution(text, min_lines, check_fun):
            montecarlo.solution = text
        return (text, score)
    else:
        return generate_complete(text, montecarlo)

def child_finder(node, montecarlo):
    (text, score) = generate_complete(node.state, montecarlo)
    if score < 0:
        hint = verifier_feedback(node.state, text)
        if not hint:
            node.update_win_value(-1)
            return
        else:
            text = hint

    child = Node(text)
    node.add_child(child)
    child.update_win_value(1)
    child.update_policy_value(1)

    child = Node(node.state)
    node.add_child(child)
    child.update_policy_value(0.2)

montecarlo.child_finder = child_finder

montecarlo.simulate(expansion_count)

print('CHOSEN SOLUTION')
print(montecarlo.solution)

