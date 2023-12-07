import random
import datetime


class Order:
    def __init__(self, number=None, products=None, time=None, phone_num=None):
        self.number = number
        self.products = products
        self.time = time
        self.phone_num = phone_num

    def set_num_time(self, number, time):
        self.number = number
        self.time = time


class Bot:
    def __init__(self):
        self.order = None
        self.orders = []

        print('Приветствую! Я бот для заказы еды.')
        self.bot_state = State()
        self.bot_state.toggle_to_StartMenu()
        self.bot_state.state.info()

    def chat(self):
        self.reaction(input('...'))

    def reaction(self, user):
        # состояние равно StartMenu
        if self.bot_state.get_state() == StartMenu(self).get_state(self):
            if user == self.bot_state.state.commands[0]:
                self.bot_state.toggle_to_AddingOrder()
                self.order = self.bot_state.state.add_products()
            elif user == self.bot_state.state.commands[1]:
                # self.bot_state.state.show_orders()
                for order in self.orders:
                    print('Заказ', order.number, 'от', order.time)
                    print('Продукты', order.products)
                    print('Ваш номер:', order.phone_num, '\n')
            elif user == self.bot_state.state.commands[2]:
                self.bot_state.state.info()
            else:
                print('Сейчас доступны только эти команды:', self.bot_state.state.commands)

        # состояние равно AddingOrder
        elif self.bot_state.get_state() == AddingOrder(self).get_state(self):
            if user == self.bot_state.state.commands[0]:
                self.bot_state.toggle_to_AddingPhNum(self.order)
                self.order = self.bot_state.state.add_phone()
            elif user == self.bot_state.state.commands[1]:
                self.order = self.bot_state.state.add_products()
            elif user == self.bot_state.state.commands[2]:
                print('Ваш заказ отменен :(')
                self.bot_state.toggle_to_StartMenu()
            else:
                print('Сейчас доступны только эти команды:', self.bot_state.state.commands)

        # состояние равно AddingPhNum
        elif self.bot_state.get_state() == AddingPhNum(self, self.order).get_state(self):
            if user == self.bot_state.state.commands[0]:
                print('Ваш заказ принят!')
                print('Мы вам скоро позвоним :)')
                time = datetime.datetime.now()
                number = random.randint(0, 1000)
                self.order.set_num_time(number, time)
                self.orders.append(self.order)
                self.bot_state.toggle_to_StartMenu()
            elif user == self.bot_state.state.commands[1]:
                self.order = self.bot_state.state.add_phone()
            elif user == self.bot_state.state.commands[2]:
                self.bot_state.toggle_to_AddingOrder()
                self.order = self.bot_state.state.add_products()
            elif user == self.bot_state.state.commands[3]:
                print('Ваш заказ отменен :(')
                self.bot_state.toggle_to_StartMenu()
            else:
                print('Сейчас доступны только эти команды:', self.bot_state.state.commands)


# класс для управления состоянием
class State:
    def __init__(self, order=None):
        self.state = None

    def get_state(self):
        return self.state.get_state(self)

    def toggle_to_StartMenu(self):
        self.state = StartMenu(self)

    def toggle_to_AddingOrder(self):
        self.state = AddingOrder(self)

    def toggle_to_AddingPhNum(self, order):
        self.state = AddingPhNum(self, order)


# состояние StartMenu
class StartMenu:
    def __init__(self, state):
        self.state = state
        self.commands = ['сделать заказ', 'мои заказы', 'инфо']

    def info(self):
        print('Мои команды:', self.commands)

    @staticmethod
    def get_state(self):
        return 'StartMenu'


# состояние AddingOrder
class AddingOrder:
    def __init__(self, state):
        self.state = state
        self.commands = ['подтвердить', 'редактировать', 'отменить']
        self.order = Order()

    def add_products(self):
        print('Введите список продуктов')
        self.order.products = input('...')

        print('Подтвердите заказ (напишите "подтвердить")')
        print('Или отредактируйте (напишите "редактировать")')
        print('Для отмены напишите "отменить"')

        return self.order

    @staticmethod
    def get_state(self):
        return 'AddingOrder'


# состояние AddingPhNum
class AddingPhNum:
    def __init__(self, state, order):
        self.state = state
        self.commands = ['подтвердить', 'редактировать', 'назад', 'отменить']
        self.user_ans = None
        self.order = order

    def add_phone(self):
        print('Введите ваш номер телефона')
        self.order.phone_num = input('...')

        print('Для завершения оформления заказа напишите "подтвердить")')
        print('Для редактирования номера напишите "редактировать")')
        print('Для возвращения к редактированию списка продуктов напишите "назад"')
        print('Для отмены заказа напишите "отменить"')

        return self.order

    @staticmethod
    def get_state(self):
        return 'AddingPhNum'


def main():
    bot = Bot()
    while True:
        bot.chat()
        print('state:', bot.bot_state.get_state())


if __name__ == '__main__':
    main()
