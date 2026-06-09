# Ядро программы


## 1. Цель документа

Определить назначение Core-модуля и его ответственность в архитектуре.

---

## 2. Компоненты Core

- [EventBus](/project_documentation/Core/EventBus.md) — обмен событиями между модулями
- [ApplicationState](/project_documentation/Core/ApplicationState.md) — глобальное состояние приложения
- [Logger](/project_documentation/Core/Logger.md) — централизованное логирование
- [Config](/project_documentation/Core/Config.md) — загрузка и хранение настроек
- [ModuleRegistry](/project_documentation/Core/ModuleRegistry.md) — регистрация модулей и их контрактов

---

## 3. Application Lifecycle

Краткое описание жизненного цикла приложения:  
инициализация → главный цикл → завершение.

Подробные этапы описаны в отдельных документах:

- [Инициализация приложения](/project_documentation/Core/application_initialization.md)
- [Главный цикл приложения](/project_documentation/Core/application_main_loop.md)
- [Завершение работы](/project_documentation/Core/application_shutdown.md)

---

## 4. Принципы

- Модульность
- Событийная модель
- SOLID
- Независимость от UI и других модулей

---

## 5. Контракты Core

- Интерфейсы для модулей
- Формат событий
- Правила подписки/публикации

---

## 6. Потоки данных

Краткое описание: событие → обработка → изменение состояния → уведомление подписчиков.