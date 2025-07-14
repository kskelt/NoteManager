# Notes Manager API

**FastAPI приложение для управления заметками с MongoDB и JWT аутентификацией**

---
## 🛠 Локально

1. **Установите зависимости**:
```bash
    poetry install
```
2. **Создайте .env файл по примеру с .env.example**
3. **Запустите MongoDB**:
```bash
    docker run -d -p 27017:27017 --name mongo mongo:6.0
```
4. **Запустите приложение**:
```bash
poetry run uvicorn app.init_app:init_app --reload
```
## 🐳 Docker
```bash
docker-compose -f docker/docker-compose.yml up -d --build
```