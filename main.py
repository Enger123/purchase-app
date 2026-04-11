import json
from pathlib import Path

class Purchases:
    FILE = "purs.json"
    def __init__(self):
        self.data = self.load_file()

    def load_file(self):
            if Path(self.FILE).is_file():
                try:
                    with open(self.FILE, 'r') as file:
                        return json.load(file)
                except(ValueError, json.JSONDecodeError):
                    return []
            else:
                return []

    def save_file(self):
        with open(self.FILE, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_pur(self):
        new_pur = input("Введіть вашу покупку: ")
        if new_pur.strip() == "":
            print("Помилка: пустий рядок")
            return
        self.data.append({'name': new_pur, 'done': False})
        print("Покупка додана")

    def del_pur(self):
        if not self.show_purs():
            return
        else:
            n_to_del = input("Введіть номер для видалення: ").strip()
            if not n_to_del.isdigit():
                print("Введіть число")
                return
            n_to_del = int(n_to_del)
            if not(1 <= n_to_del <= len(self.data)):
                print("Недоступне значення")
                return
            else:
                del self.data[n_to_del - 1]
                print("Покупку видалено")

    def show_purs(self):
        if not self.data:
            print("Список пустий")
            return False
        else:
            print("Ось список ваших покупок: ")
            for i, el in enumerate(self.data, start=1):
                status = "Yes" if el['done'] else "No"
                print(f"{i}. {el['name']}, {el['done']} - {status}")
            return True

    def sort_purs(self):
        print("Відсортований список покупок: ")
        sorted_list = sorted(self.data, key=lambda x: x['name'])
        for i, el in enumerate(sorted_list, start=1):
            print(f"{i}. {el}")

    def mark_done(self):
        self.show_purs()
        n_to_done = input("Введіть номер покупки для відмітки: ").strip()
        if not n_to_done.isdigit():
            print("Помилка: введіть число")
            return
        n_to_done = int(n_to_done)
        if 1 <= n_to_done <= len(self.data):
            self.data[n_to_done - 1]['done'] = True
            print("Покупка відмічена")
        else:
            print("Помилка: вийдено за межі")

def main():
    purchase = Purchases()
    while True:
        print("\nВиберіть пункт для покупок: ")
        print("1. додати")
        print("2. видалити")
        print("3. показати")
        print("4. відсортувати")
        print("5. відмітити")
        print("0. вийти.")
        choice = input("\nВиберіть пункт меню: ")
        if choice not in ('1', '2', '3', '4', '5', '0'):
            print("Помилка: недоступно в меню")
            continue
        elif choice == '1':
            purchase.add_pur()
            purchase.save_file()
        elif choice == '2':
            purchase.del_pur()
            purchase.save_file()
        elif choice == '3':
            purchase.show_purs()
        elif choice == '4':
            purchase.sort_purs()
        elif choice == '5':
            purchase.mark_done()
            purchase.save_file()
        else:
            break

if __name__ == '__main__':
    main()