BEGIN;

CREATE SCHEMA til;

-- DROP TABLE til.notes;

CREATE TABLE til.notes (
  id serial
  ,start_message_id INT
  ,telegram_user_id INT
  ,telegram_username VARCHAR
  ,telegram_first_name VARCHAR
  ,telegram_last_name VARCHAR
  ,doc_text VARCHAR
  ,telegram_creation_date BIGINT
  ,is_draft BOOL DEFAULT TRUE
  ,_created_at BIGINT NOT NULL DEFAULT (extract(epoch FROM now())*1000)::BIGINT
  ,_updated_at BIGINT NOT NULL DEFAULT (extract(epoch FROM now())*1000)::BIGINT
);

COMMIT;