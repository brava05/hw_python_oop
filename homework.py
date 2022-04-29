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

        data_mes = asdict(self)
        MessStr = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')
        return MessStr.format(**data_mes)


class Training:
    """Базовый класс тренировки."""
    action: float
    duration: float
    weight: float
    mean_speed: float = 0
    calories: float = 0
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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.calories)


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        super().__init__(action, duration, weight)

        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Формула (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM
        * время_тренировки_в_минутах."""

        COEF_CALL_RUN_1 = 18
        COEF_CALL_RUN_2 = 20
        coeff_speed = COEF_CALL_RUN_1 * self.mean_speed - COEF_CALL_RUN_2

        calories = (coeff_speed
                    * self.weight
                    / self.M_IN_KM
                    * self.duration * self.MIN_IN_H)

        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Формула (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        * время_тренировки_в_минутах."""

        COEF_CALL_WLK_1 = 0.035
        COEF_CALL_WLK_2 = 0.029
        mean_speed = self.get_mean_speed()
        in_brackets = mean_speed ** 2 // self.height
        in_brackets2 = (in_brackets
                        * COEF_CALL_WLK_2
                        * self.weight)

        return ((COEF_CALL_WLK_1 * self.weight + in_brackets2)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

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
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки

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

        COEF_CALL_SW_1 = 1.1
        COEF_CALL_SW_2 = 2
        return ((self.mean_speed + COEF_CALL_SW_1)
                * COEF_CALL_SW_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    code_tr = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in code_tr:
        # создаем объект нужного типа
        tr = code_tr[workout_type](*data)

    else:
        # создаем просто тренинг по умолчанию
        tr = Training()

    return tr


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        # ('RUN', [420, 4, 20]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
