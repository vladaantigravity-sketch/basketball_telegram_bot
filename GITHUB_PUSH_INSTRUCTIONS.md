# Подробная инструкция: Push проекта на GitHub

## Шаг 1: Настройка Git (если еще не настроен)

### 1.1. Настройка email и имени пользователя (локально для этого проекта)

Откройте PowerShell в папке проекта и выполните:

```powershell
# Замените на ваш реальный email GitHub
git config user.email "ваш-email@example.com"

# Замените на ваше имя или GitHub username
git config user.name "Ваше Имя"
```

**Пример:**
```powershell
git config user.email "vlada@example.com"
git config user.name "Vlada Antigravity"
```

**Примечание:** Если хотите настроить глобально для всех проектов, используйте `--global`:
```powershell
git config --global user.email "ваш-email@example.com"
git config --global user.name "Ваше Имя"
```

---

## Шаг 2: Проверка настроек Git

Проверьте, что настройки применены:

```powershell
git config user.email
git config user.name
```

---

## Шаг 3: Проверка файлов для коммита

Убедитесь, что нужные файлы добавлены (bot_env/ должен быть в .gitignore):

```powershell
git status
```

Вы должны видеть:
- ✅ `bot.py`
- ✅ `README.md`
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ❌ `bot_env/` - не должен быть виден (игнорируется)

---

## Шаг 4: Создание первого коммита

```powershell
git commit -m "Initial commit: Telegram bot for basketball lessons with Russian/English support"
```

---

## Шаг 5: Переименование ветки в main (если нужно)

```powershell
git branch -M main
```

---

## Шаг 6: Push на GitHub

### 6.1. Убедитесь, что remote настроен:

```powershell
git remote -v
```

Должно показать:
```
origin  https://github.com/vladaantigravity-sketch/basketball_telegram_bot.git (fetch)
origin  https://github.com/vladaantigravity-sketch/basketball_telegram_bot.git (push)
```

Если remote не настроен, выполните:
```powershell
git remote add origin https://github.com/vladaantigravity-sketch/basketball_telegram_bot.git
```

### 6.2. Push на GitHub

```powershell
git push -u origin main
```

**Если будет запрошен пароль:**
- GitHub больше не принимает обычные пароли
- Используйте **Personal Access Token (PAT)** вместо пароля
- Или настройте SSH-ключи (см. альтернативный метод ниже)

---

## Альтернативный метод: Push с использованием Personal Access Token

### Если GitHub требует аутентификацию:

1. **Создайте Personal Access Token на GitHub:**
   - Перейдите: https://github.com/settings/tokens
   - Нажмите "Generate new token" → "Generate new token (classic)"
   - Выберите срок действия и права доступа (достаточно `repo`)
   - Скопируйте токен

2. **При push используйте токен вместо пароля:**
   ```
   Username: ваш-github-username
   Password: вставьте-здесь-PAT-токен
   ```

3. **Или используйте токен в URL (для быстрого push):**
   ```powershell
   git remote set-url origin https://YOUR_TOKEN@github.com/vladaantigravity-sketch/basketball_telegram_bot.git
   git push -u origin main
   ```
   *(После push рекомендую вернуть обычный URL для безопасности)*

---

## Полная последовательность команд (для копирования)

```powershell
# 1. Настройка Git (выполните один раз)
git config user.email "ваш-email@example.com"
git config user.name "Ваше Имя"

# 2. Проверка файлов
git status

# 3. Создание коммита
git commit -m "Initial commit: Telegram bot for basketball lessons with Russian/English support"

# 4. Переименование ветки
git branch -M main

# 5. Push на GitHub
git push -u origin main
```

---

## Проверка результата

После успешного push:

1. Откройте браузер
2. Перейдите: https://github.com/vladaantigravity-sketch/basketball_telegram_bot
3. Вы должны увидеть ваши файлы в репозитории

---

## Важные замечания

### ✅ Безопасность

- **BOT_TOKEN не хранится в коде** - используется переменная окружения
- **bot_env/ игнорируется** - виртуальное окружение не попадет в репозиторий
- **.env файлы игнорируются** - секреты защищены через .gitignore

### ⚠️ Что НЕ попадет в репозиторий (благодаря .gitignore):

- `bot_env/` - виртуальное окружение Python
- `__pycache__/` - скомпилированные Python файлы
- `.env` - файлы с секретами
- `*.pyc` - байт-код Python
- Другие временные файлы

### 📝 Для будущих изменений

После внесения изменений в код:

```powershell
# Добавить изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push
```

---

## Решение проблем

### Проблема: "Authentication failed"

**Решение:** Используйте Personal Access Token вместо пароля

### Проблема: "remote origin already exists"

**Решение:** Это нормально, remote уже настроен. Можно продолжить.

### Проблема: "failed to push some refs"

**Решение:** 
- Если репозиторий на GitHub не пустой, сначала выполните `git pull origin main --allow-unrelated-histories`
- Затем `git push -u origin main`

### Проблема: "Permission denied"

**Решение:** 
- Проверьте, что у вас есть права на запись в репозиторий
- Убедитесь, что используете правильный GitHub аккаунт

---

## Дополнительные ресурсы

- [GitHub: Creating a repository](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [GitHub: Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Git: First-time setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
