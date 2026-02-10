import random

# 事件模板放在这里，后续会扩充或从外部加载
BABY_TEMPLATES = [
    ("这一年无事发生，你健康快乐成长", {'智商': lambda: 0, '情商': lambda: 0, '身体': lambda: 0, '金钱': lambda: 0, '颜值': lambda: 0}),
    ("这一年你化身魔丸，每次都将屎拉裤兜，还抹在爸爸妈妈衣服上，爸爸妈妈经常揍你", {'智商': lambda: random.randint(-2,0), '身体': lambda: random.randint(1,3)}),
    ("妈妈每次都抱着你看《偶像练习生》，你看着电视里的唱跳rap的人，叽里哇啦的咯咯笑", {'智商': lambda: random.randint(0,1)}),
    ("这一年爸爸妈妈给你买了很多营养品，你愈发可爱了", {'颜值': lambda: random.randint(1,3), '身体': lambda: random.randint(1,2)}),
    ("这一年爸爸晋升了，给你买了好多玩具", {'情商': lambda: random.randint(0,2), '金钱': lambda: random.randint(0,3)}),
]

KID_TEMPLATES = [
    ("学习成绩取得进步，受到学校表扬", {'智商': lambda: random.randint(1,3), '情商': lambda: random.randint(0,2)}),
    ("因奥特曼卡片与同学发生摩擦", {'情商': lambda: random.randint(-2,0), '身体': lambda: random.randint(1,3)}),
    ("通过兴趣班学会唱歌", {'情商': lambda: random.randint(1,2), '颜值': lambda: random.randint(0,1)}),
    ("随地大小便被同学偷拍发到了班级群", {'情商': lambda: random.randint(-3,0), '颜值': lambda: random.randint(-2,0)}),
    ("与朋友打赌从高处跳下，意外小伤", {'颜值': lambda: random.randint(-2,0)}),
    ("父母工作变动", {'金钱': lambda: random.randint(-3,1)}),
]

Teenager_TEMPLATES = [
    ("努力学习，学习成绩提升明显，获得学校表扬", {'智商': lambda: random.randint(1,5)}),
    ("偷听到同班的女生悄悄议论你，觉得你很讨厌", {'情商': lambda: random.randint(-5,-1), '颜值': lambda: random.randint(-2,0)}),
    ("玩王者荣耀被人骂菜鸡，你与别人对骂了一晚，第二天上课都没有精神", {'智商': lambda: random.randint(-3,0), '情商': lambda: random.randint(-3,0)}),
    ("经常熬夜玩游戏，导致上课睡觉、成绩下滑，被请家长", {'智商': lambda: random.randint(-3,0), '身体': lambda: random.randint(0,3)}),
    ("参加运动会，获得100米冠军", {'身体': lambda: random.randint(1,4), '颜值': lambda: random.randint(0,2)}),
    ("跟妈妈顶嘴，被爸爸打了一顿", {'情商': lambda: random.randint(-2,0), '身体': lambda: random.randint(0,3)}),
    ("偷偷带手机进学校，晚上在宿舍看片，被同学举报，被老师没收手机", {'颜值': lambda: random.randint(-3,0), '身体': lambda: random.randint(-2,0), '情商': lambda: random.randint(-3,0)}),
    ("每天坚持喝豆浆，身体倍棒", {'颜值': lambda: random.randint(1,3), '身体': lambda: random.randint(1,3)}),
]

HIGH_STUDENT_TEMPLATES = [
    ("你喜欢上了同桌的女生，总想着和她说话，但她总是不搭理你", {'颜值': lambda: random.randint(-2,0), '情商': lambda: random.randint(-2,0)}),
    ("努力学习，成绩提升，获得奖学金", {'智商': lambda: random.randint(1,5), '金钱': lambda: random.randint(1,3)}),
    ("偷听到同班的女生议论你：你比隔壁班的班长帅", {'情商': lambda: random.randint(0,2), '颜值': lambda: random.randint(0,4)}),
    ("偷偷带手机进学校，晚上在宿舍看片，被同学举报，被老师没收手机", {'颜值': lambda: random.randint(-3,0), '身体': lambda: random.randint(-2,0), '情商': lambda: random.randint(-3,0)}),
    ("每天坚持喝豆浆，身体倍棒", {'颜值': lambda: random.randint(1,3), '身体': lambda: random.randint(1,3)}),
]

WORKER_TEMPLATES = [
    ("无事发生", {'智商': lambda: 0, '情商': lambda: 0, '身体': lambda: 0, '金钱': lambda: 0, '颜值': lambda: 0}),
    ("职场晋升/项目成功", {'金钱': lambda: random.randint(2,6), '情商': lambda: random.randint(0,2)}),
    ("办公室政治/冲突", {'情商': lambda: random.randint(-3,1)}),
    ("职业培训提升能力", {'智商': lambda: random.randint(0,4)}),
    ("身体管理/健身", {'颜值': lambda: random.randint(1,4)}),
    ("舆论/丑闻影响", {'颜值': lambda: random.randint(-6,-1), '情商': lambda: random.randint(-2,0)}),
    ("家庭开支/意外", {'金钱': lambda: random.randint(-4,1), '身体': lambda: random.randint(-1,0)}),
]

def random_baby_event():
    """返回一个事件字典：{'desc': str, 'effects': {attr: delta}}
    使用lambda构建具体数值，便于后续扩展。"""
    desc, eff_template = random.choice(BABY_TEMPLATES)
    effects = {}
    for k, f in eff_template.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

def random_kid_event():
    desc, eff_template = random.choice(KID_TEMPLATES)
    effects = {}
    for k, f in eff_template.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

def random_teenager_event():
    desc, eff_template = random.choice(Teenager_TEMPLATES)
    effects = {}
    for k, f in eff_template.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

def random_high_student_event():
    desc, eff_template = random.choice(HIGH_STUDENT_TEMPLATES)
    effects = {}
    for k, f in eff_template.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

def random_work_event():
    desc, eff_template = random.choice(WORKER_TEMPLATES)
    effects = {}
    for k, f in eff_template.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

