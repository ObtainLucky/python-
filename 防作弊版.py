import tkinter as tk
from tkinter import font, messagebox
import pandas as pd

excel_file_path = '题库.xlsx'

current_question_index = 0

root = tk.Tk()
root.title("习思想答题")
custom_font_style = font.Font(family='黑体', weight='bold', size=20)


def load_questions():
    global questions_df
    try:
        questions_df = pd.read_excel(excel_file_path)
        if '问题' in questions_df.columns and '选项' in questions_df.columns and '答案' in questions_df.columns:
            show_question()
        else:
            messagebox.showerror("错误", "Excel文件格式不正确，请确保包含'问题'、'选项'、'答案'列。")
    except Exception as e:
        messagebox.showerror("错误", f"读取Excel文件时发生错误: {str(e)}")


def show_question():
    global current_question_index
    if 0 <= current_question_index < len(questions_df):
        question_text.set(questions_df.loc[current_question_index, '问题'])
        options = questions_df.loc[current_question_index, '选项'].split('\n')
        for idx, (option_var, option_widget) in enumerate(zip(option_vars, option_widgets)):
            option_var.set(False)  # 重置选项状态
            option_widget.config(text=options[idx], variable=option_var, font=custom_font_style)
        # prev_button.config(state=tk.NORMAL if current_question_index > 0 else tk.DISABLED)
        next_button.config(state=tk.NORMAL)  # 确保下一题按钮启用
    else:
        messagebox.showinfo("完成", "所有问题已完成。")


def map_selection_to_answer(selections, options):
    """将选项索引映射回选项字母"""
    return ','.join(options[idx - 1][0] for idx in selections if 1 <= idx <= len(options))


score = 0
# 在全局变量部分添加一个用于显示分数的StringVar
score_var = tk.StringVar()
score_var.set("得分: 0")

# 在界面布局部分添加分数显示标签
score_label = tk.Label(root, textvariable=score_var, font=custom_font_style, fg='green')
score_label.pack(side=tk.TOP, pady=(0, 20))  # 根据需要调整位置


# 修改check_answer函数
def check_answer():
    global current_question_index, score
    selected_indices = [idx + 1 for idx, var in enumerate(option_vars) if var.get()]
    user_answer_str = map_selection_to_answer(selected_indices,
                                              questions_df.loc[current_question_index, '选项'].split('\n'))
    user_answers_set = set(user_answer_str.split(','))
    correct_answers = set(questions_df.loc[current_question_index, '答案'].replace(' ', '').split(','))
    
    if user_answers_set == correct_answers:
        score += 1
        current_question_index += 1
    else:
        score -= 0
    
    # 更新分数显示并跳转到下一题或显示完成信息
    score_var.set(f"得分: {score}")
    
    if user_answers_set != correct_answers:
        messagebox.showinfo("结果", f"回答错误。正确答案是: {', '.join(correct_answers)}")
        current_question_index += 1
    if current_question_index < len(questions_df):
        show_question()
    else:
        messagebox.showinfo("完成", "所有问题已完成。")
        submit_button.config(state=tk.DISABLED)  # 所有问题完成后禁用提交按钮


# 修改go_to_previous_question函数以在返回上一题后更新分数显示
def go_to_previous_question():
    global current_question_index, score
    if current_question_index > 0:
        current_question_index -= 1
        show_question()
        score_var.set(f"得分: {score}")  # 更新分数显示


def go_to_next_question():
    global current_question_index
    current_question_index += 1
    show_question()


def on_closing():
    if messagebox.askokcancel("退出", "确定要退出吗?"):
        root.destroy()


question_text = tk.StringVar()
question_label = tk.Label(root, textvariable=question_text, wraplength=400, justify='left', font=custom_font_style,
                          fg='blue')
question_label.pack(pady=20)

option_vars = [tk.BooleanVar() for _ in range(4)]
option_widgets = []
for idx, var in enumerate(option_vars):
    checkbox = tk.Checkbutton(root, variable=var, padx=300, pady=10)  # 这里添加了padx和pady
    checkbox.pack(anchor=tk.W)
    option_widgets.append(checkbox)

# prev_button = tk.Button(root, text="上一题", command=go_to_previous_question, state=tk.DISABLED, font=custom_font_style)
# prev_button.pack(side=tk.LEFT, padx=10, pady=10)

next_button = tk.Button(root, text="下一题", command=go_to_next_question, state=tk.DISABLED, font=custom_font_style)
next_button.pack(side=tk.RIGHT, padx=100, pady=10)

submit_button = tk.Button(root, text="提交", command=check_answer, font=custom_font_style)
submit_button.pack(side=tk.LEFT, padx=350, pady=10)

load_questions()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

