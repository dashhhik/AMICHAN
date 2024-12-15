import React, { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

const VerifyMagicLink = () => {
    const { token } = useParams(); // Получаем токен из URL
    const navigate = useNavigate();

    useEffect(() => {
        const verifyToken = async () => {
            try {
                // Отправляем GET-запрос для верификации токена
                const response = await axios.get(
                    `http://0.0.0.0:8000/auth/verify_magic_link/${token}`
                );

                const jwtToken = response.data.token;

                // Сохраняем JWT-токен в localStorage
                localStorage.setItem("jwtToken", jwtToken);

                alert("Аутентификация успешна!");
                // Перенаправляем пользователя на главную страницу
                navigate("/");
            } catch (error) {
                console.error("Ошибка при верификации токена:", error);
                alert("Ссылка недействительна или устарела.");
                navigate("/auth"); // Перенаправление на страницу аутентификации
            }
        };

        verifyToken();
    }, [token, navigate]);

    return (
        <div style={styles.container}>
            <h1>Проверка ссылки...</h1>
            <p>Пожалуйста, подождите. Мы проверяем вашу ссылку для входа.</p>
        </div>
    );
};

// Inline-стили
const styles = {
    container: {
        textAlign: "center",
        marginTop: "50px",
        fontFamily: "Arial, sans-serif",
    },
};

export default VerifyMagicLink;
