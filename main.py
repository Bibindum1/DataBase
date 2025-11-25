import psycopg2

CONNECT_DB = {
    "host": "localhost",
    "user": "postgres",
    "password": "admin",
    "dbname": "postgres1",
    "port": "5432"
}

def init_database():
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS tasks
                           (
                               id
                               SERIAL
                               PRIMARY
                               KEY,
                               title
                               TEXT
                               NOT
                               NULL,
                               priority
                               TEXT
                               NOT
                               NULL
                           )
                           """)
        conn.commit()

def load_tasks():
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, title, priority FROM tasks ORDER BY id DESC')
            tasks = cursor.fetchall()
            return tasks

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Список задач пуст.")
    else:
        for task in tasks:
            print(f"{task[0]}. {task[1]} — [{task[2]}]")

def add_task():
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO tasks (title, priority) VALUES (%s, %s)', (title, priority))
        conn.commit()
    print("Задача добавлена.")

def delete_task():
    view_tasks()
    task_id = input("Введите ID задачи для удаления: ")
    try:
        task_id = int(task_id)
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
            conn.commit()
            if cursor.rowcount == 0:
                print("Задача с таким ID не найдена")
            else:
                print("Задача удалена")

def update_task():
    view_tasks()
    task_id = input("Введите ID задачи для обновления: ")
    try:
        task_id = int(task_id)
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return
    new_title = input("Введите новое название задачи (оставьте пустым, если не хотите менять): ")
    new_priority = input("Введите новый приоритет (Низкий/Средний/Высокий) (оставьте пустым, если не хотите менять): ")
    if not new_title and not new_priority:
        print("Нечего обновлять.")
        return
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            if new_title and new_priority:
                cursor.execute('UPDATE tasks SET title = %s, priority = %s WHERE id = %s',
                               (new_title, new_priority, task_id))
            elif new_title:
                cursor.execute('UPDATE tasks SET title = %s WHERE id = %s', (new_title, task_id))
            elif new_priority:
                cursor.execute('UPDATE tasks SET priority = %s WHERE id = %s', (new_priority, task_id))
            conn.commit()
            if cursor.rowcount == 0:
                print("Задача с таким ID не найдена")
            else:
                print("Задача обновлена.")

def main():
    init_database()
    print("Добро пожаловать в менеджер задач!")
    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("4 — Обновить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: \n")

        if choice == "1":
            view_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            update_task()
        elif choice == "0":
            print("Выход из программы.\n")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.\n")

if __name__ == "__main__":
    main()
