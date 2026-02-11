# Django Middleware & Signals - Lecture Notes

## 2-საათიანი ლექცია: Middleware და Signals

---

# Part 1: Middleware (1 საათი)

## 1.1 რა არის Middleware?

**Middleware** არის "შუამავალი" კოდი, რომელიც მუშაობს **ყოველი request/response**-ის დროს.

```
User Request → Middleware 1 → Middleware 2 → View → Middleware 2 → Middleware 1 → Response
```

### Django-ს ჩაშენებული Middleware (`settings.py`):
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # HTTPS, headers
    'django.contrib.sessions.middleware.SessionMiddleware', # Session management
    'django.middleware.common.CommonMiddleware',            # URL normalization
    'django.middleware.csrf.CsrfViewMiddleware',            # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # request.user
    'django.contrib.messages.middleware.MessageMiddleware', # Messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # X-Frame-Options
]
```

---

## 1.2 Middleware-ის სტრუქტურა

### ახალი სტილი (Django 1.10+):
```python
class SimpleMiddleware:
    def __init__(self, get_response):
        """
        ერთხელ გაეშვება სერვერის სტარტზე
        get_response - შემდეგი middleware ან view
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        ყოველი request-ის დროს გაეშვება
        """
        # Code BEFORE view (request phase)
        print(f"Before view: {request.path}")

        response = self.get_response(request)  # Call view

        # Code AFTER view (response phase)
        print(f"After view: {response.status_code}")

        return response
```

---

## 1.3 მაგალითი #1: Request Logging Middleware

### ფაილი: `library/middleware.py`

```python
import time
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    ლოგავს ყველა HTTP request-ს:
    - მეთოდი (GET, POST)
    - URL path
    - მომხმარებელი
    - დრო (რამდენი წამი დასჭირდა)
    - Status code
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Request-ის დაწყების დრო
        start_time = time.time()

        # View-ს გამოძახება
        response = self.get_response(request)

        # დროის გამოთვლა
        duration = time.time() - start_time

        # მომხმარებლის სახელი
        user = request.user.username if request.user.is_authenticated else 'Anonymous'

        # Console-ში ჩვენება
        print(
            f"[{request.method}] {request.path} | "
            f"User: {user} | "
            f"Status: {response.status_code} | "
            f"Time: {duration:.3f}s"
        )

        return response
```

---

## 1.4 მაგალითი #2: Maintenance Mode Middleware

```python
from django.http import HttpResponse
from django.conf import settings


class MaintenanceModeMiddleware:
    """
    თუ MAINTENANCE_MODE = True, საიტი დაბლოკილია
    გარდა admin-ისა და superuser-ებისა
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)

        if maintenance_mode:
            # Admin URL-ები გამონაკლისია
            if request.path.startswith('/admin/'):
                return self.get_response(request)

            # Superuser-ებს შეუძლიათ
            if request.user.is_authenticated and request.user.is_superuser:
                return self.get_response(request)

            # ყველა დანარჩენს - maintenance page
            return HttpResponse(
                """
                <html>
                <body style="text-align: center; padding: 50px;">
                    <h1>🔧 საიტი დროებით მიუწვდომელია</h1>
                    <p>მიმდინარეობს ტექნიკური სამუშაოები.</p>
                </body>
                </html>
                """,
                status=503
            )

        return self.get_response(request)
```

---

## 1.5 მაგალითი #3: IP Blocking Middleware

```python
from django.http import HttpResponseForbidden
from django.conf import settings


class IPBlockMiddleware:
    """
    ბლოკავს მითითებულ IP მისამართებს
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = getattr(settings, 'BLOCKED_IPS', [])

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if ip in self.blocked_ips:
            return HttpResponseForbidden(
                f"<h1>Access Denied</h1><p>Your IP ({ip}) is blocked.</p>"
            )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

---

## 1.6 Middleware-ის რეგისტრაცია

### `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom Middleware - ბოლოში დაამატეთ
    'library.middleware.RequestLoggingMiddleware',
    'library.middleware.MaintenanceModeMiddleware',
]

# Maintenance Mode setting
MAINTENANCE_MODE = False  # True = საიტი დაბლოკილია

# Blocked IPs
BLOCKED_IPS = [
    # '192.168.1.100',
]
```

---

# Part 2: Signals (1 საათი)

## 2.1 რა არის Signals?

**Signals** საშუალებას გაძლევთ **decoupled** აპლიკაციებმა მიიღონ შეტყობინება როცა რაღაც მოვლენა ხდება.

### Django-ს ჩაშენებული Signals:

| Signal | როდის იგზავნება |
|--------|-----------------|
| `pre_save` | მოდელის save()-მდე |
| `post_save` | მოდელის save()-ის შემდეგ |
| `pre_delete` | მოდელის delete()-მდე |
| `post_delete` | მოდელის delete()-ის შემდეგ |
| `m2m_changed` | ManyToMany ველის ცვლილებისას |
| `user_logged_in` | მომხმარებლის login-ისას |
| `user_logged_out` | მომხმარებლის logout-ისას |

---

## 2.2 Signal-ის სტრუქტურა

### მეთოდი 1: `@receiver` დეკორატორი (რეკომენდებული)
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book


@receiver(post_save, sender=Book)
def book_saved_handler(sender, instance, created, **kwargs):
    """
    sender - მოდელის კლასი (Book)
    instance - შენახული ობიექტი
    created - True თუ ახალი ობიექტია, False თუ update
    """
    if created:
        print(f"New book created: {instance.title}")
    else:
        print(f"Book updated: {instance.title}")
```

