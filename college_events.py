import random

COLLEGE_TEMPLATES = [
    ("参加书法社团，你的书法作品《骆雯》获得了大家一致的好评", {'情商': lambda: random.randint(1, 3), '智商': lambda: random.randint(0, 2)}),
    ("你努力学习，成绩优异，获得奖学金", {'智商': lambda: random.randint(2, 5), '金钱': lambda: random.randint(2, 3)}),
    ("你因为一点矛盾与同专业学生约架，被打了还被辅导员约谈", {'身体': lambda: random.randint(0, 3), '情商': lambda: random.randint(-3, 0)}),
    ("你买了一块apm32f407，一上手你就觉得你简直就是一个天才程序员", {'金钱': lambda: random.randint(-1, 0), '智商': lambda: random.randint(0, 4)}),
    ("你恋爱了，是同专业的一个女生，你们会一起学习，虽然大多时候你都心不在焉，只想得吃", {'情商': lambda: random.randint(-1, 2)}),
    ("你参加了老师的实验室项目，同学们都夸你厉害", {'智商': lambda: random.randint(1, 4), '金钱': lambda: random.randint(0, 3)}),
    ("你昨天去酒吧happy断片了，第二天头和屁股都痛痛的", {'身体': lambda: random.randint(-2,0), '颜值': lambda: random.randint(-2,0)}),
]

def random_college_event():
    desc, tpl = random.choice(COLLEGE_TEMPLATES)
    effects = {}
    for k, f in tpl.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}
