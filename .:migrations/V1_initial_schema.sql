--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.4

-- Started on 2022-09-28 17:48:48 +04

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE "CryptoBotDB";
--
-- TOC entry 3645 (class 1262 OID 16802)
-- Name: CryptoBotDB; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "CryptoBotDB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';


ALTER DATABASE "CryptoBotDB" OWNER TO postgres;

\connect "CryptoBotDB"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16832)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 3646 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16886)
-- Name: balance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.balance (
    profile_id uuid NOT NULL,
    currency_id smallint NOT NULL,
    total numeric(10,8)
);


ALTER TABLE public.balance OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16885)
-- Name: balance_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.balance_currency_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.balance_currency_id_seq OWNER TO postgres;

--
-- TOC entry 3647 (class 0 OID 0)
-- Dependencies: 215
-- Name: balance_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.balance_currency_id_seq OWNED BY public.balance.currency_id;


--
-- TOC entry 214 (class 1259 OID 16879)
-- Name: currency; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.currency (
    id smallint NOT NULL,
    name character varying(20) NOT NULL
);


ALTER TABLE public.currency OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16878)
-- Name: currency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.currency_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.currency_id_seq OWNER TO postgres;

--
-- TOC entry 3648 (class 0 OID 0)
-- Dependencies: 213
-- Name: currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.currency_id_seq OWNED BY public.currency.id;


--
-- TOC entry 210 (class 1259 OID 16843)
-- Name: profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profile (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text NOT NULL,
    tg_user_name character varying(50) NOT NULL
);


ALTER TABLE public.profile OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16902)
-- Name: transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction (
    profile_id uuid NOT NULL,
    date timestamp(0) with time zone NOT NULL,
    currency_id smallint NOT NULL,
    amount numeric(10,8) NOT NULL,
    transaction_type_id smallint NOT NULL
);


ALTER TABLE public.transaction OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16900)
-- Name: transaction_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_currency_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_currency_id_seq OWNER TO postgres;

--
-- TOC entry 3649 (class 0 OID 0)
-- Dependencies: 217
-- Name: transaction_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transaction_currency_id_seq OWNED BY public.transaction.currency_id;


--
-- TOC entry 218 (class 1259 OID 16901)
-- Name: transaction_transaction_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_transaction_type_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_transaction_type_id_seq OWNER TO postgres;

--
-- TOC entry 3650 (class 0 OID 0)
-- Dependencies: 218
-- Name: transaction_transaction_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transaction_transaction_type_id_seq OWNED BY public.transaction.transaction_type_id;


--
-- TOC entry 212 (class 1259 OID 16870)
-- Name: transaction_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction_type (
    id smallint NOT NULL,
    type text NOT NULL
);


ALTER TABLE public.transaction_type OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16869)
-- Name: transaction_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_type_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_type_id_seq OWNER TO postgres;

--
-- TOC entry 3651 (class 0 OID 0)
-- Dependencies: 211
-- Name: transaction_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transaction_type_id_seq OWNED BY public.transaction_type.id;


--
-- TOC entry 3465 (class 2604 OID 16889)
-- Name: balance currency_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.balance ALTER COLUMN currency_id SET DEFAULT nextval('public.balance_currency_id_seq'::regclass);


--
-- TOC entry 3464 (class 2604 OID 16882)
-- Name: currency id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency ALTER COLUMN id SET DEFAULT nextval('public.currency_id_seq'::regclass);


--
-- TOC entry 3466 (class 2604 OID 16905)
-- Name: transaction currency_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction ALTER COLUMN currency_id SET DEFAULT nextval('public.transaction_currency_id_seq'::regclass);


--
-- TOC entry 3467 (class 2604 OID 16906)
-- Name: transaction transaction_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction ALTER COLUMN transaction_type_id SET DEFAULT nextval('public.transaction_transaction_type_id_seq'::regclass);


--
-- TOC entry 3463 (class 2604 OID 16873)
-- Name: transaction_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_type ALTER COLUMN id SET DEFAULT nextval('public.transaction_type_id_seq'::regclass);


