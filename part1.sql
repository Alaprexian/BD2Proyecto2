Drop table books;

CREATE TABLE books (
    index SERIAL,
    title VARCHAR(255),
    genre VARCHAR(100),
    summary TEXT
);

select * from books;

SELECT count(*) FROM books;

-- Añadir columna tsvector combinada
ALTER TABLE books ADD COLUMN compuesto tsvector;

-- Llenar la columna combinada con los valores de title, genre y summary
UPDATE books SET compuesto = to_tsvector('english', title || ' ' || genre || ' ' || summary);

-- Crear el índice GIN en la columna compuesto
CREATE INDEX books_gin_idx ON books USING GIN(compuesto);

-- Insertar duplicados
INSERT INTO books (title, genre, summary, compuesto)
SELECT title, genre, summary, compuesto
FROM books;


EXPLAIN ANALYZE
SELECT title, ts_rank_cd(compuesto, query_w) AS rank
FROM books, to_tsquery('english', 'fantasy | nobility') query_w
WHERE query_w @@ compuesto
ORDER BY rank DESC
LIMIT 50;
