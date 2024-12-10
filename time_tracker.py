import sqlite3
from datetime import datetime


class TimeTracker:
    def __init__(self, db_name="time_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_link TEXT,
                    task_name TEXT,
                    start_time TEXT,
                    end_time TEXT
                )
                """
            )

    def start_task(self, chat_link, task_name):
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO tasks (chat_link, task_name, start_time, end_time)
                VALUES (?, ?, ?, NULL)
                """,
                (chat_link, task_name, datetime.now()),
            )
        print(f"Начата задача '{task_name}' ({chat_link}) в {datetime.now()}.")

    def end_task(self, task_id):
        with self.conn:
            task = self.conn.execute(
                "SELECT task_name, start_time FROM tasks WHERE id = ? AND end_time IS NULL",
                (task_id,),
            ).fetchone()
            if not task:
                print("Активная задача с указанным ID не найдена.")
                return

            self.conn.execute(
                """
                UPDATE tasks
                SET end_time = ?
                WHERE id = ?
                """,
                (datetime.now(), task_id),
            )
        print(f"Завершена задача '{task[0]}' в {datetime.now()}.")

    def resume_task(self, task_id):
        with self.conn:
            task = self.conn.execute(
                "SELECT chat_link, task_name FROM tasks WHERE id = ? AND end_time IS NOT NULL",
                (task_id,),
            ).fetchone()
            if not task:
                print("Нельзя продолжить задачу, которая не завершена или не существует.")
                return

            self.conn.execute(
                """
                INSERT INTO tasks (chat_link, task_name, start_time, end_time)
                VALUES (?, ?, ?, NULL)
                """,
                (task[0], task[1], datetime.now()),
            )
        print(f"Задача '{task[1]}' продолжена в {datetime.now()}.")

    def show_tasks(self):
        with self.conn:
            tasks = self.conn.execute(
                "SELECT id, chat_link, task_name, start_time, end_time FROM tasks"
            ).fetchall()
            for task in tasks:
                task_id, chat_link, task_name, start_time, end_time = task
                duration = (
                    (datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).seconds
                    if end_time
                    else "в процессе"
                )
                print(
                    f"ID: {task_id}\n"
                    f"   Задача: {task_name}\n"
                    f"   Ссылка на чат: {chat_link}\n"
                    f"   Начало: {start_time}\n"
                    f"   Конец: {end_time or 'Не завершена'}\n"
                    f"   Длительность: {duration} секунд\n"
                )

    def close(self):
        self.conn.close()


def main():
    tracker = TimeTracker()
    try:
        while True:
            print("\nДоступные команды:")
            print("1. Начать задачу")
            print("2. Завершить задачу")
            print("3. Продолжить задачу")
            print("4. Показать все задачи")
            print("5. Выход")

            command = input("Введите номер команды: ")

            if command == "1":
                chat_link = input("Введите ссылку на чат: ")
                task_name = input("Введите название задачи: ")
                tracker.start_task(chat_link, task_name)
            elif command == "2":
                task_id = int(input("Введите ID задачи для завершения: "))
                tracker.end_task(task_id)
            elif command == "3":
                task_id = int(input("Введите ID задачи для продолжения: "))
                tracker.resume_task(task_id)
            elif command == "4":
                tracker.show_tasks()
            elif command == "5":
                print("Выход из программы.")
                break
            else:
                print("Неверная команда. Попробуйте снова.")
    finally:
        tracker.close()


if __name__ == "__main__":
    main()
