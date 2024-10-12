import pandas as pd
from bs4 import BeautifulSoup
import re
from openpyxl import load_workbook

# 指定HTML文件路径
html_file_path = r'C:\Users\ASUS\Desktop\葫芦侠\e.html'

# 指定输出Excel文件路径
output_excel_path = r'C:\Users\ASUS\Desktop\葫芦侠\习题.xlsx'

# 读取HTML文件内容
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有题目元素，假设它们的class包括"mark_name colorDeep"
question_elements = soup.find_all(class_="mark_name colorDeep")
# 找到所有答案元素，假设它们的class包括"mark_letter colorDeep"
answer_elements = soup.find_all(class_="mark_letter colorDeep")

# 找到所有用户答案元素，假设它们在<span>标签内，并且<span>包含<i>标签
# 这里我们查找所有包含class "fontWeight custom-style"的<i>标签
user_answer_elements = soup.find_all('div', class_='mark_answer')


# 定义处理题目文本的函数
def process_question_text(question):
    # 查找<h3>下的<u>标签并替换其内容为括号
    for u_tag in question.find_all('u'):
        u_tag.string = '（）'
    # 返回处理后的question.text
    return question.get_text()


# 初始化一个列表来存储题目、答案和用户的答案
questions_and_answers = []


def process_answer(answer_text):
    result = ""
    i = 0
    while i < len(answer_text):
        if answer_text[i] in {'B', 'C', 'D'}:
            result += '屎'
        result += answer_text[i]
        i += 1
    return result
# 遍历题目、答案和用户答案元素
index = 0
for question in question_elements:
    # 尝试从当前用户答案元素中提取答案
    user_answer = ''
    if index < len(user_answer_elements):
        # 在每个mark_answer div中找到包含fontWeight custom-style的<i>标签
        i_tag = user_answer_elements[index].find('i', class_='fontWeight custom-style')
        if i_tag:
            # 获取<i>标签后面的直接兄弟节点文本
            user_answer = i_tag.next_sibling.strip()

# for question in question_elements:
#     # 尝试从当前用户答案元素中提取答案
#     user_answer = ''
#     if index < len(user_answer_elements):
#         # 获取当前mark_answer div中的第1个span标签
#         span_tag = user_answer_elements[index].find('span', class_='element-invisible-hidden colorDeep marginRight40 fl')
#         if span_tag:
#             # 获取<span>标签的文本内容，并去除冒号和分号
#             user_answer = re.sub(r'^[^:]*:|;$', '', span_tag.get_text(strip=True)).strip()
    
    # 提取题目文本
    question_text = process_question_text(question)
    
    # 假设答案列表与题目一一对应
    # 假设答案列表与题目一一对应
    answer_text = process_answer(answer_elements[index].get_text(strip=True)) if index < len(answer_elements) else ''
    
    # 将题目、答案和用户的答案作为字典添加到列表中
    questions_and_answers.append({
        '题目': question_text,
        '答案': answer_text,
        '用户答案': user_answer
    })
    
    # 更新索引
    index += 1

# 使用pandas创建DataFrame
df = pd.DataFrame(questions_and_answers)

# 将DataFrame写入Excel文件
df.to_excel(output_excel_path, index=False, header=True, engine='openpyxl')

print("题目和答案已保存到", output_excel_path)