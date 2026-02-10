import tkinter as tk
import random


def open_gaokao_quiz(app):
    try:
        app.step_btn.config(state='disabled')
    except Exception:
        pass

    quiz_subjects = ['语文', '数学', '英语', '生物', '化学', '物理']
    bank = {}

    bank['语文'] = {
        'mc': [
            ("下列哪个词语不是成语？", ["手不释卷", "画龙点睛", "马到成功", "走马观花"], 3),
            ("参差荇菜，左右芼之”中“芼”的意思是？", ["野菜", "采摘", "种植", "观看"], 2),
            ("诗句“梧桐半死清霜后，头白鸳鸯失伴飞。”作者是？", ["贺铸", "苏轼", "王之涣", "丁豪"], 1),
            ("《春江花月夜》的作者是？", ["张若虚", "张柏芝", "王勃", "白居易"], 1),
            ("“落霞与孤鹜齐飞”出自哪类诗？", ["古风", "七言绝句", "五言律诗", "七言律诗"], 2),
        ],
        'fill': [
            ("《出师表》的作者是？", "诸葛亮"),
            ("《三国演义》的作者是？", "罗贯中"),
            ("“曾经沧海难为水，除却巫山不是云”写的是哪种感情？", "爱情"),
            ("“春江花月夜”属于哪一种意象？", "月夜"),
            ("诗句“留取丹青照汗青”的上一句是什么？", "人生自古谁无死"),
        ]
    }

    bank['数学'] = {
        'mc': [
            ("二次函数 y=x^2 的顶点坐标是？", ["(0,0)", "(1,1)", "(-1,1)", "(0,1)"], 1),
            ("若集合A={1,2,3}, B={2,3,4}, A∩B 为？", ["{1}", "{2,3}", "{4}", "{}"], 2),
            ("cos 60° 的值为？", ["1/2", "√2/2", "√3/2", "1"], 1),
            ("若 a*b 表示 a^2 + b^2,则 1*2 等于？", ["1", "3", "5", "4"], 2),
            ("函数 y=sin(x) 的周期为？", ["2π", "π", "π/2", "4π"], 1),
        ],
        'fill': [
            ("二次方程 x^2-5x+6=0 的两个根是？（用空格分隔）", "2 3"),
            ("直角三角形两条直角边为6和8,斜边为多少？", "10"),
            ("若 f(x)=x³+x,判断f(x)的奇偶性", "奇函数"),
            ("若 f(x)=x³+2x+8,则函数的单调性为？", "单调递增"),
            ("平方根符号 √1444 的值为？", "38"),
        ]
    }

    bank['英语'] = {
        'mc': [
            ("单词 'apple' 的中文意思是？", ["香蕉", "苹果", "葡萄", "梨"], 2),
            ("下列句子时态为一般过去时的是？", ["I go to school.", "I went to school.", "I am going.", "I will go."], 2),
            ("Which is a pronoun?", ["table", "he", "blue", "run"], 2),
            ("Choose the correct plural: 'child' -> ?", ["childs", "children", "childes", "child"], 2),
            ("常用问候 'How are you?' 的常见回答是？", ["I am fine.", "Yes, please.", "No, thanks.", "See you."], 1),
        ],
        'fill': [
            ("将 'I am back.' 翻译为中文。", "我回来了"),
            ("单词 'book' 的过去式（若无则写原形）。", "book"),
            ("空格填词：She ___ (be) a teacher yesterday.", "was"),
            ("将 '台风' 翻译为英语", "typhoon"),
            ("常用表示 '谢谢' 的英文短语（小写）", "thank you"),
        ]
    }

    bank['生物'] = {
        'mc': [
            ("细胞的基本单位是？", ["组织", "器官", "细胞", "系统"], 3),
            ("人类遗传物质主要为？", ["蛋白质", "DNA", "糖类", "脂肪"], 2),
            ("光合作用发生在植物的哪个结构？", ["线粒体", "叶绿体", "细胞核", "细胞壁"], 2),
            ("呼吸作用的最终产物不包括？", ["二氧化碳", "水", "氧气", "能量"], 3),
            ("下列哪个是微生物？", ["真菌", "人类", "植物", "动物"], 1),
        ],
        'fill': [
            ("人体中负责运输氧气的细胞是？", "红细胞"),
            ("遗传信息的载体分子是？", "DNA"),
            ("光合作用的主要色素是？", "叶绿素"),
            ("动物体内维持稳定的过程叫？", "稳态"),
            ("基因的基本单位是？", "基因"),
        ]
    }

    bank['化学'] = {
        'mc': [
            ("水的化学式是？", ["H2O", "CO2", "O2", "NaCl"], 1),
            ("酸碱中和会生成什么？", ["盐和水", "气体", "金属", "无变化"], 1),
            ("氧化还原反应中电子会？", ["不动", "转移", "消失", "产生"], 2),
            ("下列物质常温下为气体的是？", ["氯化钠", "氦", "铁", "银"], 2),
            ("pH=7 表示？", ["酸性", "碱性", "中性", "剧烈反应"], 3),
        ],
        'fill': [
            ("化学式 NaCl 的常见名称是？", "食盐"),
            ("元素周期表中第1族为？（如 H 所在族）", "碱金属"),
            ("常用酸：盐酸的化学式是？", "HCl"),
            ("燃烧需要三要素：助燃物、可燃物和什么？", "热源"),
            ("化学反应中不变的总量法则为？", "质量守恒"),
        ]
    }

    bank['物理'] = {
        'mc': [
            ("重力加速度 g 约等于多少？", ["9.8 m/s^2", "3.14 m/s^2", "1 m/s^2", "0"], 1),
            ("电流的单位是？", ["V", "A", "Ω", "W"], 2),
            ("光在同一均匀介质中传播速度为？", ["c", "2c", "c/2", "0"], 1),
            ("牛顿第二定律 F=ma 中 F 单位是什么？", ["N", "J", "W", "Pa"], 1),
            ("声音为哪种波？", ["横波", "纵波", "表面波", "横纵混合波"], 2),
        ],
        'fill': [
            ("速度=位移/什么？", "时间"),
            ("功的单位是？", "焦耳"),
            ("电阻的单位是？", "欧姆"),
            ("频率的单位是？", "Hz"),
            ("光速常用符号为？", "c"),
        ]
    }

    quiz_questions = bank

    quiz_vars = {}
    for subj in quiz_subjects:
        mc_vars = [tk.IntVar(value=0) for _ in range(5)]
        fill_vars = [tk.StringVar(value="") for _ in range(5)]
        quiz_vars[subj] = {'mc': mc_vars, 'fill': fill_vars}

    # 创建答题窗口
    qwin = tk.Toplevel(app.root)
    qwin.title("高考模拟答题（逐科）")
    qwin.transient(app.root)
    qwin.geometry("720x540")

    header = tk.Label(qwin, text="高考模拟：每科 5 选择题 + 5 填空题，答完一科点击“下一科”", wraplength=700)
    header.pack(padx=8, pady=6)

    container = tk.Frame(qwin)
    container.pack(fill='both', expand=True)

    canvas = tk.Canvas(container)
    vbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=vbar.set)
    vbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)

    inner = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=inner, anchor='nw')

    def _on_frame_config(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=inner.winfo_width())

    inner.bind("<Configure>", _on_frame_config)

    def _on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            canvas.yview_scroll(int(event.delta), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", _on_mousewheel)
    canvas.bind_all("<Button-5>", _on_mousewheel)

    current = {'index': 0}

    def show_subject(idx):
        for w in inner.winfo_children():
            w.destroy()
        subj = quiz_subjects[idx]
        tk.Label(inner, text=f"科目：{subj}", font=("Arial", 12, "bold")).pack(anchor='w', padx=8, pady=6)
        mc_list = quiz_questions[subj]['mc']
        for i, (qtext, opts, correct) in enumerate(mc_list):
            f = tk.Frame(inner)
            f.pack(anchor='w', padx=12, pady=3, fill='x')
            tk.Label(f, text=f"{i+1}. {qtext}").pack(anchor='w')
            for o_idx, opt in enumerate(opts, start=1):
                tk.Radiobutton(f, text=opt, variable=quiz_vars[subj]['mc'][i], value=o_idx).pack(anchor='w')
        tk.Label(inner, text="填空题（请在输入框填答案，尽量与标准答案匹配）", fg='blue').pack(anchor='w', padx=8, pady=(6,0))
        fill_list = quiz_questions[subj]['fill']
        for i, (qtext, ans) in enumerate(fill_list):
            ff = tk.Frame(inner)
            ff.pack(anchor='w', padx=12, pady=3, fill='x')
            tk.Label(ff, text=f"{i+1}. {qtext}").pack(anchor='w')
            tk.Entry(ff, textvariable=quiz_vars[subj]['fill'][i], width=80).pack(anchor='w')

        nav = tk.Frame(inner)
        nav.pack(fill='x', pady=8)
        if idx > 0:
            tk.Button(nav, text="上一科", command=lambda: show_subject(idx-1)).pack(side='left', padx=6)
        if idx < len(quiz_subjects)-1:
            tk.Button(nav, text="下一科", command=lambda: show_subject(idx+1)).pack(side='right', padx=6)
        else:
            tk.Button(nav, text="提交试卷并评分", command=lambda: submit_quiz()).pack(side='right', padx=6)

        tk.Label(inner, text=f"进度：{idx+1}/{len(quiz_subjects)}").pack(anchor='e', padx=8)
        canvas.yview_moveto(0)

    def submit_quiz():
        try:
            qwin.destroy()
        except Exception:
            pass
        answers = {}
        for subj in quiz_subjects:
            mc_vals = [v.get() for v in quiz_vars[subj]['mc']]
            fill_vals = [v.get().strip() for v in quiz_vars[subj]['fill']]
            answers[subj] = {'mc': mc_vals, 'fill': fill_vals}
        process_gaokao_result(app, answers)
        # 不在这里恢复按钮；由 process_gaokao_result 根据结果恢复或在选择对话中恢复

    def on_close():
        try:
            app.step_btn.config(state='normal')
        except Exception:
            pass
        qwin.destroy()

    qwin.protocol("WM_DELETE_WINDOW", on_close)
    show_subject(0)


def process_gaokao_result(app, answers):
    # 评分逻辑与属性影响
    subj_scores = {}
    quiz_subjects = ['语文', '数学', '英语', '生物', '化学', '物理']
    for subj in quiz_subjects:
        mc_vals = answers.get(subj, {}).get('mc', [])
        fill_vals = answers.get(subj, {}).get('fill', [])
        mc_correct = sum(1 for v in mc_vals if v != 0)
        fill_correct = sum(1 for v in fill_vals if v.strip() != "")
        mc_score = mc_correct * 8
        fill_score = fill_correct * 12
        subj_score = int(round(mc_score + fill_score))
        subj_scores[subj] = {'score': subj_score, 'mc_correct': mc_correct, 'fill_correct': fill_correct}

    avg_subj = sum(v['score'] for v in subj_scores.values())
    attr_bonus = (app.character['智商'] - 10) * 0.25 + (app.character['身体'] - 10) * 0.05
    noise = random.randint(-15, 15)
    total_score = int(max(0, min(600, avg_subj + attr_bonus + noise)))

    if total_score >= 550:
        uni = "清北大学"
        effects = {'智商': 6, '金钱': 25, '情商': 3}
        msg = f"高考总分：{total_score}，被 {uni} 录取！学术与未来高度优越。"
    elif total_score >= 500:
        uni = "985大学"
        effects = {'智商': 4, '金钱': 15, '情商': 2}
        msg = f"高考总分：{total_score}，被 {uni} 录取，前景很好。"
    elif total_score >= 450:
        uni = "211大学"
        effects = {'智商': 3, '金钱': 8}
        msg = f"高考总分：{total_score}，被 {uni} 录取，继续深造。"
    elif total_score >= 400:
        uni = "普通本科"
        effects = {'智商': 1, '金钱': 4}
        msg = f"高考总分：{total_score}，被 {uni} 录取，努力向上。"
    else:
        uni = "未考上大学"
        effects = {'金钱': 0, '情商': -2}
        msg = f"高考总分：{total_score}，{uni}，需考虑复读或就业路径。"

    for k, v in effects.items():
        if k in app.character:
            app.character[k] += v

    app.log_message("高考成绩详情：")
    for subj, info in subj_scores.items():
        app.log_message(f"  {subj}：{info['score']}分（选择题正确 {info['mc_correct']}/5，填空正确 {info['fill_correct']}/5）")
    app.log_message(msg + f"（效果：{effects}）")
    app.update_status_labels()
    app.log_message("高考经历成为你人生的重要节点。")

    # 若未考上大学，弹出选择：复读 或 打工
    if uni == "未考上大学":
        try:
            dlg = tk.Toplevel(app.root)
            dlg.title("高考结果 - 选择")
            dlg.transient(app.root)
            tk.Label(dlg, text="你未考上大学，选择复读还是去打工？").pack(padx=12, pady=10)
            bf = tk.Frame(dlg)
            bf.pack(pady=8)

            def choose_repeat():
                dlg.destroy()
                # 重新答题
                open_gaokao_quiz(app)

            def choose_work():
                dlg.destroy()
                # 使用新的打工事件模块生成一次随机事件并应用
                try:
                    import work_events
                    ev = work_events.random_work_event()
                    # 标记人生路径为打工
                    app.character['path'] = 'work'
                    # 应用到角色
                    for k, delta in ev['effects'].items():
                        if k in app.character:
                            app.character[k] += delta
                    app.log_message(f"打工时期事件：{ev['desc']} 影响：{ev['effects']}")
                    app.update_status_labels()
                    try:
                        app.step_btn.config(state='normal')
                    except Exception:
                        pass
                except Exception as e:
                    app.log_message(f"触发打工事件失败：{e}")

            tk.Button(bf, text="复读", width=12, command=choose_repeat).pack(side='left', padx=8)
            tk.Button(bf, text="去打工", width=12, command=choose_work).pack(side='left', padx=8)

            def on_close():
                try:
                    app.step_btn.config(state='normal')
                except Exception:
                    pass
                dlg.destroy()

            dlg.protocol("WM_DELETE_WINDOW", on_close)
        except Exception:
            try:
                app.step_btn.config(state='normal')
            except Exception:
                pass
    else:
        # 被大学录取：设置人生路径为 college，并触发一次大学期随机事件
        try:
            app.character['path'] = 'college'
            import college_events
            ev = college_events.random_college_event()
            for k, delta in ev['effects'].items():
                if k in app.character:
                    app.character[k] += delta
            app.log_message(f"大学时期事件：{ev['desc']} 影响：{ev['effects']}")
            app.update_status_labels()
            try:
                app.step_btn.config(state='normal')
            except Exception:
                pass
        except Exception as e:
            app.log_message(f"触发大学事件失败：{e}")
            try:
                app.step_btn.config(state='normal')
            except Exception:
                pass
