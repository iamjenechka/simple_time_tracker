import sqlite3
from datetime import datetime

class TimeTracker:
    def __init__(self, db_name="time_tracker.db"):
        self.conn = sqlite3.connect(db_name)

    def get_tasks_for_january(self):
        """Получаем задачи, которые начинаются или заканчиваются в январе 2025 года"""
        with self.conn:
            tasks = self.conn.execute(
                """
                SELECT id, chat_link, task_name, start_time, end_time
                FROM tasks
                WHERE (start_time LIKE '2025-01%' OR end_time LIKE '2025-01%')
                """
            ).fetchall()

        return tasks

    def calculate_duration(self, start_time, end_time):
        """Вычисляем продолжительность в минутах между start_time и end_time"""
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
        duration = (end_time - start_time).total_seconds() / 60  # Перевод в минуты
        return round(duration, 2)

    def show_january_tasks(self):
        tasks = self.get_tasks_for_january()
        total_minutes = 0

        if not tasks:
            print("Нет задач за январь.")
            return

        for task in tasks:
            task_id, chat_link, task_name, start_time, end_time = task
            if end_time:  # Если задача завершена
                duration = self.calculate_duration(start_time, end_time)
                total_minutes += duration
                print(
                    f"ID: {task_id}\n"
                    f"Задача: {task_name}\n"
                    f"Ссылка на чат: {chat_link}\n"
                    f"Начало: {start_time}\n"
                    f"Конец: {end_time}\n"
                    f"Длительность: {duration} минут\n"
                )
            else:
                print(
                    f"ID: {task_id}\n"
                    f"Задача: {task_name}\n"
                    f"Ссылка на чат: {chat_link}\n"
                    f"Начало: {start_time}\n"
                    f"Конец: Не завершена\n"
                    f"Длительность: В процессе\n"
                )

        print(f"\nОбщее время за январь: {round(total_minutes, 2)} минут.")

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    tracker = TimeTracker()

    print("Задачи за январь:")
    tracker.show_january_tasks()

    tracker.close()
