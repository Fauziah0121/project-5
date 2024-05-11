CREATE TABLE public.users (
    user_id int4 NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    name varchar(100) NULL,
    city varchar(50) NULL,
    telp varchar(14) NULL,
    CONSTRAINT users_pkey1 PRIMARY KEY (user_id)
);
