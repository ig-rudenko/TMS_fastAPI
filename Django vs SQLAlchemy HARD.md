## Фильтрация с выражением OR и игнорированием регистра

**Django ORM:**

```python
from django.db.models import Q

...
notes = Note.objects.filter(
    Q(title__icontains="search_term") | Q(content__icontains="search_term")
).select_related("tags")

```

**Синхронный SQLAlchemy:**

```python
from sqlalchemy import or_, func
from sqlalchemy.orm import selectinload

...
notes = session.scalars(
    select(Note)
    .filter(
        or_(
            func.lower(Note.title).contains("search_term".lower()),
            func.lower(Note.content).contains("search_term".lower()),
        )
    )
    .options(selectinload(Note.tags))
).all()

```

**Асинхронный SQLAlchemy:**

```python
from sqlalchemy import or_, func, select
from sqlalchemy.orm import selectinload

...
stmt = (
    select(Note)
    .filter(
        or_(
            func.lower(Note.title).contains("search_term".lower()),
            func.lower(Note.content).contains("search_term".lower()),
        )
    )
    .options(selectinload(Note.tags))
)

result = await session.execute(stmt)
notes = result.scalars().all()

```

---

### Объяснение:

- **Django ORM:** Используется комбинация `Q` для выражения `OR` и `__icontains` для игнорирования регистра, что
  позволяет искать совпадения в строках `title` и `content`.

- **Синхронный SQLAlchemy:** Здесь используется метод `or_` для выражения `OR` и `func.lower()` для приведения обоих
  полей и строки поиска к нижнему регистру, что имитирует поведение `__icontains` в Django ORM.

- **Асинхронный SQLAlchemy:** В асинхронной версии SQLAlchemy, код практически идентичен синхронной версии, но
  используется асинхронная сессия для выполнения запроса с помощью `await`.


## Поиск всех заметок для пользователя с _username_ равным _user123_

**Django ORM:**

```python
notes = Note.objects.filter(user__username='user123')
```

**Синхронный SQLAlchemy:**

```python
notes = session.query(Note).join(User).filter(User.username == 'user123').all()
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(Note).join(User).filter(User.username == 'user123')
result = await session.execute(stmt)
notes = result.scalars().all()
```

---

### Объяснение:

- **Django ORM:** Используется `filter` с отношением к связанному объекту `user__username`, что позволяет легко искать заметки, связанные с пользователем.

- **Синхронный SQLAlchemy:** Здесь используется метод `join`, чтобы присоединить таблицу `User` и затем применить фильтр по полю `username`. Запрос возвращает все заметки, соответствующие пользователю `user123`.

- **Асинхронный SQLAlchemy:** Асинхронная версия SQLAlchemy выполняет аналогичный запрос, используя `select` и `await` для выполнения асинхронного запроса.



## Поиск всех заметок, созданных за последние 10 часов, без содержимого и возврат первых 100 записей

**Django ORM:**

```python
from django.utils import timezone
from datetime import timedelta

# Определяем время 10 часов назад
ten_hours_ago = timezone.now() - timedelta(hours=10)

# Выполняем запрос
notes = Note.objects.filter(created_at__gte=ten_hours_ago).only('id', 'title')[:100]
```

**Синхронный SQLAlchemy:**

```python
from sqlalchemy import select
from datetime import datetime, timedelta, UTC

# Определяем время 10 часов назад
ten_hours_ago = datetime.now(UTC) - timedelta(hours=10)

# Выполняем запрос
stmt = select(Note.id, Note.title).filter(Note.created_at >= ten_hours_ago).limit(100)
result = session.execute(stmt)
notes = result.fetchall()
```

**Асинхронный SQLAlchemy:**

```python
from sqlalchemy import select
from datetime import datetime, timedelta, UTC

# Определяем время 10 часов назад
ten_hours_ago = datetime.now(UTC) - timedelta(hours=10)

# Выполняем запрос
stmt = select(Note.id, Note.title).filter(Note.created_at >= ten_hours_ago).limit(100)
result = await session.execute(stmt)
notes = result.fetchall()
```

---

### Объяснение:

- **Django ORM:** 
  - Используем `timezone.now()` и `timedelta` для вычисления времени 10 часов назад.
  - Фильтруем заметки по дате создания с помощью `created_at__gte`.
  - Используем `only('id', 'title')` для выборки только необходимых полей (`id` и `title`), что помогает избежать загрузки полного содержимого.
  - Ограничиваем результат до первых 100 записей с помощью среза `[:100]`.

- **Синхронный SQLAlchemy:** 
  - Используем `datetime.now(UTC)` и `timedelta` для вычисления времени 10 часов назад.
  - Выполняем запрос с `select` для выбора только полей `id` и `title`.
  - Фильтруем заметки по дате создания и ограничиваем результат до 100 записей с помощью `limit(100)`.

- **Асинхронный SQLAlchemy:** 
  - Применяем аналогичный подход как и в синхронном SQLAlchemy, но используем асинхронные операции с `await` для выполнения запроса.


## Получение всех заметок с тегами "python" и "js"

**Django ORM:**

```python
from django.db.models import Q

# Находим теги по именам
python_tag = Tag.objects.get(name='python')
js_tag = Tag.objects.get(name='js')

# Фильтруем заметки, которые имеют оба тега
notes = Note.objects.filter(tags__in=[python_tag, js_tag]).annotate(
    tag_count=Count('tags')
).filter(tag_count=2)
```

**Синхронный SQLAlchemy:**

```python
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload

# Находим теги по именам
python_tag = session.query(Tag).filter_by(name='python').one()
js_tag = session.query(Tag).filter_by(name='js').one()

# Создаем подзапрос для фильтрации заметок с обоими тегами
stmt = (
    select(Note)
    .join(Note.tags)
    .filter(Tag.name.in_(['python', 'js']))
    .group_by(Note.id)
    .having(func.count(Tag.id) == 2)
)
result = session.execute(stmt)
notes = result.scalars().all()
```

**Асинхронный SQLAlchemy:**

```python
from sqlalchemy import select, and_, func
from sqlalchemy.future import select

# Находим теги по именам
python_tag = await session.execute(select(Tag).filter_by(name='python'))
python_tag = python_tag.scalars().one()
js_tag = await session.execute(select(Tag).filter_by(name='js'))
js_tag = js_tag.scalars().one()

# Создаем подзапрос для фильтрации заметок с обоими тегами
stmt = (
    select(Note)
    .join(Note.tags)
    .filter(Tag.name.in_(['python', 'js']))
    .group_by(Note.id)
    .having(func.count(Tag.id) == 2)
)
result = await session.execute(stmt)
notes = result.scalars().all()
```

---

### Объяснение:

- **Django ORM:**
  - Сначала находим объекты тегов `python` и `js`.
  - Используем `filter` с `tags__in` для фильтрации заметок, которые имеют хотя бы один из этих тегов.
  - Затем аннотируем количество тегов у каждой заметки с помощью `Count('tags')` и фильтруем заметки, у которых количество тегов равно 2.

- **Синхронный SQLAlchemy:**
  - Находим теги по именам.
  - Создаем запрос с `select` и `join` для соединения таблиц `Note` и `Tag`.
  - Используем `filter` для проверки, что заметки имеют теги "python" и "js".
  - Группируем по `Note.id` и используем `having` для проверки, что у заметки есть оба тега (т.е., `func.count(Tag.id) == 2`).

- **Асинхронный SQLAlchemy:**
  - Подход аналогичен синхронному SQLAlchemy, но используется асинхронный подход с `await` для выполнения запросов и получения результатов.