--
-- TOC entry 3636 (class 0 OID 16886)
-- Dependencies: 216
-- Data for Name: balance; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3634 (class 0 OID 16879)
-- Dependencies: 214
-- Data for Name: currency; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3630 (class 0 OID 16843)
-- Dependencies: 210
-- Data for Name: profile; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3639 (class 0 OID 16902)
-- Dependencies: 219
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3632 (class 0 OID 16870)
-- Dependencies: 212
-- Data for Name: transaction_type; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3652 (class 0 OID 0)
-- Dependencies: 215
-- Name: balance_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.balance_currency_id_seq', 1, false);


--
-- TOC entry 3653 (class 0 OID 0)
-- Dependencies: 213
-- Name: currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.currency_id_seq', 1, false);


--
-- TOC entry 3654 (class 0 OID 0)
-- Dependencies: 217
-- Name: transaction_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transaction_currency_id_seq', 1, false);


--
-- TOC entry 3655 (class 0 OID 0)
-- Dependencies: 218
-- Name: transaction_transaction_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transaction_transaction_type_id_seq', 1, false);


--
-- TOC entry 3656 (class 0 OID 0)
-- Dependencies: 211
-- Name: transaction_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transaction_type_id_seq', 1, false);


--
-- TOC entry 3481 (class 2606 OID 16884)
-- Name: currency currency__id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency__id_pkey PRIMARY KEY (id);


--
-- TOC entry 3483 (class 2606 OID 16927)
-- Name: currency currency_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_id_key UNIQUE (id) INCLUDE (id);


--
-- TOC entry 3485 (class 2606 OID 16929)
-- Name: currency currency_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_name_key UNIQUE (name) INCLUDE (name);


--
-- TOC entry 3469 (class 2606 OID 16923)
-- Name: profile profile_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_name_key UNIQUE (name) INCLUDE (name);


--
-- TOC entry 3471 (class 2606 OID 16850)
-- Name: profile profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (id);


--
-- TOC entry 3473 (class 2606 OID 16925)
-- Name: profile profile_tg_user_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_tg_user_name_key UNIQUE (tg_user_name) INCLUDE (tg_user_name);


--
-- TOC entry 3475 (class 2606 OID 16931)
-- Name: transaction_type transaction_type_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_type
    ADD CONSTRAINT transaction_type_id_key UNIQUE (id) INCLUDE (id);


--
-- TOC entry 3477 (class 2606 OID 16877)
-- Name: transaction_type transaction_type_id_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_type
    ADD CONSTRAINT transaction_type_id_pkey PRIMARY KEY (id);


--
-- TOC entry 3479 (class 2606 OID 16933)
-- Name: transaction_type transaction_type_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_type
    ADD CONSTRAINT transaction_type_type_key UNIQUE (type) INCLUDE (type);


--
-- TOC entry 3487 (class 2606 OID 16895)
-- Name: balance currency_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.balance
    ADD CONSTRAINT currency_id_fk FOREIGN KEY (currency_id) REFERENCES public.currency(id) NOT VALID;


--
-- TOC entry 3486 (class 2606 OID 16890)
-- Name: balance profile_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.balance
    ADD CONSTRAINT profile_id_fk FOREIGN KEY (profile_id) REFERENCES public.profile(id) NOT VALID;


--
-- TOC entry 3489 (class 2606 OID 16912)
-- Name: transaction transaction_currency_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_currency_id_fk FOREIGN KEY (currency_id) REFERENCES public.currency(id);


--
-- TOC entry 3490 (class 2606 OID 16917)
-- Name: transaction transaction_type_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_type_id_fk FOREIGN KEY (transaction_type_id) REFERENCES public.transaction_type(id);


--
-- TOC entry 3488 (class 2606 OID 16907)
-- Name: transaction transaction_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_user_id_fk FOREIGN KEY (profile_id) REFERENCES public.profile(id);


-- Completed on 2022-09-28 17:48:48 +04

--
-- PostgreSQL database dump complete
--

