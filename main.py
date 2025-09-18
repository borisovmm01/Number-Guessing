import random
from colorama import Fore, Style

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

# Запуск программы
if __name__ == "__main__":
    main()