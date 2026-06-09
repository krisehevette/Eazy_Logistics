# Описание ApplicationState


## 1. Назначение ApplicationState

**ApplicationState** — это централизованное хранилище глобального состояния приложения. Он содержит данные, которые отражают текущее состояние системы и обновляются модулями через события.

ApplicationState **не выполняет логику** — он только хранит данные и предоставляет безопасный доступ к ним.

---

## 2. Требования

- Единый экземпляр, создаваемый на этапе InitCore
- Только данные, никакой бизнес‑логики
- Потокобезопасный доступ к изменяемым полям
- Минимальные аллокации
- Независимость от UI и других модулей
- Обновление состояния только через события (EventBus)
- Быстрый доступ к данным (O(1) по ключу/полю)

---

## 3. Структура состояния

ApplicationState содержит набор структурированных данных, например:
```cpp
struct ApplicationState {
    EmailState email;
    LogisticsState logistics;
    DocumentState documents;
    UIState ui;
    // ...
};
```

Каждая подсекция — простая структура данных:
```cpp
struct EmailState {
    int unreadCount;
    std::vector<EmailMetadata> recentEmails;
};
```

Требования к данным:

- без виртуальных методов
- без логики
- только данные
- структуры должны быть лёгкими и сериализуемыми

---

## 4. Интерфейс ApplicationState

### 4.1 Получение состояния
```cpp
const ApplicationState& get() const;
```

### 4.2 Модификация состояния
```cpp
ApplicationState& mutate();
```

### 4.3 Потокобезопасность
```cpp
std::lock_guard<std::mutex> lock(mutex);
```

### 4.4 Подсекции
```cpp
EmailState& email();
LogisticsState& logistics();
DocumentState& documents();
```

---

## 5. Механизм работы

### 5.1 Хранение данных

Вся структура ApplicationState хранится в одном объекте:
```cpp
ApplicationState state;
```

Доступ к нему контролируется через Core.

### 5.2 Обновление состояния

Обновление происходит **только через события**, например:
- `EmailFetched` → обновить список писем
- `EmailClassified` → изменить статус
- `CargoUpdated` → обновить данные о грузе
- `DocumentGenerated` → добавить документ

Модуль не изменяет состояние напрямую — только через обработчики событий.

### 5.3 Потокобезопасность

- Чтение — без блокировок (если данные неизменяемые)
- Запись — через мьютекс
- Обновления атомарные на уровне секции

---

## 6. Ограничения

- ApplicationState не выполняет бизнес‑логику
- ApplicationState не публикует события
- ApplicationState не зависит от модулей
- ApplicationState не хранит тяжёлые объекты (БД, сокеты, UI‑элементы)
- ApplicationState не должен разрастаться до монолита — только необходимые данные

---

## 7. Минимальный пример использования

### 7.1 Чтение состояния
```cpp
auto& state = core.appState().get();
int unread = state.email.unreadCount;
```

### 7.2 Обновление состояния
```cpp
auto& state = core.appState().mutate();
state.email.unreadCount++;
```

### 7.3 Обработка события
```cpp
bus.subscribe<EmailFetched>([&](const EmailFetched& e) {
    auto& st = core.appState().mutate();
    st.email.recentEmails.push_back(e.metadata);
});
```