---

## 2.3 Signals ფაილის შექმნა

### ფაილი: `library/signals.py`

```python
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import Book, Loan, Author


# =============================================================================
# BOOK SIGNALS
# =============================================================================

@receiver(pre_save, sender=Book)
def book_pre_save(sender, instance, **kwargs):
    """
    წიგნის შენახვამდე - title-ის ფორმატირება
    """
    if instance.title:
        instance.title = instance.title.strip()


@receiver(post_save, sender=Book)
def book_post_save(sender, instance, created, **kwargs):
    """
    წიგნის შენახვის შემდეგ
    """
    if created:
        print(f"📚 [SIGNAL] New book added: '{instance.title}' by {instance.author}")
    else:
        print(f"📝 [SIGNAL] Book updated: '{instance.title}'")


@receiver(post_delete, sender=Book)
def book_post_delete(sender, instance, **kwargs):
    """
    წიგნის წაშლის შემდეგ
    """
    print(f"🗑️ [SIGNAL] Book deleted: '{instance.title}'")

    # წაშალე cover image ფაილიც
    if instance.cover:
        instance.cover.delete(save=False)


# =============================================================================
# LOAN SIGNALS
# =============================================================================

@receiver(post_save, sender=Loan)
def loan_created(sender, instance, created, **kwargs):
    """
    წიგნის გატანისას
    """
    if created:
        print(
            f"📖 [SIGNAL] Book borrowed: '{instance.book.title}' "
            f"by {instance.student.full_name}"
        )


@receiver(pre_save, sender=Loan)
def loan_returned_check(sender, instance, **kwargs):
    """
    წიგნის დაბრუნებისას
    """
    if instance.pk:
        try:
            old_loan = Loan.objects.get(pk=instance.pk)
            if old_loan.returned_at is None and instance.returned_at is not None:
                print(
                    f"✅ [SIGNAL] Book returned: '{instance.book.title}' "
                    f"by {instance.student.full_name}"
                )
        except Loan.DoesNotExist:
            pass


# =============================================================================
# USER AUTHENTICATION SIGNALS
# =============================================================================

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    მომხმარებლის login-ისას
    """
    ip = get_client_ip(request)
    print(f"🔑 [SIGNAL] User logged in: {user.username} from IP: {ip}")


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """
    მომხმარებლის logout-ისას
    """
    if user:
        print(f"🚪 [SIGNAL] User logged out: {user.username}")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return ip
```

---

## 2.4 Signals-ის რეგისტრაცია

### ფაილი: `library/apps.py`

```python
from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        """
        აპლიკაციის ჩატვირთვისას - signals-ის იმპორტი
        """
        import library.signals  # noqa
```

---

## 2.5 Custom Signals

```python
from django.dispatch import Signal

# Custom signal-ის შექმნა
book_borrowed = Signal()
book_returned = Signal()


# Signal-ის გაგზავნა (view-ში)
def borrow_book(request, book_id):
    # ... borrow logic ...
    
    # გაგზავნე custom signal
    book_borrowed.send(
        sender=Book,
        book=book,
        student=student,
        request=request
    )


# Signal-ის მიღება
@receiver(book_borrowed)
def handle_book_borrowed(sender, book, student, request, **kwargs):
    print(f"Custom signal received: {book} borrowed by {student}")
```

---

# Summary Tables

## Middleware vs Signals

| Middleware | Signals |
|------------|---------|
| Request/Response level | Model/Event level |
| ყოველი HTTP request | კონკრეტული მოვლენა |
| თანმიმდევრობა მნიშვნელოვანია | თანმიმდევრობა არ აქვს |
| `settings.py`-ში რეგისტრაცია | `apps.py`-ში რეგისტრაცია |

## Common Use Cases

| Use Case | Middleware or Signal? |
|----------|----------------------|
| Request logging | Middleware |
| Authentication check | Middleware |
| IP blocking | Middleware |
| Auto-create related objects | Signal |
| Send notifications | Signal |
| Audit logging | Signal |
| Cache invalidation | Signal |

---

# Quick Copy-Paste Commands

## Create middleware file:
```bash
touch library/middleware.py
```

## Create signals file:
```bash
touch library/signals.py
```

## Test server:
```bash
python manage.py runserver
```

---

# Console Output Examples

## Middleware Output:
```
[GET] /library/ | User: admin | Status: 200 | Time: 0.045s
[POST] /library/add/ | User: admin | Status: 302 | Time: 0.089s
```

## Signals Output:
```
📚 [SIGNAL] New book added: 'Python Guide' by John Doe
📖 [SIGNAL] Book borrowed: 'Python Guide' by Student Name
🔑 [SIGNAL] User logged in: admin from IP: 127.0.0.1
```
