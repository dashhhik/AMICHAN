CREATE TABLE board (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR NOT NULL,
                       description VARCHAR,
                       created_at TIMESTAMP NOT NULL,
                       updated_at TIMESTAMP NOT NULL,
                       threads_count INT NOT NULL DEFAULT 0
);

CREATE TABLE ban_list (
                          id SERIAL PRIMARY KEY,
                          email VARCHAR NOT NULL UNIQUE,
                          reason VARCHAR,
                          banned_at TIMESTAMP NOT NULL,
                          expires_at TIMESTAMP
);


CREATE TABLE thread (
                        id SERIAL PRIMARY KEY,
                        board_id INT NOT NULL REFERENCES board(id),

                        title VARCHAR NOT NULL,
                        content VARCHAR,
                        created_at TIMESTAMP NOT NULL,
                        replies_count INT NOT NULL DEFAULT 0,
                        nickname VARCHAR,
                        is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE post (
                      id SERIAL PRIMARY KEY,
                      thread_id INT NOT NULL REFERENCES thread(id),
                      parent_id INT REFERENCES post(id),
                      content VARCHAR NOT NULL,
                      created_at TIMESTAMP NOT NULL,
                      nickname VARCHAR,
                      is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
                      replies_count INT NOT NULL DEFAULT 0
);


CREATE TABLE file (
                      id SERIAL PRIMARY KEY,
                      thread_id INT NOT NULL REFERENCES thread(id),
                      file_path VARCHAR NOT NULL,
                      file_type VARCHAR,
                      created_at TIMESTAMP NOT NULL
);

CREATE TABLE role (
                      id SERIAL PRIMARY KEY,
                      name VARCHAR NOT NULL UNIQUE,
                      permissions VARCHAR
);

CREATE TABLE admins (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR NOT NULL UNIQUE,
                        password_hash VARCHAR NOT NULL,
                        role_id INT NOT NULL REFERENCES role(id)
);
