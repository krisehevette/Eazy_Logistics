from abc import ABC, abstractmethod

# ============================
# S — Single Responsibility
# ============================

class Order:
    """Хранит данные заказа (только данные — никакой логики)."""
    def __init__(self, items):
        self.items = items

    @property
    def total(self):
        return sum(self.items)


# ============================
# O — Open/Closed
# ============================

class DiscountStrategy(ABC):
    """Абстракция скидки — можно добавлять новые стратегии без изменения старого кода."""
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        return amount


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, amount: float) -> float:
        return amount * (1 - self.percent / 100)


# ============================
# L — Liskov Substitution
# ============================

class FixedDiscount(DiscountStrategy):
    """Корректно подставляется вместо любого DiscountStrategy."""
    def __init__(self, value: float):
        self.value = value

    def apply(self, amount: float) -> float:
        result = amount - self.value
        return max(result, 0)  # Не ломаем контракт: возвращаем число >= 0


# ============================
# I — Interface Segregation
# ============================

class ILogger(ABC):
    """Узкий интерфейс логирования."""
    @abstractmethod
    def log(self, message: str):
        pass


class INotifier(ABC):
    """Отдельный интерфейс уведомлений."""
    @abstractmethod
    def notify(self, message: str):
        pass


class ConsoleLogger(ILogger):
    def log(self, message: str):
        print("[LOG]", message)


class EmailNotifier(INotifier):
    def notify(self, message: str):
        print("[EMAIL]", message)


# ============================
# D — Dependency Inversion
# ============================

class OrderProcessor:
    """Высокоуровневый модуль зависит от абстракций, а не от конкретных классов."""

    def __init__(self, logger: ILogger, notifier: INotifier, discount: DiscountStrategy):
        self.logger = logger
        self.notifier = notifier
        self.discount = discount

    def process(self, order: Order):
        self.logger.log("Начинаю обработку заказа")

        total = order.total
        total_after_discount = self.discount.apply(total)

        self.logger.log(f"Сумма до скидки: {total}")
        self.logger.log(f"Сумма после скидки: {total_after_discount}")

        self.notifier.notify(f"Ваш заказ обработан. Итог: {total_after_discount}")

        return total_after_discount


# ============================
# Пример использования
# ============================

if __name__ == "__main__":
    order = Order([100, 200, 350])

    processor = OrderProcessor(
        logger=ConsoleLogger(),
        notifier=EmailNotifier(),
        discount=PercentageDiscount(10)
    )

    processor.process(order)
