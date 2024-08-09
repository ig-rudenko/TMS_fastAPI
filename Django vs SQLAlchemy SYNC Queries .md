Ниже представлены примеры сложных запросов, таких как агрегация, сортировка,
объединение таблиц и использование подзапросов. 

Каждый запрос на Django ORM соответствует аналогичному запросу в SQLAlchemy,
что позволяет увидеть, как различные типы операций реализуются в обеих системах.

## Поиск по одному полю

**Django:**

```python
user = User.objects.get(username='john_doe')
```

**SQLAlchemy:**

```python
user = session.query(User).filter_by(username='john_doe').one()
```

---

## Фильтрация по нескольким полям

**Django:**

```python
users = User.objects.filter(username='john_doe', email='john@example.com')
```

**SQLAlchemy:**

```python
users = session.query(User).filter_by(username='john_doe', email='john@example.com').all()
```

---

## Добавление новой записи

**Django:**

```python
new_user = User(username='jane_doe', email='jane@example.com')
new_user.save()
```

**SQLAlchemy:**

```python
new_user = User(username='jane_doe', email='jane@example.com')
session.add(new_user)
session.commit()
```

---

## Многие ко многим (добавление)

**Django:**

```python
user = User.objects.get(username='john_doe')
group = Group.objects.get(name='admins')
user.groups.add(group)
```

**SQLAlchemy:**

```python
user = session.query(User).filter_by(username='john_doe').one()
group = session.query(Group).filter_by(name='admins').one()
user.groups.append(group)
session.commit()
```

---

## Многие ко многим (получение)

**Django:**

```python
user = User.objects.get(username='john_doe')
groups = user.groups.all()
```

**SQLAlchemy:**

```python
user = session.query(User).filter_by(username='john_doe').one()
groups = user.groups
```

---

## Один ко многим (получение)

**Django:**

```python
author = Author.objects.get(name='J.K. Rowling')
books = author.book_set.all()
```

**SQLAlchemy:**

```python
author = session.query(Author).filter_by(name='J.K. Rowling').one()
books = author.books
```

---

## Агрегация (количество объектов)

**Django:**

```python
count = Book.objects.filter(author__name='J.K. Rowling').count()
```

**SQLAlchemy:**

```python
count = session.query(Book).join(Author).filter(Author.name == 'J.K. Rowling').count()
```

---

## Агрегация (сумма, среднее)

**Django:**

```python
avg_price = Book.objects.aggregate(Avg('price'))['price__avg']
```

**SQLAlchemy:**

```python
avg_price = session.query(func.avg(Book.price)).scalar()
```

---

## Сложная фильтрация с аннотацией

**Django:**

```python
from django.db.models import Count
authors = Author.objects.annotate(num_books=Count('book')).filter(num_books__gt=5)
```

**SQLAlchemy:**

```python
from sqlalchemy.sql import func
authors = session.query(Author, func.count(Book.id).label('num_books'))
authors = authors.join(Book).group_by(Author.id).having(func.count(Book.id) > 5).all()
```

---

## Поиск с сортировкой и лимитом

**Django:**

```python
top_books = Book.objects.order_by('-rating')[:10]
```

**SQLAlchemy:**

```python
top_books = session.query(Book).order_by(Book.rating.desc()).limit(10).all()
```

---

## Поиск с объединением таблиц

**Django:**

```python
books = Book.objects.select_related('author').filter(author__name='J.K. Rowling')
```

**SQLAlchemy:**

```python
books = session.query(Book).join(Author).filter(Author.name == 'J.K. Rowling').all()
```

---

## Запрос с использованием подзапроса

**Django:**

```python
from django.db.models import Subquery, OuterRef
books = Book.objects.filter(price__gt=Subquery(Author.objects.filter(name='J.K. Rowling').values('average_price')))
```

**SQLAlchemy:**

```python
subquery = session.query(func.avg(Book.price)).filter(Book.author_id == Author.id).subquery()
books = session.query(Book).filter(Book.price > subquery.c.avg_price).all()
```

