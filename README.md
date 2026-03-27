# KOMPAS-3D MCP Client

Готовый Windows-пакет для подключения KOMPAS-3D к MCP.

Внутри архива:
- `kompas-mcp.exe`
- все нужные runtime-файлы
- `README.md`
- skill `kompas-mcp-operator`

## Что нужно

- Windows
- установленный KOMPAS-3D
- MCP-клиент, который умеет запускать локальную команду

## Установка

1. Скачайте последний архив из Releases.
2. Распакуйте его, например, в:

```text
C:\Programs\kompasmcp
```

3. Если вам уже выдали `config.json`, положите его сюда:

```text
%USERPROFILE%\.kompasmcp\config.json
```

4. Если `config.json` еще нет, выполните вход одной из команд ниже.

## Вход

Если у вас есть invite code:

```bash
C:\Programs\kompasmcp\kompas-mcp.exe login --base-url https://your-host --invite-code XXXX-XXXX
```

Если у вас есть `token` и `client_id`:

```bash
C:\Programs\kompasmcp\kompas-mcp.exe login --base-url https://your-host --token <token> --client-id <client-id>
```

После этого клиент создаст файл:

```text
%USERPROFILE%\.kompasmcp\config.json
```

## Подключение в MCP-клиенте

Пример конфигурации:

```json
{
  "mcpServers": {
    "kompas": {
      "command": "C:/Programs/kompasmcp/kompas-mcp.exe"
    }
  }
}
```

## Skill

В архиве есть папка:

```text
skills\kompas-mcp-operator
```

Скопируйте ее в:

```text
%USERPROFILE%\.codex\skills\kompas-mcp-operator
```

Этот skill помогает при работе с 2D, 3D, screenshot, export и диагностикой.

## Если запуск не работает

Проверьте:

1. `kompas-mcp.exe` лежит в той папке, откуда вы его запускаете.
2. `config.json` лежит в `%USERPROFILE%\.kompasmcp\config.json`.
3. KOMPAS-3D установлен на этой Windows-машине.
4. После логина вы перезапустили MCP-клиент.
5. Если используется удаленный сервер, проверьте `base-url`, `token` и `client_id`.

## Контакт

Если нужен доступ или внедрение:

```text
grandfatherofny1984@gmail.com
```
