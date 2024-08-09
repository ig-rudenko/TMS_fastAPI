Для асинхронной работы с базой данных в SQLAlchemy используется `AsyncSession`,
и запросы выполняются немного по-другому, чем в синхронном режиме. 

Ниже соответствия запросов между Django ORM и асинхронным SQLAlchemy.


## Поиск по одному полю

**Django ORM:**

```python
user = User.objects.get(username='john_doe')
```

**Асинхронный SQLAlchemy:**

```python
user = await session.execute(select(User).filter_by(username='john_doe'))
user = user.scalars().one()
```

---

## Фильтрация по нескольким полям

**Django ORM:**

```python
users = User.objects.filter(username='john_doe', email='john@example.com')
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(User).filter_by(username='john_doe', email='john@example.com')
result = await session.execute(stmt)
users = result.scalars().all()
```

---

## Добавление новой записи

**Django ORM:**

```python
new_user = User(username='jane_doe', email='jane@example.com')
new_user.save()
```

**Асинхронный SQLAlchemy:**

```python
new_user = User(username='jane_doe', email='jane@example.com')
session.add(new_user)
await session.commit()
```

---

## Многие ко многим (добавление)

**Django ORM:**

```python
user = User.objects.get(username='john_doe')
group = Group.objects.get(name='admins')
user.groups.add(group)
```

**Асинхронный SQLAlchemy:**

```python
user = await session.execute(select(User).filter_by(username='john_doe'))
user = user.scalars().one()
group = await session.execute(select(Group).filter_by(name='admins'))
group = group.scalars().one()
user.groups.append(group)
await session.commit()
```

---

## Многие ко многим (получение)

**Django ORM:**

```python
user = User.objects.get(username='john_doe')
groups = user.groups.all()
```

**Асинхронный SQLAlchemy:**

```python
user = await session.execute(select(User).filter_by(username='john_doe'))
user = user.scalars().one()
groups = user.groups
```

---

## Один ко многим (получение)

**Django ORM:**

```python
author = Author.objects.get(name='J.K. Rowling')
books = author.book_set.all()
```

**Асинхронный SQLAlchemy:**

```python
author = await session.execute(select(Author).filter_by(name='J.K. Rowling'))
author = author.scalars().one()
books = await session.execute(select(Book).filter_by(author_id=author.id))
books = books.scalars().all()
```

---

## Агрегация (количество объектов)

**Django ORM:**

```python
count = Book.objects.filter(author__name='J.K. Rowling').count()
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(func.count()).select_from(Book).join(Author).filter(Author.name == 'J.K. Rowling')
result = await session.execute(stmt)
count = result.scalar()
```

---

## Агрегация (сумма, среднее)

**Django ORM:**

```python
avg_price = Book.objects.aggregate(Avg('price'))['price__avg']
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(func.avg(Book.price))
result = await session.execute(stmt)
avg_price = result.scalar()
```

---

## Сложная фильтрация с аннотацией

**Django ORM:**

```python
from django.db.models import Count
authors = Author.objects.annotate(num_books=Count('book')).filter(num_books__gt=5)
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(Author, func.count(Book.id).label('num_books')).join(Book).group_by(Author.id).having(func.count(Book.id) > 5)
result = await session.execute(stmt)
authors = result.all()
```

---

## Поиск с сортировкой и лимитом

**Django ORM:**

```python
top_books = Book.objects.order_by('-rating')[:10]
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(Book).order_by(Book.rating.desc()).limit(10)
result = await session.execute(stmt)
top_books = result.scalars().all()
```

---

## Поиск с объединением таблиц

**Django ORM:**

```python
books = Book.objects.select_related('author').filter(author__name='J.K. Rowling')
```

**Асинхронный SQLAlchemy:**

```python
stmt = select(Book).join(Author).filter(Author.name == 'J.K. Rowling')
result = await session.execute(stmt)
books = result.scalars().all()
```

---

## Запрос с использованием подзапроса

**Django ORM:**

```python
from django.db.models import Subquery, OuterRef
books = Book.objects.filter(price__gt=Subquery(Author.objects.filter(name='J.K. Rowling').values('average_price')))
```

**Асинхронный SQLAlchemy:**

```python
subquery = select(func.avg(Book.price)).filter(Book.author_id == Author.id).scalar_subquery()
stmt = select(Book).filter(Book.price > subquery)
result = await session.execute(stmt)
books = result.scalars().all()
```
