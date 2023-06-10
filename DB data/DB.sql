--
-- PostgreSQL database dump
--

-- Dumped from database version 14.8 (Homebrew)
-- Dumped by pg_dump version 14.8 (Homebrew)

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
-- Name: catalog_schema; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA catalog_schema;


ALTER SCHEMA catalog_schema OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: facility; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.facility (
    facility_id integer NOT NULL,
    region_id integer DEFAULT 0 NOT NULL
);


ALTER TABLE catalog_schema.facility OWNER TO admin;

--
-- Name: job_applications; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.job_applications (
    person_id integer,
    position_id integer,
    supermarket_id integer
);


ALTER TABLE catalog_schema.job_applications OWNER TO admin;

--
-- Name: people; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.people (
    person_id integer NOT NULL,
    person_name character varying,
    person_age integer,
    person_gender character varying,
    position_list_id integer
);


ALTER TABLE catalog_schema.people OWNER TO admin;

--
-- Name: position_list; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.position_list (
    position_list_id integer NOT NULL,
    position_id integer
);


ALTER TABLE catalog_schema.position_list OWNER TO admin;

--
-- Name: positions; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.positions (
    position_id integer NOT NULL,
    position_name character varying,
    sallary integer,
    work_hours integer
);


ALTER TABLE catalog_schema.positions OWNER TO admin;

--
-- Name: product; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.product (
    facility_id integer,
    quantity integer,
    product_id integer,
    creation_date date
);


ALTER TABLE catalog_schema.product OWNER TO admin;

--
-- Name: product_regional; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.product_regional (
    product_regional_id integer DEFAULT 0 NOT NULL,
    region_id integer DEFAULT 0 NOT NULL,
    product_id integer DEFAULT 0 NOT NULL,
    sell_price integer DEFAULT 0 NOT NULL,
    days_till_expire integer DEFAULT 0 NOT NULL,
    local_name character varying,
    order_price integer
);


ALTER TABLE catalog_schema.product_regional OWNER TO admin;

--
-- Name: region; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.region (
    region_id integer DEFAULT 0 NOT NULL,
    road_list_id integer
);


ALTER TABLE catalog_schema.region OWNER TO admin;

--
-- Name: road_list; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.road_list (
    road_list_id integer NOT NULL,
    a integer,
    b integer,
    dist integer
);


ALTER TABLE catalog_schema.road_list OWNER TO admin;

--
-- Name: sales_history; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.sales_history (
    product_id integer,
    quantity integer,
    date date,
    supermarket_id integer
);


ALTER TABLE catalog_schema.sales_history OWNER TO admin;

--
-- Name: stuff; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.stuff (
    person_id integer,
    supermarket_id integer,
    position_id integer
);


ALTER TABLE catalog_schema.stuff OWNER TO admin;

--
-- Name: supermarket; Type: TABLE; Schema: catalog_schema; Owner: admin
--

CREATE TABLE catalog_schema.supermarket (
    supermarket_id integer DEFAULT 0 NOT NULL,
    facility_id integer DEFAULT 0 NOT NULL
);


ALTER TABLE catalog_schema.supermarket OWNER TO admin;

--
-- Name: contract; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.contract (
    contract_id integer NOT NULL,
    position_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
);


ALTER TABLE public.contract OWNER TO admin;

--
-- Name: deliveries_history; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.deliveries_history (
    delivery_id integer NOT NULL,
    delivery_date date NOT NULL,
    supermarket_id integer NOT NULL,
    order_id integer
);


ALTER TABLE public.deliveries_history OWNER TO admin;

