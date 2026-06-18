import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')

class Tariff:
    def __init__(self, name, operator, minutes, gb, sms, price, extra_minute, extra_gb, extra_sms):
        self.name = name
        self.operator = operator
        self.minutes = minutes
        self.gb = gb
        self.sms = sms
        self.price = price
        self.extra_minute = extra_minute
        self.extra_gb = extra_gb
        self.extra_sms = extra_sms

    def calculate_total(self, need_minutes, need_gb, need_sms):
        total = self.price
        if need_minutes > self.minutes:
            total += (need_minutes - self.minutes) * self.extra_minute
        if need_gb > self.gb:
            total += (need_gb - self.gb) * self.extra_gb
        if need_sms > self.sms:
            total += (need_sms - self.sms) * self.extra_sms
        return total

tariffs = [
    Tariff("Смарт", "МТС", 500, 10, 500, 500, 2, 150, 2),
    Tariff("Тарифище", "МТС", 1000, 20, 1000, 800, 1.5, 100, 1.5),
    Tariff("Всё просто", "Билайн", 300, 5, 300, 350, 3, 200, 3),
    Tariff("Максимум", "Билайн", 800, 15, 800, 650, 2, 120, 2),
    Tariff("Стартовый", "Мегафон", 200, 3, 200, 250, 4, 250, 4),
    Tariff("Премиум", "Мегафон", 1200, 30, 1200, 1000, 1, 80, 1),
    Tariff("Лайт", "Tele2", 150, 2, 150, 200, 5, 300, 5),
    Tariff("Безлимитный", "Tele2", 2000, 50, 2000, 1500, 0.5, 50, 0.5),
]

class TariffApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Подбор тарифа мобильной связи")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        title_label = tk.Label(root, text="📱 ПОДБОР ТАРИФА МОБИЛЬНОЙ СВЯЗИ", font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white', pady=15)
        title_label.pack(fill=tk.X)
        
        main_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = tk.Frame(main_frame, bg='white', relief=tk.GROOVE, bd=2, padx=20, pady=20)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_title = tk.Label(left_frame, text="Введите ваши потребности:", font=('Arial', 14, 'bold'), bg='white')
        input_title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')
        
        labels = ["📞 Минуты в месяц:", "🌐 Интернет (ГБ):", "✉️ SMS в месяц:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(left_frame, text=label_text, font=('Arial', 11), bg='white').grid(row=i+1, column=0, sticky='w', pady=10)
            entry = tk.Entry(left_frame, font=('Arial', 11), width=20, relief=tk.SUNKEN, bd=2)
            entry.grid(row=i+1, column=1, pady=10, padx=(20, 0))
            self.entries[label_text] = entry
        
        calc_btn = tk.Button(left_frame, text="🔍 РАССЧИТАТЬ", font=('Arial', 12, 'bold'), bg='#3498db', fg='white', padx=30, pady=10, relief=tk.RAISED, bd=3, cursor='hand2', command=self.calculate)
        calc_btn.grid(row=4, column=0, columnspan=2, pady=30)
        
        reset_btn = tk.Button(left_frame, text="🔄 Очистить", font=('Arial', 10), bg='#e74c3c', fg='white', padx=20, pady=5, relief=tk.RAISED, bd=2, cursor='hand2', command=self.reset)
        reset_btn.grid(row=5, column=0, columnspan=2)
        
        right_frame = tk.Frame(main_frame, bg='white', relief=tk.GROOVE, bd=2, padx=20, pady=20)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        result_title = tk.Label(right_frame, text="📊 РЕЗУЛЬТАТЫ", font=('Arial', 14, 'bold'), bg='white')
        result_title.pack(pady=(0, 10))
        
        self.tree = ttk.Treeview(right_frame, columns=('Тариф', 'Оператор', 'Минуты', 'ГБ', 'SMS', 'Абонплата', 'Итого'), show='headings', height=8)
        columns = [('Тариф', 100), ('Оператор', 80), ('Минуты', 70), ('ГБ', 60), ('SMS', 60), ('Абонплата', 80), ('Итого', 90)]
        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.recommend_label = tk.Label(right_frame, text="🏆 Рекомендация появится здесь", font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50')
        self.recommend_label.pack(pady=(15, 5))
        self.price_label = tk.Label(right_frame, text="", font=('Arial', 11), bg='white', fg='#27ae60')
        self.price_label.pack()
        
        self.graph_frame = tk.Frame(right_frame, bg='white')
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def calculate(self):
        try:
            need_min = int(self.entries["📞 Минуты в месяц:"].get())
            need_gb = float(self.entries["🌐 Интернет (ГБ):"].get())
            need_sms = int(self.entries["✉️ SMS в месяц:"].get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа!")
            return
        
        results = []
        for t in tariffs:
            cost = t.calculate_total(need_min, need_gb, need_sms)
            results.append((t, cost))
        results.sort(key=lambda x: x[1])
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for t, cost in results:
            self.tree.insert('', tk.END, values=(t.name, t.operator, f"{t.minutes}", f"{t.gb}", f"{t.sms}", f"{t.price}", f"{cost:.2f}"))
        
        best_tariff, best_cost = results[0]
        self.recommend_label.config(text=f"🏆 РЕКОМЕНДАЦИЯ: {best_tariff.name} ({best_tariff.operator})", fg='#2c3e50')
        self.price_label.config(text=f"💰 Итоговая стоимость: {best_cost:.2f} руб./мес.", fg='#27ae60')
        self.plot_graph(results)

    def plot_graph(self, results):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        names = [t.name for t, _ in results]
        costs = [c for _, c in results]
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
        
        fig, ax = plt.subplots(figsize=(9, 3.5))
        bars = ax.bar(names, costs, color=colors[:len(names)])
        ax.set_xlabel('Тарифы', fontsize=10)
        ax.set_ylabel('Стоимость (руб.)', fontsize=10)
        ax.set_title('Сравнение тарифов по итоговой стоимости', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        
        for bar, cost in zip(bars, costs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{cost:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        if bars:
            bars[0].set_color('#27ae60')
            bars[0].set_edgecolor('darkgreen')
            bars[0].set_linewidth(2)
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def reset(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.recommend_label.config(text="🏆 Рекомендация появится здесь", fg='#2c3e50')
        self.price_label.config(text="")
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TariffApp(root)
    root.mainloop()