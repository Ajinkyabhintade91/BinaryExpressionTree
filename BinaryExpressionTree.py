import re
import tkinter as tk
from tkinter import ttk

class Node:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None

def convertToRPN(expression):
    precedence = {'+':1, '-':1, '*':2, '/':2, '%':2}
    output = []
    stack = []

    for token in re.findall(r'\d+|[+\-*/()%]', expression):
        if token.isdigit():
            output.append(token)
        elif token =='(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] !='(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[token] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())
    return output

def rpnToTree(rpn):
    stack = []

    for token in rpn:
        if token.isdigit():
            stack.append(Node(token))
        else:
            right = stack.pop()
            left = stack.pop()
            node = Node(token)
            node.left = left
            node.right = right
            stack.append(node)

    return stack[0]

def printTree(root, level=0, direction="", output=None):
    if output is None:
        output = []
    if not root:
        return
    printTree(root.right, level+1, "/", output)
    print(" " * 4 * level + direction + str(root.value))
    printTree(root.left, level+1, "\\", output)

def main():
    try:
        expression = input("Enter an arithmetic expression: ")
        rpn = convertToRPN(expression)
        print("\n\nReverse Polish Notation is:", " ".join(rpn))

        treeRoot = rpnToTree(rpn)
        print("\n\nIn-order Binary Tree:")
        printTree(treeRoot)
    except Exception as ex:
        print("Error: ", str(ex))

def create_gui():
    def draw_node(canvas, node, x, y, dx):
        if not node:
            return

        canvas.create_text(x, y, text=node.value, anchor=tk.CENTER, font=("Arial", 12))

        if node.left:
            canvas.create_line(x, y + 20, x - dx, y + 40, arrow=tk.LAST)
            draw_node(canvas, node.left, x - dx, y + 40, dx / 2)
        
        if node.right:
            canvas.create_line(x, y + 20, x + dx, y + 40, arrow=tk.LAST)
            draw_node(canvas, node.right, x + dx, y + 40, dx / 2)

    def on_btn_press():
        try:
            expression = expression_entry.get()
            rpn = convertToRPN(expression)
            rpn_output.set(" ".join(rpn))

            treeRoot = rpnToTree(rpn)

            tree_canvas.delete("all")
            draw_node(tree_canvas, treeRoot, tree_canvas.winfo_width() / 2, 10, tree_canvas.winfo_width() / 4)
        except Exception as ex:
            error_output.set(f"Error: {str(ex)}")

    root = tk.Tk()
    root.title("Arithmetic Expression to In-order Binary Tree")

    mainframe = ttk.Frame(root, padding="10")
    mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    expression_label = ttk.Label(mainframe, text="Enter an arithmetic expression:")
    expression_label.grid(column=0, row=0, sticky=tk.W)

    expression_entry = ttk.Entry(mainframe, width=50)
    expression_entry.grid(column=0, row=1, sticky=(tk.W, tk.E))

    calculate_button = ttk.Button(mainframe, text="Draw", command=on_btn_press)
    calculate_button.grid(column=0, row=2, pady="10")

    rpn_output = tk.StringVar()
    rpn_label = ttk.Label(mainframe, text="Reverse Polish Notation:")
    rpn_label.grid(column=0, row=3, sticky=tk.W)
    rpn_result_label = ttk.Label(mainframe, textvariable=rpn_output)
    rpn_result_label.grid(column=0, row=4, sticky=tk.W)

    tree_canvas = tk.Canvas(mainframe, width=400, height=400, bg="white")
    tree_canvas.grid(column=0, row=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    error_output = tk.StringVar()
    error_label = ttk.Label(mainframe, textvariable=error_output, foreground="red")
    error_label.grid(column=0, row=6, sticky=tk.W)

    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=1)

    expression_entry.focus()
    root.mainloop()

if __name__ == "__main__":
    # main()
    create_gui()