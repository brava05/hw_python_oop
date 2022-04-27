# from turtle import speed

class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""

        rez = (f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')

        return rez


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    distance = 0
    mean_speed = 0
    calories = 0

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

        if self.duration == 0:
            return 0
        else:
            return self.distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        mes = InfoMessage(training_type=self.__class__.__name__,
                          duration=self.duration,
                          distance=self.distance,
                          speed=self.mean_speed,
                          calories=self.calories)
        return mes


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.LEN_STEP = 0.65
        super().__init__(action, duration, weight)
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # (18 * средняя_скорость - 20) * вес_спортсмена / M_IN_KM \
        # * время_тренировки_в_минутах

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        mn_in_h = 60
        coeff_speed = coeff_calorie_1 * self.mean_speed - coeff_calorie_2

        calories = (coeff_speed
                    * self.weight
                    / self.M_IN_KM
                    * self.duration * mn_in_h)

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
        self.LEN_STEP = 0.65
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        # * время_тренировки_в_минутах
        coeff_1 = 0.035
        coeff_2 = 0.029
        mn_in_h = 60
        # (средняя_скорость**2 // рост) * 0.029 * вес
        coeff_body1 = self.mean_speed ** 2 // self.height
        coeff_body2 = (coeff_body1
                       * coeff_2
                       * self.weight)

        calories = ((coeff_1 * self.weight + coeff_body2)
                    * self.duration * mn_in_h)

        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

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
        self.distance = self.get_distance()
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
        """Получить количество затраченных калорий."""
        # (средняя_скорость + 1.1) * 2 * вес
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        calories = ((self.mean_speed + coeff_calorie_1)
                    * coeff_calorie_2
                    * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    code_tr = {
        'SWM': 'Swimming',
        'RUN': 'Running',
        'WLK': 'SportsWalking'
    }

    if workout_type in code_tr:
        # создаем объект нужного типа
        class_name = code_tr[workout_type]

        if class_name == 'Swimming':
            tr = Swimming(action=data[0],
                          duration=data[1],
                          weight=data[2],
                          length_pool=data[3],
                          count_pool=data[4])
        elif class_name == 'Running':
            tr = Running(action=data[0],
                         duration=data[1],
                         weight=data[2])
        elif class_name == 'SportsWalking':
            tr = SportsWalking(action=data[0],
                               duration=data[1],
                               weight=data[2],
                               height=data[3])
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
        # ('RUN', [15000, 1, 75]),
        ('RUN', [420, 4, 20]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
