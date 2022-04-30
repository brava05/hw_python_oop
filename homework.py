from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""

        MESSAGE_STR = ('Тип тренировки: {training_type}; '
                       'Длительность: {duration:.3f} ч.; '
                       'Дистанция: {distance:.3f} км; '
                       'Ср. скорость: {speed:.3f} км/ч; '
                       'Потрачено ккал: {calories:.3f}.')
        return MESSAGE_STR.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    action: float
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Для указанного вида тренировки нет формулы расчета калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_RUNNING_COEFFICIENT_1: int = 18
    CALORIES_RUNNING_COEFFICIENT_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Формула (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM
        * время_тренировки_в_минутах."""

        return (
            (
                self.CALORIES_RUNNING_COEFFICIENT_1 * self.get_mean_speed()
                - self.CALORIES_RUNNING_COEFFICIENT_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WALKING_COEFFICIENT_1: float = 0.035
    CALORIES_WALKING_COEFFICIENT_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Формула (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        * время_тренировки_в_минутах."""

        return (
            (
                self.CALORIES_WALKING_COEFFICIENT_1 * self.weight
                + (self.get_mean_speed() ** 2
                   // self.height
                   * self.CALORIES_WALKING_COEFFICIENT_2
                   * self.weight
                   )
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_SWIMMING_COEFFICIENT_1: float = 1.1
    CALORIES_SWIMMING_COEFFICIENT_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:

        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
        Формула длина_бассейна * count_pool / M_IN_KM / время_тренировки."""

        if self.duration == 0:
            return 0
        else:
            return (self.length_pool
                    * self.count_pool
                    / self.M_IN_KM
                    / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Формула (средняя_скорость + 1.1) * 2 * вес"""

        return ((self.get_mean_speed() + self.CALORIES_SWIMMING_COEFFICIENT_1)
                * self.CALORIES_SWIMMING_COEFFICIENT_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in dict_training:
        raise NotImplementedError(
            'В данных указан вид тренировки, не предусмотренный программой')

    # создаем объект нужного типа
    return dict_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    # сомневаюсь, что так лучше для понимания кода,
    # чем с промежуточной переменной,
    # но замечание учел
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        # здесь тоже можно убрать одноразовую переменную
        # но тогда код вообще какой-то неудобоваримый полчается
        training = read_package(workout_type, data)
        main(training)
