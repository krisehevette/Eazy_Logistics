# Описание ModuleRegistry

## 1. Назначение ModuleRegistry

**ModuleRegistry** — централизованный реестр модулей и их контрактов. Он отвечает за регистрацию модулей, хранение их интерфейсов, событий, зависимостей и предоставление доступа к контрактам другим частям системы.

ModuleRegistry создаётся на этапе **InitCore**, а наполняется на этапе **InitModules**.

---

## 2. Требования

- Один глобальный экземпляр
- Регистрация модулей только на этапе InitModules
- Хранение контрактов модулей (интерфейсы + события)
- Быстрый доступ к модулю по имени или типу
- Независимость от UI и других модулей
- Минимальные аллокации
- Отсутствие бизнес‑логики

---

## 3. Контракт модуля

Каждый модуль описывает свой контракт:
```cpp
struct ModuleContract {
    std::string name;
    std::vector<std::string> eventsPublished;
    std::vector<std::string> eventsSubscribed;
    void* interfacePtr; // указатель на интерфейс модуля
};
```

Требования:
- без виртуальных методов
- только данные
- интерфейс хранится как `void*` или `std::any`
- контракт не содержит логики

---

## 4. Интерфейс ModuleRegistry

### 4.1 Регистрация модуля
```cpp
void registerModule(const ModuleContract& contract);
```

### 4.2 Получение контракта по имени
```cpp
const ModuleContract* get(const std::string& name) const;
```

### 4.3 Проверка наличия модуля
```cpp
bool has(const std::string& name) const;
```

### 4.4 Перечень всех модулей
```cpp
std::vector<std::string> list() const;
```

---

## 5. Механизм работы

### 5.1 Хранение данных

Контракты модулей хранятся в хэш‑таблице:
```cpp
unordered_map<string, ModuleContract> modules;
```

Это обеспечивает O(1) доступ по имени.

### 5.2 Регистрация

На этапе InitModules каждый модуль:

- объявляет свой контракт
- указывает интерфейс
- перечисляет события, которые он публикует
- перечисляет события, которые он слушает
- регистрируется в ModuleRegistry

### 5.3 Доступ к интерфейсам

ModuleRegistry не знает, что такое модуль — он хранит только указатели на интерфейсы.

Пример:
```cpp
auto* email = registry.get("Email");
auto client = static_cast<IEmailClient*>(email->interfacePtr);
```

### 5.4 Потокобезопасность

- Регистрация происходит один раз при старте
- После старта — только чтение
- Мьютексы не требуются

---

## 6. Ограничения

- ModuleRegistry не создаёт модули
- ModuleRegistry не управляет их жизненным циклом
- ModuleRegistry не вызывает методы модулей
- ModuleRegistry не публикует события
- ModuleRegistry не зависит от EventBus, UI, Database и других модулей

---

## 7. Минимальный пример использования

### 7.1 Регистрация модуля
```cpp
ModuleContract emailContract;
emailContract.name = "Email";
emailContract.interfacePtr = static_cast<void*>(emailClient);
emailContract.eventsPublished = {"EmailFetched"};
emailContract.eventsSubscribed = {"ApplicationStarted"};

registry.registerModule(emailContract);
```

### 7.2 Получение интерфейса
```cpp
auto* contract = registry.get("Email");
auto* client = static_cast<IEmailClient*>(contract->interfacePtr);
client->fetch();
```

### 7.3 Проверка наличия
```cpp
if (registry.has("AI")) {
    // модуль существует
}
```

### 7.4 Перечень модулей
```cpp
for (auto& name : registry.list()) {
    logger.info("Module: " + name);
}
```
