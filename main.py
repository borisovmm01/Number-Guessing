import random
import tkinter as tk
from tkinter import messagebox, ttk
import random
from colorama import Fore, Style
import threading
try:
    import winsound
    _HAS_WINSOUND = True
except Exception:
    _HAS_WINSOUND = False
try:
    from playsound import playsound
    _HAS_PLAYSOUND = True
except Exception:
    _HAS_PLAYSOUND = False
import wave
import struct
import tempfile
import os
import math

# Процесс игры
def play():
    secret_num = generate_number()
    
    print(f"\n{Fore.CYAN}Число загадано! Попробуй угадать его.{Style.RESET_ALL}")

    attempts = 0
    while True:
        try:
            guess_input = input("Введите 4-значное число: ").strip()
            
            if len(guess_input) != 4 or not guess_input.isdigit():
                print(f"{Fore.RED}Введите ровно 4 цифры!{Style.RESET_ALL}")
                continue

            attempts += 1

            # Проверим, выиграл ли игрок
            if guess_input == secret_num:
                print(f"{Fore.GREEN}🎉 Поздравляем! Вы угадали число {secret_num} за {attempts} попыток!{Style.RESET_ALL}")
                break

            # Подсчёт цветов с учётом повторений
            result_colors = evaluate_guess(guess_input, secret_num)

            # Выводим ответ с цветами
            colored_output = ""
            for char, color in zip(guess_input, result_colors):
                if color == 'green':
                    colored_output += f"{Fore.GREEN}{char}{Style.RESET_ALL}"
                elif color == 'yellow':
                    colored_output += f"{Fore.YELLOW}{char}{Style.RESET_ALL}"
                else:  # red
                    colored_output += f"{Fore.RED}{char}{Style.RESET_ALL}"

            print("Результат: " + colored_output + "\n")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}\nИгра прервана. Загаданное число было: {secret_num}{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
    return secret_num

# Окрашиваем цифры
def evaluate_guess(guess, secret):
    # Создаём списки для меток и подсчёта доступных цифр
    result = ['red'] * 4
    secret_list = list(secret)  # чтобы отмечать использованные цифры

    # Сначала отмечаем зелёные (на своих местах)
    for i in range(4):
        if guess[i] == secret[i]:
            result[i] = 'green'
            secret_list[i] = None  # "используем" эту цифру

    # Теперь жёлтые: цифра есть, но не на своём месте
    for i in range(4):
        if result[i] != 'green':  # если ещё не зелёная
            if guess[i] in secret_list:
                result[i] = 'yellow'
                # "используем" первую подходящую цифру
                secret_list[secret_list.index(guess[i])] = None

    return result

# Выбор игрока
def main():
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}--- МЕНЮ ---")
        print(f"{Fore.GREEN}1. {Fore.YELLOW}Старт")
        print(f"{Fore.GREEN}2. {Fore.LIGHTBLUE_EX}Инфо")
        print(f"{Fore.GREEN}3. {Fore.RED}Выход")
        choice = input(f"{Fore.CYAN}Введите номер действия: {Style.RESET_ALL}")
        # Начало игры
        if choice == "1":
            print(f"{Fore.YELLOW}Вы выбрали: {Fore.LIGHTYELLOW_EX}Старт{Style.RESET_ALL}")
            gues_num = play()
            print(f"{Fore.MAGENTA}Сгенерировано число: {Fore.LIGHTMAGENTA_EX}{gues_num}{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Нажмите Enter или любую клавишу для продолжения...{Style.RESET_ALL}")
        # Информация о игре
        elif choice == "2":
            print(f"{Fore.BLUE}Вы выбрали: {Fore.LIGHTBLUE_EX}Инфо{Style.RESET_ALL}")
            print(f"{Fore.LIGHTWHITE_EX}Это игра, где нужно угадать число от {Fore.GREEN}0{Fore.LIGHTWHITE_EX} до {Fore.RED}9999{Fore.LIGHTWHITE_EX}.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}● Зелёный{Style.RESET_ALL} — правильная цифра на правильном месте.")
            print(f"{Fore.YELLOW}● Жёлтый{Style.RESET_ALL} — цифра есть, но не на своём месте.")
            print(f"{Fore.RED}● Красный{Style.RESET_ALL} — цифры нет в числе.\n")
            input(f"{Fore.CYAN}Нажмите Enter или любую клавишу для продолжения...{Style.RESET_ALL}")
        # Выход из игры
        elif choice == "3":
            print(f"{Fore.RED}Выход из программы...{Style.RESET_ALL}")
            break
        # Обработка ошибок
        else:
            print(f"{Fore.RED}Неверный ввод. Пожалуйста, выберите 1, 2 или 3.{Style.RESET_ALL}")
        print("")

# Генерация числа
def generate_number():
    guessing_number = random.randrange(1000, 10000)
    return str(guessing_number)

