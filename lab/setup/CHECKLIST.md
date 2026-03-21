Checklist — быстрые шаги для проверки (копировать/выполнять в терминале)

1) Находясь в корне проекта:

```bash
# Проверка бэкенда
curl -sf http://localhost:42002/docs && echo "backend OK" || echo "backend недоступен"

# Проверка .env файлов
[ -f .env.bot.secret ] && echo ".env.bot.secret OK" || echo ".env.bot.secret отсутствует"
[ -f .env.docker.secret ] && echo ".env.docker.secret OK" || echo ".env.docker.secret отсутствует"

# Запуск docker-compose (если используется)
docker compose up -d --build
```

2) Быстрая проверка тестов:

```bash
python -m pytest -q || true
```

3) Проверка работы бота в тестовом режиме — см. `bot/pyproject.toml` или `bot/bot.py` для синтаксиса.

Если что-то не работает — сохраните вывод ошибок и свяжитесь с ассистентом, приложив логи.
