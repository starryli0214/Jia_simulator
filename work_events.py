import random

WORKER_TEMPLATES = [
    ("流水线的日子，工作枯燥但收入稳定", {'金钱': lambda: random.randint(5, 8), '身体': lambda: random.randint(-2, 0)}),
    ("遇见厂妹，你们互加了联系方式，互相聊了很久但并没有在一起", {'情商': lambda: random.randint(1, 4), '金钱': lambda: random.randint(-2, 0)}),
    ("你被生产线的线长针对，每个月的奖金都被扣", {'情商': lambda: random.randint(-3, 0), '金钱': lambda: random.randint(-2, 0)}),
    ("操作时不小心将机器弄坏了，赔了一大笔钱", {'金钱': lambda: random.randint(-8, 0), '智商': lambda: random.randint(-3, 0)}),
    ("被同事孤立，感到孤独", {'情商': lambda: random.randint(-3, -1), '身体': lambda: random.randint(-2, 1)}),
]

SEVER_TEMPLATES = [
    ("你总是上错菜，被顾客投诉，被老板批评", {'情商': lambda: random.randint(-4, 0), '智商': lambda: random.randint(-2, 0)}),
    ("服务员的日子，过的美国作息，身体出了很多问题", {'金钱': lambda: random.randint(4, 6), '身体': lambda: random.randint(-3, 0)}),
    ("兼职送外卖，但小电炉被城管没收了", {'身体': lambda: random.randint(-2, 0), '金钱': lambda: random.randint(-2, 0)}),
    ("顾客夸你服务好，给你好评和小费", {'金钱': lambda: random.randint(1, 3), '情商': lambda: random.randint(1, 4)}),
    ("主动留下来加班，老板夸你踏实肯干", {'情商': lambda: random.randint(0, 3), '金钱': lambda: random.randint(0, 3)}),
]

BOSS_TEMPLATES = [
    ("饭局偶遇贵人，得知你公司困难，出手帮助你", {'金钱': lambda: random.randint(5, 12), '情商': lambda: random.randint(0, 3)}),
    ("经济危机，你的产业遭遇了很大的冲击", {'身体': lambda: random.randint(-1, 0), '金钱': lambda: random.randint(-3, 0)}),
    ("这一年你的产业大赚，你心血来潮雇了一个女秘书，相处久了你竟产生了别样的心思，霸王硬上弓不成，被警察约谈", {'情商': lambda: random.randint(-12, -9), '智商': lambda: random.randint(-10, -8)}),
    ("你通过内部消息，抓住了风口，大赚了一笔", {'金钱': lambda: random.randint(8, 15), '智商': lambda: random.randint(4, 7)}),
    ("被竞争对手打压，产业业绩持续下滑", {'智商': lambda: random.randint(-3, -1), '金钱': lambda: random.randint(-5, -3)}),
]

def random_worker_event():
    desc, tpl = random.choice(WORKER_TEMPLATES)
    effects = {}
    for k, f in tpl.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

def random_sever_event():
    desc, tpl = random.choice(SEVER_TEMPLATES)
    effects = {}
    for k, f in tpl.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}

def random_boss_event():
    desc, tpl = random.choice(BOSS_TEMPLATES)
    effects = {}
    for k, f in tpl.items():
        effects[k] = f()
    return {'desc': desc, 'effects': effects}
