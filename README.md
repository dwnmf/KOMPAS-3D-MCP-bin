# KOMPAS-3D MCP Client

Готовый клиентский пакет для подключения к KOMPAS MCP на Windows.

В архиве вы получите:
- `kompas-mcp.exe`
- все нужные runtime-файлы
- `README.md`
- skill `kompas-mcp-operator`

## Что нужно заранее

- Windows
- установленный KOMPAS-3D
- MCP-клиент, который умеет запускать локальную команду

## Установка

1. Скачайте последний release-архив.
2. Распакуйте его в обычную папку, например:

```text
C:\Programs\kompasmcp
```

3. Если вам передали готовый `config.json`, положите его сюда:

```text
%USERPROFILE%\.kompasmcp\config.json
```

4. Если `config.json` вам не передали, используйте одну из команд ниже.

## Вход и настройка

### Вариант 1. Есть invite code

```bash
C:\Programs\kompasmcp\kompas-mcp.exe login --base-url https://your-host --invite-code XXXX-XXXX
```

### Вариант 2. Есть token и client_id

```bash
C:\Programs\kompasmcp\kompas-mcp.exe login --base-url https://your-host --token <token> --client-id <client-id>
```

После этого клиент сам создаст:

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

## Установка skill

В архиве есть:

```text
skills\kompas-mcp-operator
```

Скопируйте эту папку в:

```text
%USERPROFILE%\.codex\skills\kompas-mcp-operator
```

Этот skill помогает при работе с:
- 2D drawings
- 3D parts
- screenshots
- export
- runtime diagnosis

## Если ничего не работает

Проверьте по порядку:

1. `kompas-mcp.exe` действительно лежит в папке, из которой вы его запускаете.
2. `config.json` лежит в:

```text
%USERPROFILE%\.kompasmcp\config.json
```

3. KOMPAS-3D установлен на этой Windows-машине.
4. После логина вы перезапустили MCP-клиент.
5. Если используется удаленный сервер, проверьте правильность `base-url`, `token` и `client_id`.

## Контакт

Если нужен индивидуальный доступ или внедрение:

```text
grandfatherofny1984@gmail.com
```
