-- Создание таблицы пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,               
    login VARCHAR(255) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL       
);

-- Создание таблицы заметок
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,               
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
    content TEXT NOT NULL,              
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);
