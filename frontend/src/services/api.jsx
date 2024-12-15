import axios from "axios";

// Создаем инстанс axios с базовыми настройками
const api = axios.create({
    baseURL: "http://0.0.0.0:8000", // Базовый URL вашего API
    timeout: 5000, // Таймаут на запросы (5 секунд)
    headers: {
        "Content-Type": "application/json", // Устанавливаем тип содержимого по умолчанию
    },
});

// Добавляем interceptor для автоматического добавления JWT-токена
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("jwtToken"); // Получаем токен из localStorage
        if (token) {
            config.headers.Authorization = `Token ${token}`; // Добавляем токен в заголовок Authorization
        }
        return config;
    },
    (error) => {
        return Promise.reject(error); // Обрабатываем ошибку запроса
    }
);

// Добавляем interceptor для обработки ошибок ответов
api.interceptors.response.use(
    (response) => response, // Просто возвращаем ответ при успехе
    (error) => {
        if (error.response) {
            // Проверяем статус ошибки
            if (error.response.status === 401) {
                console.warn("Ошибка 401: Токен устарел или невалиден.");
                // Удаляем токен из localStorage
                localStorage.removeItem("jwtToken");
                // Перенаправляем пользователя на страницу аутентификации
                window.location.href = "/auth";
            } else if (error.response.status === 403) {
                console.warn("Ошибка 403: Доступ запрещен.");
            } else if (error.response.status === 500) {
                console.error("Ошибка 500: Внутренняя ошибка сервера.");
            }
        } else {
            console.error("Ошибка сети или таймаут запроса.");
        }
        return Promise.reject(error); // Возвращаем ошибку для дальнейшей обработки
    }
);

export default api;
