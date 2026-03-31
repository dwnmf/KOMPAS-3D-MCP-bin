# KOMPAS-3D MCP
Код приглашения для первых 500 пользователей: invite-c716395c

Сайт активации: https://kompasmcp.ru

Поддержать проект: https://pay.cloudtips.ru/p/cdf123e9

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

1. Скачайте последний архив из Releases. https://github.com/dwnmf/KOMPAS-3D-MCP-bin/releases
3. Распакуйте его, например, в:

```text
C:\Programs\kompasmcp
```

3. Если вам уже выдали `config.json`, положите его сюда:

```text
%USERPROFILE%\.kompasmcp\config.json
```

4. Если `config.json` еще нет, выполните вход одной из команд ниже.

## Вход

Если у вас есть invite code(он в самом начале текста):

Заберите config.json с сайта https://kompasmcp.ru

После этого клиент создаст файл:

```text
%USERPROFILE%\.kompasmcp\config.json
```

## Подключение в MCP-клиенте

### CODEX(%USERPROFILE%\.codex\config.toml)

```text
[mcp_servers.kompas-3d]
command = "C:/Programs/kompasmcp/kompas-mcp.exe"
```

### Остальные клиенты (Claude, Roo Code, Cline)

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

## Что умеет

Ниже перечислены основные MCP tools, которые доступны клиенту KOMPAS-3D.

### 2D

- `create_document` - создает новый 2D-документ
- `open_document` - открывает существующий документ
- `save_document` - сохраняет 2D-документ
- `create_line` - создает отрезок
- `create_circle` - создает окружность
- `create_arc` - создает дугу
- `create_rectangle` - создает прямоугольник
- `create_point` - создает точку
- `create_polyline` - создает ломаную
- `create_regular_polygon` - создает правильный многоугольник
- `create_ellipse` - создает эллипс
- `create_ellipse_arc` - создает эллиптическую дугу
- `create_text` - добавляет текст
- `create_linear_dimension` - создает линейный размер
- `create_angle_dimension` - создает угловой размер
- `create_radius_dimension` - создает радиусный размер
- `create_diameter_dimension` - создает диаметральный размер
- `create_ordinate_dimension` - создает ординатный размер
- `create_chamfer` - строит фаску в 2D
- `create_fillet` - строит скругление в 2D
- `move_object` - перемещает объект
- `transform_object` - трансформирует объект
- `delete_object` - удаляет объект
- `symmetry_object` - зеркалит объект
- `list_objects` - показывает объекты в документе
- `get_object_info` - возвращает информацию об объекте
- `find_object_by_point` - ищет объект рядом с точкой
- `measure_distance` - измеряет расстояние
- `measure_length` - измеряет длину
- `measure_angle` - измеряет угол
- `measure_area` - измеряет площадь
- `check_intersection` - проверяет пересечение объектов

### 3D

- `create_document_3d` - создает новый 3D-документ
- `save_document_3d` - сохраняет 3D-модель
- `set_part_properties_3d` - задает свойства детали
- `get_3d_context` - возвращает текущее состояние 3D-документа
- `list_default_entities_3d` - показывает базовые сущности модели
- `create_offset_plane_3d` - создает смещенную плоскость
- `create_sketch_3d` - создает эскиз на плоскости
- `update_sketch_3d` - добавляет геометрию в эскиз
- `close_sketch_3d` - закрывает редактирование эскиза
- `create_extrude_boss_3d` - строит выдавливание
- `create_extrude_cut_3d` - строит вырез выдавливанием
- `create_revolve_boss_3d` - строит тело вращением
- `create_edge_fillet_3d` - строит 3D-скругление ребер
- `create_edge_chamfer_3d` - строит 3D-фаску ребер
- `create_cylindrical_helix_3d` - создает цилиндрическую спираль
- `create_sweep_cut_3d` - строит вырез по траектории
- `rebuild_model_3d` - перестраивает модель
- `list_feature_tree_3d` - показывает дерево построения
- `get_feature_info_3d` - возвращает информацию о feature
- `update_feature_3d` - обновляет feature
- `suppress_feature_3d` - подавляет feature
- `set_3d_view` - переключает вид камеры
- `list_faces_3d` - показывает грани модели
- `list_edges_3d` - показывает ребра модели

### Документы и экспорт

- `list_open_documents` - показывает открытые документы
- `get_active_document` - показывает активный документ
- `activate_document` - делает документ активным
- `close_document` - закрывает документ
- `close_all_documents` - закрывает все документы
- `close_all_except_documents` - закрывает все документы, кроме выбранных
- `create_view` - создает вид в 2D-документе
- `set_active_view` - переключает активный вид
- `create_layer` - создает слой
- `set_active_layer` - переключает активный слой
- `set_object_layer` - переносит объект на слой
- `fill_drawing_stamp` - заполняет штамп чертежа
- `export_to_dxf` - экспортирует документ в DXF
- `export_to_json` - экспортирует геометрию в JSON
- `screenshot_document` - делает скриншот документа
- `checkpoint_create` - создает checkpoint
- `checkpoint_restore` - восстанавливает состояние из checkpoint

### Скрипты и диагностика

- `execute_geometry_script` - выполняет геометрический сценарий через DSL
- `execute_python_script` - выполняет Python-сценарий внутри KOMPAS-3D
- `describe_tool` - показывает схему и описание инструмента
- `snapshot_state` - снимает состояние документа
- `snapshot_diff` - сравнивает состояния до и после
- `preflight_context` - проверяет контекст перед изменениями
- `resolve_selection_3d` - помогает выбрать 3D-сущности по описанию
- `safe_feature_create` - выполняет создание feature с дополнительными проверками

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
