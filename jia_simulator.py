import tkinter as tk
from tkinter import messagebox, scrolledtext
import events
import random
import gaokao
import work_events
import college_events


class JiaSimulatorApp:
    def __init__(self, root):
        self.root = root
        #version number
        self.app_version = "0.1.2"
        root.title(f"贾天航模拟器 v{self.app_version}")

        self.max_points = 25
        self.start_age = 0

        self.alloc_vars = {
            '智商': tk.IntVar(value=0),
            '情商': tk.IntVar(value=0),
            '身体': tk.IntVar(value=0),
            '金钱': tk.IntVar(value=0),
            '颜值': tk.IntVar(value=0),
        }
        self.prev_values = {k: 0 for k in self.alloc_vars}
        self.alloc_controls = {}

        self.create_allocation_frame()
        self.create_status_frame()
        self.create_log_frame()

        # redraw bars on resize
        self.root.bind('<Configure>', lambda e: self.on_resize())

        self.college_over_age = None
        self.worker_over_age = None
        #工种：1-工人 2-服务员 3-创业小老板
        self.work = None
        self.character = None

        # quiz storage
        self.quiz_questions = {}
        self.quiz_vars = {}
        self.quiz_subjects = []

    def create_allocation_frame(self):
        frame = tk.LabelFrame(self.root, text="天赋加点（总共25点）")
        frame.grid(row=0, column=0, sticky='nsew', padx=7, pady=7)
        # allow the canvas column to expand
        frame.grid_columnconfigure(2, weight=1)

        row = 0
        for name, var in self.alloc_vars.items():
            tk.Label(frame, text=name).grid(row=row, column=0, padx=4, pady=6)
            plus = tk.Button(frame, text='-', width=4)
            plus.grid(row=row, column=1, padx=2)
            canvas = tk.Canvas(frame, width=150, height=18, bg='gray', highlightthickness=1, relief='sunken')
            canvas.grid(row=row, column=2, padx=4, sticky='we')
            minus = tk.Button(frame, text='+', width=4)
            minus.grid(row=row, column=3, padx=2)
            # bind press/release for continuous change
            plus.bind('<ButtonPress-1>', lambda e, n=name: self.start_repeat(n, -1))
            plus.bind('<ButtonRelease-1>', lambda e, n=name: self.stop_repeat(n))
            minus.bind('<ButtonPress-1>', lambda e, n=name: self.start_repeat(n, 1))
            minus.bind('<ButtonRelease-1>', lambda e, n=name: self.stop_repeat(n))
            self.alloc_controls[name] = {'plus': plus, 'minus': minus, 'canvas': canvas, 'job': None}
            self.draw_bar(name)
            row += 1

        self.rem_label = tk.Label(frame, text=f"剩余点数: {self.max_points}")
        self.rem_label.grid(row=row, column=0, columnspan=4, pady=6)

        self.start_btn = tk.Button(frame, text="开始游戏", command=self.start_game, state='disabled')
        self.start_btn.grid(row=row+1, column=0, columnspan=4, sticky='we', pady=6)

        self.reset_alloc_btn = tk.Button(frame, text="重置加点", command=self.reset_alloc)
        self.reset_alloc_btn.grid(row=row+2, column=0, columnspan=4, sticky='we', pady=2)

    def on_alloc_change_trace(self, name):
        # kept for compatibility if IntVar changed externally
        self.update_all_remain()

    def on_alloc_change(self):
        self.update_all_remain()

    def reset_alloc(self):
        for k, v in self.alloc_vars.items():
            v.set(0)
            self.prev_values[k] = 0
            self.draw_bar(k)
        self.rem_label.config(text=f"剩余点数: {self.max_points}")
        self.start_btn.config(state='disabled')

    def create_status_frame(self):
        frame = tk.LabelFrame(self.root, text="状态")
        frame.grid(row=0, column=1, sticky='nsew', padx=8, pady=8)

        self.age_label = tk.Label(frame, text="年龄: -")
        self.age_label.pack(anchor='w')

        self.attr_labels = {}
        for name in self.alloc_vars:
            lbl = tk.Label(frame, text=f"{name}: -")
            lbl.pack(anchor='w')
            self.attr_labels[name] = lbl

        self.step_btn = tk.Button(frame, text="模拟一年", state='disabled', command=self.simulate_year)
        self.step_btn.pack(fill='x', pady=12)

        self.reset_btn = tk.Button(frame, text='重置游戏', command=self.reset_game, state='disabled')
        self.reset_btn.pack(fill='x', pady=12)

    def create_log_frame(self):
        frame = tk.LabelFrame(self.root, text="事件日志")
        frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=8, pady=8)
        self.log = scrolledtext.ScrolledText(frame, height=15, state='disabled')
        self.log.pack(fill='both', expand=True)

    def start_game(self):
        attrs = {k: self.alloc_vars[k].get() for k in self.alloc_vars}
        self.character = {
            'age': self.start_age,
            '智商': attrs['智商'],
            '情商': attrs['情商'],
            '身体': attrs['身体'],
            '金钱': attrs['金钱'],
            '颜值': attrs['颜值'],
        }
        self.log_message(f"游戏开始：年龄 {self.character['age']}，初始属性：{attrs}")
        self.log_message(f"天地异变，白昼颠倒，随着一道闪电劈开夜空，伴随着道道霞光落于贾府，比极光艳，比霞光美，最后凝聚成一只火龙，龙眼之处射下一道光柱，将躺在床上的婴儿包裹在内，直至天空异象消逝，婴儿儿身上出现若隐若现的龙纹，你就这样出生了，贾天航！")
        self.update_status_labels()
        self.step_btn.config(state='normal')
        self.reset_btn.config(state='normal')
        self.disable_allocation_controls()

    def disable_allocation_controls(self):
        for name, ctrls in self.alloc_controls.items():
            try:
                ctrls['plus'].config(state='disabled')
                ctrls['minus'].config(state='disabled')
            except Exception:
                pass

    def enable_allocation_controls(self):
        for name, ctrls in self.alloc_controls.items():
            try:
                ctrls['plus'].config(state='normal')
                ctrls['minus'].config(state='normal')
            except Exception:
                pass

    def reset_game(self):
        self.character = None
        self.log_message("游戏已重置。")
        self.age_label.config(text="年龄: -")
        for name in self.attr_labels:
            self.attr_labels[name].config(text=f"{name}: -")
        self.reset_alloc()
        self.step_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.enable_allocation_controls()

    def log_message(self, text):
        self.log.config(state='normal')
        self.log.insert('end', text + '\n')
        self.log.see('end')
        self.log.config(state='disabled')

    def update_status_labels(self):
        if not self.character:
            return
        self.age_label.config(text=f"年龄: {self.character['age']}")
        for name in ['智商', '情商', '身体', '金钱', '颜值']:
            self.attr_labels[name].config(text=f"{name}: {self.character[name]}")

    def draw_bar(self, name):
        ctl = self.alloc_controls.get(name)
        if not ctl:
            return
        canvas = ctl['canvas']
        canvas.delete('all')
        # use actual rendered size so bar adapts to layout/resizing
        w = canvas.winfo_width() or int(canvas.cget('width'))
        h = canvas.winfo_height() or int(canvas.cget('height'))
        try:
            w = int(w)
            h = int(h)
        except Exception:
            w, h = 150, 18

        val = int(self.alloc_vars[name].get())
        fill_w = int(w * (val / 100))

        # colors: unfilled background, filled portion (distinct), full bar black
        bg_color = '#e6e6e6'
        fill_color = 'black' if val >= 100 else '#4aa3ff'

        # draw background then filled portion
        canvas.create_rectangle(0, 0, w, h, fill=bg_color, width=0)
        if fill_w > 0:
            canvas.create_rectangle(0, 0, fill_w, h, fill=fill_color, width=0)

        # draw border
        canvas.create_rectangle(0, 0, w-1, h-1, outline='#999', width=1)

        # center the value text
        text_fill = 'white' if val >= 60 else 'black'
        canvas.create_text(w/2, h/2, text=str(val), fill=text_fill, anchor='center')

    def update_all_remain(self):
        total = sum(v.get() for v in self.alloc_vars.values())
        if total > self.max_points:
            messagebox.showwarning("超过上限", f"总点数不能超过 {self.max_points} 点。")
        self.rem_label.config(text=f"剩余点数: {self.max_points - total}")
        self.start_btn.config(state='normal' if total == self.max_points else 'disabled')
        for name in self.alloc_vars:
            self.draw_bar(name)

    def inc_attr(self, name):
        total = sum(v.get() for v in self.alloc_vars.values())
        if total >= self.max_points:
            return
        if self.alloc_vars[name].get() >= 100:
            return
        self.alloc_vars[name].set(self.alloc_vars[name].get() + 1)
        self.update_all_remain()

    def dec_attr(self, name):
        if self.alloc_vars[name].get() <= 0:
            return
        self.alloc_vars[name].set(self.alloc_vars[name].get() - 1)
        self.update_all_remain()

    def start_repeat(self, name, direction):
        # direction: 1 for inc, -1 for dec
        ctl = self.alloc_controls.get(name)
        if not ctl:
            return

        def step():
            if direction > 0:
                total = sum(v.get() for v in self.alloc_vars.values())
                if total < self.max_points and self.alloc_vars[name].get() < 100:
                    self.alloc_vars[name].set(self.alloc_vars[name].get() + 1)
            else:
                if self.alloc_vars[name].get() > 0:
                    self.alloc_vars[name].set(self.alloc_vars[name].get() - 1)
            self.update_all_remain()
            # schedule next
            ctl['job'] = self.root.after(100, step)

        # perform immediate step then schedule
        step()

    def stop_repeat(self, name):
        ctl = self.alloc_controls.get(name)
        if not ctl:
            return
        job = ctl.get('job')
        if job:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        ctl['job'] = None

    def on_resize(self):
        # redraw bars when window resized
        for name in self.alloc_vars:
            self.draw_bar(name)

    def clamp_attrs(self):
        for name in ['智商', '情商', '身体', '金钱', '颜值']:
            self.character[name] = max(0, min(100, int(self.character[name])))

    def simulate_year(self):
        if not self.character:
            return
        # 如果之前在高考后关闭了复读/打工选择框，优先重新弹出该选择（不推进年龄）
        try:
            if self.character.get('awaiting_post_gaokao_choice'):
                try:
                    self.step_btn.config(state='disabled')
                except Exception:
                    pass
                try:
                    gaokao.show_post_gaokao_choice(self)
                except Exception:
                    try:
                        self.step_btn.config(state='normal')
                    except Exception:
                        pass
                return
        except Exception:
            pass
        self.character['age'] += 1
        age = self.character['age']
        ev = None
        #根据年龄触发特定事件

        if age == 1:
            if self.character['智商'] >= 15:
                self.log_message('1岁：你抓周抓到了一块apm32f407，爸爸妈妈说以后你肯定可以成为一个伟大的程序员。')
                self.character['智商'] += 3
            elif self.character['情商'] >= 15:
                self.log_message('1岁：抓周的时候你什么都没有选择，而是亲了爸爸妈妈，爸爸妈妈很高兴。')
                self.character['情商'] += 3
            elif self.character['身体'] >= 15:
                self.log_message('1岁：你体重已经有25kg了，爸爸妈妈希望你以后搞体育。')
                self.character['身体'] += 3
            elif self.character['金钱'] >= 15:
                self.log_message('1岁：你家境优渥，并没有抓周，无论你做什么爸爸妈妈都会支持你。')
                self.character['金钱'] += 3
            elif self.character['颜值'] >= 15:
                self.log_message('1岁：你集齐了爸爸妈妈所有的优点，长相可爱，爸爸妈妈以后想让你做偶像练习生。')
                self.character['颜值'] += 3
            else:
                self.log_message('1岁：抓周的时候你一直傻笑，爸爸妈妈觉得你以后可能会很平凡。')
                # 无显著偏向，给予轻微成长
                self.character['智商'] += 1
                self.character['身体'] += 1

        if age < 5 and age > 1:
            ev = events.random_baby_event()
            self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")

        if age == 5:
            self.log_message('进入小学')
            if self.character['智商'] >= 20:
                self.log_message('5岁：你已经会计算20以内加减法了，爸爸妈妈觉得你以后可能会成为一个学霸。')
                self.character['智商'] += 5
            elif self.character['情商'] >= 20:
                self.log_message('5岁：你已经会在爸爸妈妈不开心时主动关心他们了，爸爸妈妈觉得很欣慰。')
                self.character['情商'] += 5
            elif self.character['身体'] >= 20:
                self.log_message('5岁：你已经会骑自行车了，爸爸妈妈觉得你以后可能会成为一个体育健将。')
                self.character['身体'] += 5
            elif self.character['金钱'] >= 20:
                self.log_message('5岁：你家境优渥，以后可能会成为一个富二代。')
                self.character['金钱'] += 5
            elif self.character['颜值'] >= 20:
                self.log_message('5岁：你长得非常可爱，爸爸妈妈觉得你以后可能会成为一个小明星。')
                self.character['颜值'] += 5
            else:
                self.log_message('5岁：爸爸给你报了兴趣班，但是你总是不认真，每天都想着和伙伴疯玩，爸爸妈妈为你以后的生活担忧。')
                # 无显著偏向，给予轻微成长
                self.character['智商'] += 2
                self.character['身体'] += 2


        if age < 10 and age > 5:
            ev = events.random_kid_event()
            self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")

        if age < 15 and age >= 10:
            ev = events.random_teenager_event()
            self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")   

        if age == 15:
            self.log_message('进入高中')
            if self.character['智商'] >= 28:
                self.log_message('15岁：你在初中已经学会了高一的课程，入学考试取得了年纪第5的成绩。')
                self.character['智商'] += 8
            elif self.character['情商'] >= 28:
                self.log_message('15岁：军训的时候你把同个连队的女生逗得咯咯笑，军训结束后你成了女生们心中的男神。')
                self.character['情商'] += 8
            elif self.character['身体'] >= 28:
                self.log_message('15岁：你在体育方面非常突出，军训的时候你是连队里唯一一个能完成所有项目的男生，军训结束后体育老师让你加入了校田径队。')
                self.character['身体'] += 8
            elif self.character['金钱'] >= 28:
                self.log_message('15岁：爸爸妈妈开豪车来送你上学，校门口的商贩都认识你了，大家都很羡慕你。')
                self.character['金钱'] += 8
            elif self.character['颜值'] >= 28:
                self.log_message('15岁：军训的时候，女同学都不敢和你对视，还收到了8封情书，军训结束后你成了女生们心中的男神。')
                self.character['颜值'] += 8
            else:
                self.log_message('15岁：你开始了平平无奇的高中生活，成绩一般，体育一般，长相一般，既不受同学喜欢也不讨厌。')
                # 无显著偏向，给予轻微成长
                self.character['智商'] += 3
                self.character['身体'] += 3

        if age < 18 and age > 15:
            ev = events.random_high_student_event()
            self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
        if age == 18:
            # 年满18，弹窗选择：若之前未录取选择被关闭则优先重新弹出未录取选择（复读/打工），否则弹出高考或打工的初始抉择
            self.log_message(f"{age}岁：高中毕业，面临选择。")
            # 禁用“模拟一年”按钮，直到做出选择或窗口关闭
            try:
                self.step_btn.config(state='disabled')
            except Exception:
                pass
            # 如果之前在高考后关闭了“复读/打工”对话，优先重新弹出该对话
            if self.character and self.character.get('awaiting_post_gaokao_choice'):
                try:
                    # 不在此处恢复按钮；恢复在对话处理或 on_close 时完成
                    gaokao.show_post_gaokao_choice(self)
                except Exception:
                    try:
                        self.step_btn.config(state='normal')
                    except Exception:
                        pass
            else:
                # 正常的 18 岁初始抉择
                self.handle_age_18()
        path = self.character.get('path') if self.character else None

        # 大学阶段与工作阶段事件基于入学年龄动态计算（支持复读后年龄偏移）
        if path == 'college' and self.character and 'college_start_age' in self.character:
            start = int(self.character['college_start_age'])
            self.college_over_age = start + 4  # 记录大学结束年龄
            # 在大学入学后的 0..3 年（含入学当年）触发大学期事件，四年后毕业
            if age == start:
                self.log_message(f"你进入大学了，开始了全新的生活。")
            if age >= start and age < start + 4:
                ev = college_events.random_college_event()
                self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
        elif path == 'work' and self.character:
            # 若记录了打工起始年龄，则在起始年龄起的若干年内触发对应工作事件（默认 4 年窗口）
            if 'work_start_age' in self.character:
                wstart = int(self.character['work_start_age'])
                self.worker_over_age = wstart + 4  # 记录打工结束年龄
                if age >= wstart and age < wstart + 4:
                    if self.work == 1:
                        ev = work_events.random_worker_event()
                        self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
                    if self.work == 2:
                        ev = work_events.random_sever_event()
                        self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
                    if self.work == 3:
                        ev = work_events.random_boss_event()
                        self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
            else:
                # 未记录起始年龄时，保守策略：在 19-21 岁区间触发旧行为
                self.worker_over_age = 22  # 记录打工结束年龄
                if age > 18 and age < 22:
                    if self.work == 1:
                        ev = work_events.random_worker_event()
                        self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
                    if self.work == 2:
                        ev = work_events.random_sever_event()
                        self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")
                    if self.work == 3:
                        ev = work_events.random_boss_event()
                        self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")

        # 毕业/转行与职业期（将年龄段基于 college_start_age / work_start_age 平移）
        # 计算大学入学/打工起始与职业开始年龄
        career_start = None
        # 大学入学->毕业->职业开始 = college_start_age + 4
        if path == 'college' and self.character and 'college_start_age' in self.character:
            college_start = int(self.character['college_start_age'])
            grad_age = college_start + 4
            # 大学毕业时获得职业机会
            if age == grad_age:
                self.log_message(f"{age}岁：你大学毕业，通过了极嗨维电子公司的面试，成为了一名嵌入式软件工程师。")
                self.character['智商'] += 15
                self.character['情商'] += 15
                self.character['身体'] += 15
                self.character['金钱'] += 15
                self.character['颜值'] += 15
            career_start = grad_age
        # 打工起始 -> 若设定，职业开始视为 work_start_age + 4（与大学毕业同等年限后转正/转行）
        if path == 'work' and self.character and 'work_start_age' in self.character:
            wstart = int(self.character['work_start_age'])
            transfer_age = wstart + 4
            if age == transfer_age:
                self.log_message(f"{age}岁：你厌倦了这个行业，想要转行，通过自学，通过了极嗨维电子公司的面试，成为了一名嵌入式软件工程师。")
                self.character['智商'] += 15
                self.character['情商'] += 15
                self.character['身体'] += 15
                self.character['金钱'] += 15
                self.character['颜值'] += 15
            career_start = transfer_age
        # fallback：若没有任何起始记录则保持原始的 22 作为职业开始基准
        if career_start is None:
            career_start = 22

        # 职业期随机事件：原先为 22-30，现在改为 career_start .. career_start+7
        if career_start <= age < career_start + 8:
            if path in ('college', 'work'):
                ev = events.random_work_event()
                self.log_message(f"{age}岁：{ev['desc']} 影响：{ev['effects']}")

        if age == career_start + 1:
            self.log_message(f"你在极嗨维电子公司工作，认识很多人：庞大，林二，丁三，李四，骆五")

        # 中期标记（原24岁 -> career_start+2）
        if age == career_start + 2:
            if self.character['颜值'] > 50:
                self.log_message(f"{age}岁：遇到欧文。")
            if self.character['情商'] < 50:
                self.log_message(f"{age}岁：与庞大决裂，友情出现裂痕。")

        # 稳定期标记（原30岁 -> career_start+8）
        if age == career_start + 8:
            self.log_message(f"{age}岁：海纳苑买房，事业稳定，生活幸福。")
            self.log_message(f"游戏结束，恭喜你成为幸福的贾天航！")

        # 若本年有随机事件则应用
        if ev:
            self.apply_event(ev)

        self.clamp_attrs()
        self.update_status_labels()

    def goto_age(self):
        if not self.character:
            return
        try:
            target = int(self.goto_entry.get())
        except Exception:
            messagebox.showinfo('输入错误', '请输入合法的整数年龄')
            return
        if target <= self.character['age']:
            messagebox.showinfo('提示', '目标年龄必须大于当前年龄')
            return
        while self.character['age'] < target:
            self.simulate_year()

    def apply_event(self, ev):
        for k, delta in ev['effects'].items():
            if k in self.character:
                self.character[k] += delta

    # 新增：处理18岁选择
    def handle_age_18(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("人生抉择（18岁）")
        dlg.transient(self.root)
        tk.Label(dlg, text="你将面临重要选择：参加高考还是外出打工？").pack(padx=12, pady=10)
        btn_frame = tk.Frame(dlg)
        btn_frame.pack(pady=8)

        def choose_gaokao():
            dlg.destroy()
            self.open_gaokao_quiz()

        def choose_work():
            dlg.destroy()
            self.open_work_choices()

        tk.Button(btn_frame, text="参加高考", width=12, command=choose_gaokao).pack(side='left', padx=8)
        tk.Button(btn_frame, text="外出打工", width=12, command=choose_work).pack(side='left', padx=8)

        def on_close():
            # 如果用户关闭弹窗且未选择，恢复“模拟一年”按钮
            try:
                self.step_btn.config(state='normal')
            except Exception:
                pass
            # 将年龄回退一岁，使得再次点击“模拟一年”会重新触发该选择
            try:
                if self.character and self.character.get('age', 0) >= 18:
                    self.character['age'] -= 1
                    self.update_status_labels()
            except Exception:
                pass
            dlg.destroy()

        dlg.protocol("WM_DELETE_WINDOW", on_close)

    # 高考逻辑已移至独立模块 `gaokao.py`，此处委托给该模块处理
    def open_gaokao_quiz(self):
        try:
            gaokao.open_gaokao_quiz(self)
        except Exception as e:
            try:
                self.step_btn.config(state='normal')
            except Exception:
                pass
            self.log_message(f"无法打开高考模块：{e}")

    # 新增：工人/打工选项窗口（保留原实现），并在窗口关闭/选择后恢复按钮
    def open_work_choices(self):
        # 禁用“模拟一年”按钮直到做出选择或关闭窗口
        try:
            self.step_btn.config(state='disabled')
        except Exception:
            pass

        wwin = tk.Toplevel(self.root)
        wwin.title("外出打工选择")
        wwin.transient(self.root)
        tk.Label(wwin, text="选择打工去向（不同选择有不同剧情与属性变动）：").pack(padx=10, pady=8)

        def choose_factory():
            wwin.destroy()
            self.process_work_choice('工厂')
            self.work = 1
            # mark career path
            if self.character:
                self.character['path'] = 'work'
                # 记录打工起始年龄（支持在复读后选择打工）
                self.character['work_start_age'] = self.character.get('age', 0)
            try:
                self.step_btn.config(state='normal')
            except Exception:
                pass

        def choose_service():
            wwin.destroy()
            self.process_work_choice('服务业')
            self.work = 2
            if self.character:
                self.character['path'] = 'work'
                self.character['work_start_age'] = self.character.get('age', 0)
            try:
                self.step_btn.config(state='normal')
            except Exception:
                pass

        def choose_startup():
            wwin.destroy()
            self.process_work_choice('创业')
            self.work = 3
            if self.character:
                self.character['path'] = 'work'
                self.character['work_start_age'] = self.character.get('age', 0)
            try:
                self.step_btn.config(state='normal')
            except Exception:
                pass

        btnf = tk.Frame(wwin)
        btnf.pack(pady=6)
        tk.Button(btnf, text="工厂（稳定但辛苦）", command=choose_factory, width=25).pack(pady=4)
        tk.Button(btnf, text="服务业（人际关系与情商）", command=choose_service, width=25).pack(pady=4)
        tk.Button(btnf, text="创业（高风险高回报）", command=choose_startup, width=25).pack(pady=4)

        def on_close():
            try:
                self.step_btn.config(state='normal')
            except Exception:
                pass
            wwin.destroy()

        wwin.protocol("WM_DELETE_WINDOW", on_close)

    def process_work_choice(self, choice):
        if choice == '工厂':
            effects = {'身体': -5, '金钱': 15, '颜值': -2}
            msg = "你去工厂打工，劳动辛苦但收入相对稳定。"
        elif choice == '服务业':
            effects = {'情商': 5, '金钱': 8}
            msg = "你进入服务业，情商提升，人脉积累。"
        else:  # 创业
            # 创业有概率成功或失败
            success = random.random() < 0.35 + self.character['智商'] * 0.002
            if success:
                effects = {'金钱': 40, '情商': 3}
                msg = "创业成功，获得可观收入与声誉！"
            else:
                effects = {'金钱': -10, '情商': -3, '身体': -2}
                msg = "创业失败，损失惨重，需要重新开始。"

        for k, v in effects.items():
            if k in self.character:
                self.character[k] += v
        self.log_message(f"选择：{choice}。{msg}（效果：{effects}）")
        self.update_status_labels()


if __name__ == '__main__':
    root = tk.Tk()
    app = JiaSimulatorApp(root)
    root.mainloop()