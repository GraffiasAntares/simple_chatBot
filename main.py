class FoodOrderBot:
    def __init__(self):
        self.state = "StartMenu"
        self.order_items = []
        self.phone_number = None
        self.commands = {
            "StartMenu": {"старт": self.start_menu},
            "AddOrder": {"заказ": self.add_order,
                         "редактировать": self.edit_order,
                         "завершить": self.finish_order,
                         "телефон": self.enter_phone_number},
            "PhoneNumber": {"телефон": self.enter_phone_number}
        }

    def start_menu(self):
        self.message()
        self.state = "AddOrder"
        self.message()

    def add_order(self):
        self.order_items = input("Введите товары через пробел: ").split()
        if not(self.phone_number in [None, '']):
            self.message()
            return
        self.state = "PhoneNumber"
        self.message()

    def edit_order(self):
        print("Отредактируйте ваш заказ.")
        print("Товары:", self.order_items)
        item_to_remove = input("Напишите товар для удаления: ")
        if item_to_remove in self.order_items:
            self.order_items.remove(item_to_remove)
        else:
            print("Товар не найден.")
        self.state = "AddOrder"
        self.message()

    def finish_order(self):
        if len(self.order_items) != 0 and not(self.phone_number in [None, '']):
            print("Заказ оформлен.")
            print("Товары:", self.order_items)
            if self.phone_number:
                print("Ваш телефон:", self.phone_number)

            self.phone_number = None
            self.order_items = []
            self.state = "StartMenu"

        elif len(self.order_items) != 0 and self.phone_number in [None, '']:
            print("Добавьте номер телефона!")

        elif len(self.order_items) == 0:
            print("До свидания!")
            self.state = "StartMenu"

    def enter_phone_number(self):
        phone = input("Добавьте номер телефона: ").replace(" ", "")
        self.phone_number = phone
        self.state = "AddOrder"
        self.message()

    def process_command(self, command):
        if self.state == "PhoneNumber" and command.lower() == "назад":
            self.state = "AddOrder"
            self.message()
        else:
            handler = self.commands[self.state].get(command, lambda: print("Неверная команда"))
            handler()

    def message(self):
        if self.state == "StartMenu":
            print("Приветствую!")
        elif self.state == "AddOrder":
            print("Меню: Оформление заказа")
        elif self.state == "PhoneNumber":
            print("Меню: Добавление номера")


def main():
    bot = FoodOrderBot()
    while True:
        bot.process_command(input('...'))


if __name__ == '__main__':
    main()


