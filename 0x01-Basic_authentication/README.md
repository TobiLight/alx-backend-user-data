# Project: 0x01. Basic authentication

## Resources

#### Read or watch:

* [REST API Authentication Mechanisms](https://intranet.alxswe.com/rltoken/ssg5umgsMk5jKM8WRHk2Ug)
* [Base64 in Python](https://intranet.alxswe.com/rltoken/RpaPRyKx1rdHgRSUyuPfeg)
* [HTTP header Authorization](https://intranet.alxswe.com/rltoken/WlARq8tQPUGQq5VphLKM4w)
* [Flask](https://intranet.alxswe.com/rltoken/HG5WXgSja5kMa29fbMd9Aw)
* [Base64 - concept](https://intranet.alxswe.com/rltoken/br6Rp4iMaOce6EAC-JQnOw)
## Learning Objectives

### General

* What authentication means
* What Base64 is
* How to encode a string in Base64
* What Basic authentication means
* How to send the Authorization header
## Tasks

| Task | File |
| ---- | ---- |
| 0. Simple-basic-API | [SOON](./) |
| 1. Error handler: Unauthorized | [api/v1/app.py](./api/v1/app.py), [api/v1/views/index.py](./api/v1/views/index.py) |
| 2. Error handler: Forbidden | [api/v1/app.py](./api/v1/app.py), [api/v1/views/index.py](./api/v1/views/index.py) |
| 3. Auth class | [api/v1/auth](./api/v1/auth), [api/v1/auth/__init__.py](./api/v1/auth/__init__.py), [api/v1/auth/auth.py](./api/v1/auth/auth.py) |
| 4. Define which routes don't need authentication | [api/v1/auth/auth.py](./api/v1/auth/auth.py) |
| 5. Request validation! | [api/v1/app.py](./api/v1/app.py), [api/v1/auth/auth.py](./api/v1/auth/auth.py) |
| 6. Basic auth | [api/v1/app.py](./api/v1/app.py), [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py) |
| 7. Basic - Base64 part | [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py) |
| 8. Basic - Base64 decode | [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py) |
| 9. Basic - User credentials | [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py) |
| 10. Basic - User object | [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py) |
| 11. Basic - Overload current_user - and BOOM! | [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py) |