# GUI Приложение
class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.geometry("800x700")
        self.root.state('zoomed')  # Полный экран (Windows/Linux)
        self.root.configure(bg="#121212")

        self.secret_num = ""
        self.attempts = 0
        self.guess_history = []
        # fireworks control
        self.fireworks_active = False
        self._firework_after_id = None

        self.setup_ui()

    def setup_ui(self):
    # Холст для фейерверков (на заднем плане)
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.root['bg'])
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        try:
            # Опустить canvas ниже других виджетов; в некоторых версиях Tk требуется аргумент
            self.canvas.lower("all")
        except Exception:
            try:
                self.canvas.lower()
            except Exception:
                pass

    # Состояние фейерверков
        self.fireworks_particles = []
        self.max_fireworks = 6

        # Заголовок
        title = tk.Label(self.root, text="🎯 Угадай число", font=("Helvetica", 24, "bold"),
                         fg="cyan", bg="#1e1e1e")
        title.pack(pady=20)

        # Подзаголовок
        subtitle = tk.Label(self.root, text="Введите 4-значное число и нажмите 'Проверить' или Enter",
                            font=("Arial", 12), fg="lightgray", bg="#1e1e1e")
        subtitle.pack(pady=5)

        # Поле ввода
        self.entry = tk.Entry(self.root, font=("Arial", 18), justify='center', width=10,
                              bg="#333", fg="white", insertbackground="white")
        self.entry.pack(pady=15)
        self.entry.focus()

    # Привязка Enter
        self.entry.bind("<Return>", lambda event: self.check_guess())

        # Кнопки под полем ввода
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=10)

        self.submit_btn = tk.Button(button_frame, text="✅ Проверить", font=("Arial", 12),
                                    bg="#007acc", fg="white", width=12, command=self.check_guess)
        self.submit_btn.grid(row=0, column=0, padx=5)

        info_btn = tk.Button(button_frame, text="ℹ️ Инфо", font=("Arial", 12),
                             bg="#FF9800", fg="white", width=12, command=self.show_info)
        info_btn.grid(row=0, column=1, padx=5)

        exit_btn = tk.Button(button_frame, text="🚪 Выход", font=("Arial", 12),
                             bg="#f44336", fg="white", width=12, command=self.root.quit)
        exit_btn.grid(row=0, column=2, padx=5)

        # Счётчик попыток
        self.attempts_label = tk.Label(self.root, text="Попытки: 0", font=("Arial", 14),
                                       fg="yellow", bg="#1e1e1e")
        self.attempts_label.pack(pady=5)

        # История попыток
        history_title = tk.Label(self.root, text="История попыток:", font=("Arial", 14, "bold"),
                                 fg="white", bg="#1e1e1e")
        history_title.pack(pady=(20, 5))

    # Canvas + Frame для скролла
        self.history_canvas = tk.Canvas(self.root, bg="#1f1f1f", height=200, highlightthickness=0)
        self.history_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.history_canvas.yview)
        self.history_frame = tk.Frame(self.history_canvas, bg="#2a2a2a")

        self.history_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))
        )

        self.history_canvas.create_window((0, 0), window=self.history_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)

        self.history_canvas.pack(side="top", fill="both", expand=True, padx=40, pady=5)
        self.history_scrollbar.pack(side="right", fill="y")

    # --- Панель информации (встроенная) ---
        self.info_frame = tk.Frame(self.root, bg="#254", bd=2, relief="solid")
        info_text = (
            " 🎯 Угадайте 4-значное число от 1000 до 9999\n\n"
            " 🟢 Зелёный — цифра на своём месте\n"
            " 🟡 Жёлтый — цифра есть, но не на своём месте\n"
            " 🔴 Красный — цифры нет в числе\n"
        )
        self.info_label = tk.Label(
            self.info_frame,
            text=info_text,
            font=("Arial", 11),
            fg="#b8f6d6",
            bg="#1f1f1f",
            justify="left",
            anchor="w",
            padx=15,
            pady=10
        )
        self.info_label.pack()
        self.info_frame.pack_forget()  # Скрыто изначально

    # Кнопка "Новая игра"
        self.restart_btn = tk.Button(self.root, text="🔄 Новая игра", font=("Arial", 12),
                                     bg="#555", fg="white", width=20, command=self.start_game)
        self.restart_btn.pack(pady=10)
        self.restart_btn.pack_forget()  # Скрыта до победы
        self.start_game()

    def start_game(self):
        self.secret_num = generate_number()
        self.attempts = 0
        self.guess_history = []
        self.attempts_label.config(text="Попытки: 0")
        self.entry.delete(0, tk.END)
        self.clear_history_display()
        self.submit_btn.config(state=tk.NORMAL)
        # Stop fireworks from previous round (if any)
        self.restart_btn.pack_forget()
        self.fireworks_active = False
        if getattr(self, '_firework_after_id', None):
            try:
                self.root.after_cancel(self._firework_after_id)
            except Exception:
                pass
            self._firework_after_id = None
        # remove leftover particles
        for p in list(getattr(self, 'fireworks_particles', [])):
            try:
                self.canvas.delete(p['id'])
            except Exception:
                pass
        self.fireworks_particles = []
        # hide history canvas/scrollbar so no gray block remains
        try:
            self.history_canvas.pack_forget()
            self.history_scrollbar.pack_forget()
        except Exception:
            pass
        self.entry.focus()
        print(f"[DEBUG] Загадано: {self.secret_num}")

    def clear_history_display(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

    def check_guess(self):
        guess_input = self.entry.get().strip()

        if len(guess_input) != 4 or not guess_input.isdigit():
            self.entry.delete(0, tk.END)
            self.entry.focus()
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Попытки: {self.attempts}")

        self.guess_history.append(guess_input)

        if guess_input == self.secret_num:
            self.win()
            return

        colors = evaluate_guess(guess_input, self.secret_num)
        self.display_result_in_history(guess_input, colors)
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def display_result_in_history(self, guess, colors):
    # убедиться, что панель истории и скроллбар видимы
        try:
            if not self.history_canvas.winfo_ismapped():
                self.history_canvas.pack(side="top", fill="both", expand=True, padx=40, pady=5)
                self.history_scrollbar.pack(side="right", fill="y")
        except Exception:
            pass
        colors_map = {
            'green': '#4CAF50',
            'yellow': '#FFD700',
            'red': '#F44336'
        }

        attempt_frame = tk.Frame(self.history_frame, bg="#2a2a2a")
        attempt_frame.pack(pady=4, anchor="w", padx=10)

        num_label = tk.Label(attempt_frame, text=f"{len(self.guess_history)}. {guess} → ",
                             font=("Courier", 12), fg="lightblue", bg="#2a2a2a")
        num_label.pack(side=tk.LEFT)

        color_frame = tk.Frame(attempt_frame, bg="#2a2a2a")
        color_frame.pack(side=tk.LEFT)

        for char, color in zip(guess, colors):
            label = tk.Label(color_frame, text=char, font=("Courier", 14, "bold"),
                             bg=colors_map[color], fg="white", width=2, height=1)
            label.pack(side=tk.LEFT, padx=1)

    def win(self):
        self.submit_btn.config(state=tk.DISABLED)
        self.display_result_in_history(self.secret_num, ['green'] * 4)
        self.restart_btn.pack()

    # Воспроизвести звук победы в фоновом потоке
        if _HAS_WINSOUND:
            threading.Thread(target=self.play_victory_sound, daemon=True).start()

        # Launch fireworks animation
        self.start_fireworks()

    # без всплывающего окна: только четыре зелёных квадрата в истории и запуск фейерверков/звука

    def play_victory_sound(self):
        # Проигрываем victory.mp3
        try:
            mp3_path = os.path.join(os.path.dirname(__file__), 'victory.mp3')
            if _HAS_PLAYSOUND and os.path.exists(mp3_path):
                # play in background thread 
                threading.Thread(target=lambda: playsound(mp3_path), daemon=True).start()
                return
        except Exception:
            pass

    # В крайнем случае, если доступен winsound, воспроизвести тихие звуковые сигналы
        if _HAS_WINSOUND:
            try:
                winsound.Beep(880, 120)
                winsound.Beep(1047, 200)
            except Exception:
                pass

    def start_fireworks(self):
        """Запускать фейерверки непрерывно до начала новой игры."""
        if self.fireworks_active:
            return
        self.fireworks_active = True

        def spawn():
            if not self.fireworks_active:
                return
            w = self.root.winfo_width() or 800
            h = self.root.winfo_height() or 600
            x = random.randint(100, max(150, w - 100))
            y = random.randint(80, max(120, h // 3))
            color = f"#{random.randint(100,255):02x}{random.randint(100,255):02x}{random.randint(100,255):02x}"
            self.launch_firework(x, y, color)
            # schedule next spawn
            self._firework_after_id = self.root.after(random.randint(300, 900), spawn)

        spawn()

    def launch_firework(self, x, y, color):
        """Создать простой взрыв частиц и анимировать их."""
        particles = []
        count = 30
        for _ in range(count):
            dx = random.uniform(-6, 6)
            dy = random.uniform(-6, 6)
            size = random.randint(3, 6)
            pid = self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)
            particles.append({'id': pid, 'dx': dx, 'dy': dy, 'life': random.randint(12, 26)})

        self.fireworks_particles.extend(particles)
        # анимация (запустить цикл анимации, если он ещё не запущен)
        self.animate_fireworks()

    def animate_fireworks(self):
        if not self.fireworks_particles:
            return
        to_remove = []
        for p in list(self.fireworks_particles):
            try:
                self.canvas.move(p['id'], p['dx'], p['dy'])
            except Exception:
                continue
            # gravity effect
            p['dy'] += 0.2
            p['dx'] *= 0.98
            p['dy'] *= 0.98
            p['life'] -= 1
            if p['life'] <= 0:
                try:
                    self.canvas.delete(p['id'])
                except Exception:
                    pass
                try:
                    self.fireworks_particles.remove(p)
                except ValueError:
                    pass

        if self.fireworks_particles:
            self.root.after(40, self.animate_fireworks)

    def show_info(self):
        if self.info_frame.winfo_ismapped():
            self.info_frame.pack_forget()
        else:
            self.info_frame.pack(pady=10)
        self.entry.focus()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()