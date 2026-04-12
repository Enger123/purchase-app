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
        with open(self.FILE, 'w', encoding='utf-8') as file:
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
                print(f"{i}. {el['name'].capitalize()}, done - {status}")
            return True

    def sort_purs(self):
        print("Відсортований список покупок: ")
        sorted_list = sorted(self.data, key=lambda x: x['name'])
        for i, el in enumerate(sorted_list, start=1):
            status = "Yes" if el['done'] else "No"
            print(f"{i}. {el['name'].capitalize()}, done - {status}")

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

    def search_pur(self):
        word = input("Введіть слово (для показу покупок з цим словом): ").strip().lower()
        found = False
        for el in self.data:
            if word in el['name'].lower():
                found = True
                status = "Yes" if el['done'] else "No"
                print(f"{el['name'].capitalize()} done - {status}")
        if not found:
            print("Нічого не знайдено за цим словом")


    def edit_pur(self):
        if not self.show_purs():
            return
        else:
            n_to_edit = input("Введіть номер покупки для редагування: ").strip()
            if not n_to_edit.isdigit():
                print("Номер повинен бути цифрою")
                return
            n_to_edit = int(n_to_edit)
            if 1 <= n_to_edit <= len(self.data):
                new_pur = input("Введіть нову покупку: ").strip()
                status = input("Статус done (1-True, 2-False): ").strip()
                if new_pur.strip() == "" or status.strip() == "" or status not in ('1', '2'):
                    print("Дані не записано, пустий рядок або статус введений невірно")
                    return
                self.data[n_to_edit - 1]['name'] = new_pur
                if status == '1':
                    self.data[n_to_edit - 1]['done'] = True
                else:
                    self.data[n_to_edit - 1]['done'] = False
                print("Покупку змінено.")
            else:
                print("Немає такого номеру покупки.")

def main():
    purchase = Purchases()
    while True:
        print("\nВиберіть пункт для покупок: ")
        print("1. додати")
        print("2. видалити")
        print("3. показати")
        print("4. відсортувати")
        print("5. відмітити")
        print("6. пошук покупки")
        print("7. редагування покупки")
        print("0. вийти.")
        choice = input("\nВиберіть пункт меню: ")
        if choice not in ('1', '2', '3', '4', '5', '6', '7', '0'):
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
        elif choice == '6':
            purchase.search_pur()
        elif choice == '7':
            purchase.edit_pur()
            purchase.save_file()
        else:
            break

if __name__ == '__main__':
    main()