--
-- Name: employment_history; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.employment_history (
    employment_history_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE public.employment_history OWNER TO admin;

--
-- Name: facility; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.facility (
    facility_id integer NOT NULL,
    region_id integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.facility OWNER TO admin;

--
-- Name: item; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.item (
    item_id integer NOT NULL,
    facility_id integer,
    expiry_date date,
    product_regional_id integer NOT NULL
);


ALTER TABLE public.item OWNER TO admin;

--
-- Name: job_applications; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.job_applications (
    person_id integer,
    position_id integer,
    supermarket_id integer
);


ALTER TABLE public.job_applications OWNER TO admin;

--
-- Name: order_history; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.order_history (
    order_id integer NOT NULL,
    facility_id integer NOT NULL,
    buy_price integer NOT NULL,
    order_date date NOT NULL
);


ALTER TABLE public.order_history OWNER TO admin;

--
-- Name: people; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.people (
    person_id integer NOT NULL,
    person_first_name character varying(20),
    person_last_name character varying(20),
    person_date_of_birth date,
    person_gender character varying(10)
);


ALTER TABLE public.people OWNER TO admin;

--
-- Name: positions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.positions (
    position_id integer NOT NULL,
    position_name character varying(20),
    salary numeric(7,2),
    work_hours integer
);


ALTER TABLE public.positions OWNER TO admin;

--
-- Name: price_change; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.price_change (
    price_change_id integer NOT NULL,
    product_regional_id integer NOT NULL,
    new_price integer NOT NULL,
    date date NOT NULL,
    old_price integer NOT NULL
);


ALTER TABLE public.price_change OWNER TO admin;

--
-- Name: product_regional; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.product_regional (
    product_regional_id integer DEFAULT 0 NOT NULL,
    region_id integer DEFAULT 0 NOT NULL,
    sell_price numeric(5,2) DEFAULT 0.00 NOT NULL,
    local_name character varying(10),
    order_price numeric(5,2) DEFAULT 0.00 NOT NULL,
    expiry_time integer NOT NULL
);


ALTER TABLE public.product_regional OWNER TO admin;

--
-- Name: region; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.region (
    region_id integer NOT NULL,
    region_name character varying(100),
    road_list_id integer DEFAULT 0
);


ALTER TABLE public.region OWNER TO admin;

--
-- Name: region_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.region_id_seq OWNER TO admin;

--
-- Name: region_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.region_id_seq OWNED BY public.region.region_id;


--
-- Name: requested_position; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.requested_position (
    requested_position_id integer NOT NULL,
    position_id integer,
    supermarket_id integer NOT NULL
);


ALTER TABLE public.requested_position OWNER TO admin;

--
-- Name: road_list; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.road_list (
    road_list_id integer NOT NULL,
    id_from integer,
    id_to integer,
    dist integer
);


ALTER TABLE public.road_list OWNER TO admin;

--
-- Name: sales_history; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.sales_history (
    product_id integer,
    quantity integer,
    date date,
    supermarket_id integer
);


ALTER TABLE public.sales_history OWNER TO admin;

--
-- Name: stuff; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.stuff (
    person_id integer,
    supermarket_id integer,
    position_id integer
);


ALTER TABLE public.stuff OWNER TO admin;

--
-- Name: supermarket; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.supermarket (
    supermarket_id integer DEFAULT 0 NOT NULL,
    supermarket_name character varying(20),
    facility_id integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.supermarket OWNER TO admin;

--
-- Data for Name: facility; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.facility (facility_id, region_id) FROM stdin;
\.


--
-- Data for Name: job_applications; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.job_applications (person_id, position_id, supermarket_id) FROM stdin;
\.


--
-- Data for Name: people; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.people (person_id, person_name, person_age, person_gender, position_list_id) FROM stdin;
\.


--
-- Data for Name: position_list; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.position_list (position_list_id, position_id) FROM stdin;
\.


--
-- Data for Name: positions; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.positions (position_id, position_name, sallary, work_hours) FROM stdin;
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.product (facility_id, quantity, product_id, creation_date) FROM stdin;
\.


--
-- Data for Name: product_regional; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.product_regional (product_regional_id, region_id, product_id, sell_price, days_till_expire, local_name, order_price) FROM stdin;
\.


--
-- Data for Name: region; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.region (region_id, road_list_id) FROM stdin;
\.


--
-- Data for Name: road_list; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.road_list (road_list_id, a, b, dist) FROM stdin;
\.


--
-- Data for Name: sales_history; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.sales_history (product_id, quantity, date, supermarket_id) FROM stdin;
\.


--
-- Data for Name: stuff; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.stuff (person_id, supermarket_id, position_id) FROM stdin;
\.


--
-- Data for Name: supermarket; Type: TABLE DATA; Schema: catalog_schema; Owner: admin
--

COPY catalog_schema.supermarket (supermarket_id, facility_id) FROM stdin;
\.


--
-- Data for Name: contract; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.contract (contract_id, position_id, start_date, end_date) FROM stdin;
\.


--
-- Data for Name: deliveries_history; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.deliveries_history (delivery_id, delivery_date, supermarket_id, order_id) FROM stdin;
\.


--
-- Data for Name: employment_history; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.employment_history (employment_history_id, person_id) FROM stdin;
\.


--
-- Data for Name: facility; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.facility (facility_id, region_id) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
11	11
12	12
13	13
14	14
15	15
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.item (item_id, facility_id, expiry_date, product_regional_id) FROM stdin;
1009	9	2023-01-09	3
1005	5	2023-01-05	4
1004	4	2023-01-04	3
1013	13	2023-01-13	14
1011	11	2023-01-11	8
1014	14	2023-01-14	1
1007	7	2023-01-07	7
1008	8	2023-01-08	11
1012	12	2023-01-12	2
1006	6	2023-01-06	6
1010	10	2023-01-10	2
1003	3	2023-01-03	2
1015	15	2023-01-15	2
\.


--
-- Data for Name: job_applications; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.job_applications (person_id, position_id, supermarket_id) FROM stdin;
1	1	1
2	2	2
3	3	3
4	4	4
5	5	5
6	6	6
7	7	7
8	8	8
9	9	9
10	10	10
11	11	11
12	12	12
13	13	13
14	14	14
15	15	15
\.


--
-- Data for Name: order_history; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.order_history (order_id, facility_id, buy_price, order_date) FROM stdin;
\.


--
-- Data for Name: people; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.people (person_id, person_first_name, person_last_name, person_date_of_birth, person_gender) FROM stdin;
1	John	Doe	1990-01-01	Male
2	Jane	Smith	1992-03-15	Female
3	David	Johnson	1988-07-10	Male
4	Sarah	Williams	1995-05-20	Female
5	Michael	Brown	1993-09-05	Male
6	Emily	Davis	1991-02-12	Female
7	Daniel	Miller	1989-06-25	Male
8	Olivia	Anderson	1994-04-18	Female
9	James	Taylor	1992-08-10	Male
10	Sophia	Wilson	1993-12-05	Female
11	Benjamin	Thompson	1995-03-20	Male
12	Ava	Clark	1990-07-15	Female
13	William	Walker	1988-11-08	Male
14	Mia	Harris	1991-09-02	Female
15	Liam	Lewis	1994-01-28	Male
\.


--
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.positions (position_id, position_name, salary, work_hours) FROM stdin;
1	Position 1	5000.00	40
2	Position 2	4000.00	35
3	Position 3	6000.00	45
4	Position 4	5500.00	38
5	Position 5	4500.00	37
6	Position 6	5200.00	42
7	Position 7	4800.00	36
8	Position 8	5800.00	43
9	Position 9	5100.00	39
10	Position 10	4700.00	34
11	Position 11	5300.00	41
12	Position 12	4900.00	35
13	Position 13	5700.00	42
14	Position 14	5200.00	37
15	Position 15	5600.00	44
\.


--
-- Data for Name: price_change; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.price_change (price_change_id, product_regional_id, new_price, date, old_price) FROM stdin;
\.


--
-- Data for Name: product_regional; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.product_regional (product_regional_id, region_id, sell_price, local_name, order_price, expiry_time) FROM stdin;
4	4	12.99	Product 4	11.99	5
12	12	10.99	Product 12	9.99	5
8	8	11.50	Product 8	10.50	4
6	6	9.99	Product 6	8.99	3
1	1	10.99	Product 1	9.99	3
10	10	8.75	Product 10	7.75	1
15	15	11.75	Product 15	10.75	1
13	13	13.50	Product 13	12.50	6
14	14	17.99	Product 14	16.99	4
5	5	6.75	Product 5	5.75	3
11	11	7.99	Product 11	6.99	3
3	3	8.50	Product 3	7.50	1
9	9	15.99	Product 9	14.99	5
2	2	5.99	Product 2	4.99	4
7	7	7.99	Product 7	6.99	2
16	1	2.00	123	2.00	2
17	1	5.00	567	5.00	5
18	1	4.00	444	4.00	4
19	1	4.00	435	4.00	4
20	1	4.00	43543	4.00	4
21	2	2.00	Goofy	3.00	1
22	1	2.00	aboba	2.00	8
23	1	2.00	adsa	2.00	2
\.


--
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.region (region_id, region_name, road_list_id) FROM stdin;
1	Region A	1
2	Region B	2
3	Region C	3
4	Region D	4
5	Region E	5
6	Region F	6
7	Region G	7
8	Region H	8
9	Region I	9
10	Region J	10
11	Region K	11
12	Region L	12
13	Region M	13
14	Region N	14
15	Region O	15
0	Region ABOBA	1
\.


--
-- Data for Name: requested_position; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.requested_position (requested_position_id, position_id, supermarket_id) FROM stdin;
\.


--
-- Data for Name: road_list; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.road_list (road_list_id, id_from, id_to, dist) FROM stdin;
1	10	20	100
2	15	25	150
3	12	22	120
4	18	28	180
5	11	21	110
6	30	40	200
7	35	45	250
8	32	42	220
9	38	48	280
10	31	41	210
11	50	60	300
12	55	65	350
13	52	62	320
14	58	68	380
15	51	61	310
\.


--
-- Data for Name: sales_history; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.sales_history (product_id, quantity, date, supermarket_id) FROM stdin;
1001	10	2023-06-01	1
1002	8	2023-06-02	2
1003	15	2023-06-03	3
1004	12	2023-06-04	4
1005	5	2023-06-05	5
1006	7	2023-06-06	6
1007	9	2023-06-07	7
1008	11	2023-06-08	8
1009	13	2023-06-09	9
1010	6	2023-06-10	10
1011	8	2023-06-11	11
1012	10	2023-06-12	12
1013	12	2023-06-13	13
1014	14	2023-06-14	14
1015	16	2023-06-15	15
\.


--
-- Data for Name: stuff; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.stuff (person_id, supermarket_id, position_id) FROM stdin;
1	1	1
2	2	2
3	3	3
4	4	4
5	5	5
6	6	6
7	7	7
8	8	8
9	9	9
10	10	10
11	11	11
12	12	12
13	13	13
14	14	14
15	15	15
\.


--
-- Data for Name: supermarket; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.supermarket (supermarket_id, supermarket_name, facility_id) FROM stdin;
1	Supermarket 1	1
2	Supermarket 2	2
3	Supermarket 3	3
4	Supermarket 4	4
5	Supermarket 5	5
6	Supermarket 6	6
7	Supermarket 7	7
8	Supermarket 8	8
9	Supermarket 9	9
10	Supermarket 10	10
11	Supermarket 11	11
12	Supermarket 12	12
13	Supermarket 13	13
14	Supermarket 14	14
15	Supermarket 15	15
17	123213	1
18	Product 228	2
19	34	6
21	345	1
\.


--
-- Name: region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.region_id_seq', 1, false);


--
-- Name: facility facility_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.facility
    ADD CONSTRAINT facility_pk PRIMARY KEY (facility_id);


--
-- Name: people people_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.people
    ADD CONSTRAINT people_pk PRIMARY KEY (person_id);


--
-- Name: position_list position_list_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.position_list
    ADD CONSTRAINT position_list_pk PRIMARY KEY (position_list_id);


--
-- Name: positions positions_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.positions
    ADD CONSTRAINT positions_pk PRIMARY KEY (position_id);


--
-- Name: product_regional product_regional_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.product_regional
    ADD CONSTRAINT product_regional_pk PRIMARY KEY (product_regional_id);


--
-- Name: region region_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.region
    ADD CONSTRAINT region_pk PRIMARY KEY (region_id);


--
-- Name: road_list road_list_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.road_list
    ADD CONSTRAINT road_list_pk PRIMARY KEY (road_list_id);


--
-- Name: supermarket supermarket_pk; Type: CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.supermarket
    ADD CONSTRAINT supermarket_pk PRIMARY KEY (supermarket_id);


--
-- Name: contract contract_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.contract
    ADD CONSTRAINT contract_pk PRIMARY KEY (contract_id);


--
-- Name: deliveries_history deliveries_history_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.deliveries_history
    ADD CONSTRAINT deliveries_history_pk PRIMARY KEY (delivery_id);


--
-- Name: employment_history employment_history_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employment_history
    ADD CONSTRAINT employment_history_pk PRIMARY KEY (employment_history_id);


--
-- Name: facility facility_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.facility
    ADD CONSTRAINT facility_pk PRIMARY KEY (facility_id);


--
-- Name: item item_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pk PRIMARY KEY (item_id);


--
-- Name: order_history order_history_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.order_history
    ADD CONSTRAINT order_history_pk PRIMARY KEY (order_id);


--
-- Name: people people_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.people
    ADD CONSTRAINT people_pk PRIMARY KEY (person_id);


--
-- Name: positions positions_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pk PRIMARY KEY (position_id);


--
-- Name: price_change price_change_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.price_change
    ADD CONSTRAINT price_change_pk PRIMARY KEY (price_change_id);


--
-- Name: product_regional product_regional_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.product_regional
    ADD CONSTRAINT product_regional_pk PRIMARY KEY (product_regional_id);


--
-- Name: region region_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_pk PRIMARY KEY (region_id);


--
-- Name: requested_position requested_position_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.requested_position
    ADD CONSTRAINT requested_position_pk PRIMARY KEY (requested_position_id);


--
-- Name: road_list road_list_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.road_list
    ADD CONSTRAINT road_list_pk PRIMARY KEY (road_list_id);


--
-- Name: supermarket supermarket_pk; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.supermarket
    ADD CONSTRAINT supermarket_pk PRIMARY KEY (supermarket_id);


--
-- Name: facility facility_region_region_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.facility
    ADD CONSTRAINT facility_region_region_id_fk FOREIGN KEY (region_id) REFERENCES catalog_schema.region(region_id);


--
-- Name: job_applications job_applications_people_person_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.job_applications
    ADD CONSTRAINT job_applications_people_person_id_fk FOREIGN KEY (person_id) REFERENCES catalog_schema.people(person_id);


--
-- Name: job_applications job_applications_positions_position_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.job_applications
    ADD CONSTRAINT job_applications_positions_position_id_fk FOREIGN KEY (position_id) REFERENCES catalog_schema.positions(position_id);


--
-- Name: job_applications job_applications_supermarket_supermarket_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.job_applications
    ADD CONSTRAINT job_applications_supermarket_supermarket_id_fk FOREIGN KEY (supermarket_id) REFERENCES catalog_schema.supermarket(supermarket_id);


--
-- Name: people people_position_list_position_list_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.people
    ADD CONSTRAINT people_position_list_position_list_id_fk FOREIGN KEY (position_list_id) REFERENCES catalog_schema.position_list(position_list_id);


--
-- Name: position_list position_list_positions_position_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.position_list
    ADD CONSTRAINT position_list_positions_position_id_fk FOREIGN KEY (position_id) REFERENCES catalog_schema.positions(position_id);


--
-- Name: product product_facility_facility_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.product
    ADD CONSTRAINT product_facility_facility_id_fk FOREIGN KEY (facility_id) REFERENCES catalog_schema.facility(facility_id);


--
-- Name: product_regional product_regional_region_region_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.product_regional
    ADD CONSTRAINT product_regional_region_region_id_fk FOREIGN KEY (region_id) REFERENCES catalog_schema.region(region_id);


--
-- Name: region region_road_list_road_list_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.region
    ADD CONSTRAINT region_road_list_road_list_id_fk FOREIGN KEY (road_list_id) REFERENCES catalog_schema.road_list(road_list_id);


--
-- Name: sales_history sales_history_supermarket_supermarket_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.sales_history
    ADD CONSTRAINT sales_history_supermarket_supermarket_id_fk FOREIGN KEY (supermarket_id) REFERENCES catalog_schema.supermarket(supermarket_id);


--
-- Name: stuff stuff_people_person_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.stuff
    ADD CONSTRAINT stuff_people_person_id_fk FOREIGN KEY (person_id) REFERENCES catalog_schema.people(person_id);


--
-- Name: stuff stuff_positions_position_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.stuff
    ADD CONSTRAINT stuff_positions_position_id_fk FOREIGN KEY (position_id) REFERENCES catalog_schema.positions(position_id);


--
-- Name: stuff stuff_supermarket_supermarket_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.stuff
    ADD CONSTRAINT stuff_supermarket_supermarket_id_fk FOREIGN KEY (supermarket_id) REFERENCES catalog_schema.supermarket(supermarket_id);


--
-- Name: supermarket supermarket_facility_facility_id_fk; Type: FK CONSTRAINT; Schema: catalog_schema; Owner: admin
--

ALTER TABLE ONLY catalog_schema.supermarket
    ADD CONSTRAINT supermarket_facility_facility_id_fk FOREIGN KEY (facility_id) REFERENCES catalog_schema.facility(facility_id);


--
-- Name: order_history facility_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.order_history
    ADD CONSTRAINT facility_id FOREIGN KEY (facility_id) REFERENCES public.facility(facility_id);


--
-- Name: facility facility_region_region_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.facility
    ADD CONSTRAINT facility_region_region_id_fk FOREIGN KEY (region_id) REFERENCES public.region(region_id);


--
-- Name: item item_facility_facility_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_facility_facility_id_fk FOREIGN KEY (facility_id) REFERENCES public.facility(facility_id);


--
-- Name: job_applications job_applications_people_person_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_people_person_id_fk FOREIGN KEY (person_id) REFERENCES public.people(person_id);


--
-- Name: job_applications job_applications_positions_position_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_positions_position_id_fk FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- Name: job_applications job_applications_supermarket_supermarket_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_supermarket_supermarket_id_fk FOREIGN KEY (supermarket_id) REFERENCES public.supermarket(supermarket_id);


--
-- Name: deliveries_history order_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.deliveries_history
    ADD CONSTRAINT order_id FOREIGN KEY (order_id) REFERENCES public.order_history(order_id);


--
-- Name: employment_history person_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.employment_history
    ADD CONSTRAINT person_id FOREIGN KEY (person_id) REFERENCES public.people(person_id);


--
-- Name: requested_position position_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.requested_position
    ADD CONSTRAINT position_id FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- Name: contract position_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.contract
    ADD CONSTRAINT position_id FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- Name: item product_regional_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT product_regional_id FOREIGN KEY (product_regional_id) REFERENCES public.product_regional(product_regional_id);


--
-- Name: price_change product_regional_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.price_change
    ADD CONSTRAINT product_regional_id FOREIGN KEY (product_regional_id) REFERENCES public.product_regional(product_regional_id);


--
-- Name: product_regional product_regional_region_region_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.product_regional
    ADD CONSTRAINT product_regional_region_region_id_fk FOREIGN KEY (region_id) REFERENCES public.region(region_id);


--
-- Name: region region_road_list_road_list_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_road_list_road_list_id_fk FOREIGN KEY (road_list_id) REFERENCES public.road_list(road_list_id);


--
-- Name: sales_history sales_history_supermarket_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.sales_history
    ADD CONSTRAINT sales_history_supermarket_id_fk FOREIGN KEY (supermarket_id) REFERENCES public.supermarket(supermarket_id);


--
-- Name: stuff stuff_people_person_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stuff
    ADD CONSTRAINT stuff_people_person_id_fk FOREIGN KEY (person_id) REFERENCES public.people(person_id);


--
-- Name: stuff stuff_positions_position_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stuff
    ADD CONSTRAINT stuff_positions_position_id_fk FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- Name: stuff stuff_supermarket_supermarket_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stuff
    ADD CONSTRAINT stuff_supermarket_supermarket_id_fk FOREIGN KEY (supermarket_id) REFERENCES public.supermarket(supermarket_id);


--
-- Name: supermarket supermarket_facility_facility_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.supermarket
    ADD CONSTRAINT supermarket_facility_facility_id_fk FOREIGN KEY (facility_id) REFERENCES public.facility(facility_id);


--
-- Name: requested_position supermarket_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.requested_position
    ADD CONSTRAINT supermarket_id FOREIGN KEY (supermarket_id) REFERENCES public.supermarket(supermarket_id);


--
-- Name: deliveries_history supermarket_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.deliveries_history
    ADD CONSTRAINT supermarket_id FOREIGN KEY (supermarket_id) REFERENCES public.supermarket(supermarket_id);


--
-- PostgreSQL database dump complete
--

