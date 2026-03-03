--
-- PostgreSQL database dump
--

\restrict Y3c2L9sZQqb48V9MsfMrmDFhD9QGXnakNLUEywGUI6E69OixeBnTXxkyA4f9Afu

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

-- Started on 2026-03-03 11:21:19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 17114)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 5103 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- TOC entry 250 (class 1255 OID 17031)
-- Name: reduce_stock(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.reduce_stock() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE stock
    SET quantity = quantity - NEW.quantity
    WHERE branch_id = (SELECT branch_id FROM sales WHERE sale_id = NEW.sale_id)
    AND medicine_id = NEW.medicine_id;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.reduce_stock() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 243 (class 1259 OID 17073)
-- Name: ai_safety_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_safety_logs (
    log_id integer NOT NULL,
    sale_id integer,
    medicine_id integer,
    warning_message text,
    log_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.ai_safety_logs OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 17072)
-- Name: ai_safety_logs_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_safety_logs_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_safety_logs_log_id_seq OWNER TO postgres;

--
-- TOC entry 5104 (class 0 OID 0)
-- Dependencies: 242
-- Name: ai_safety_logs_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_safety_logs_log_id_seq OWNED BY public.ai_safety_logs.log_id;


--
-- TOC entry 221 (class 1259 OID 16876)
-- Name: branches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branches (
    branch_id integer NOT NULL,
    branch_name character varying(100) NOT NULL,
    address character varying(255),
    phone character varying(20)
);


ALTER TABLE public.branches OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16875)
-- Name: branches_branch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.branches ALTER COLUMN branch_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.branches_branch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 247 (class 1259 OID 17164)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    name character varying(100),
    phone character varying(20),
    email character varying(150)
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 17163)
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_customer_id_seq OWNER TO postgres;

--
-- TOC entry 5105 (class 0 OID 0)
-- Dependencies: 246
-- Name: customers_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;


--
-- TOC entry 227 (class 1259 OID 16914)
-- Name: medicines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medicines (
    medicine_id integer NOT NULL,
    medicine_name character varying(150) NOT NULL,
    description text,
    unit_price numeric(10,2) NOT NULL,
    requires_prescription boolean DEFAULT false
);


ALTER TABLE public.medicines OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16913)
-- Name: medicines_medicine_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.medicines ALTER COLUMN medicine_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.medicines_medicine_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 249 (class 1259 OID 17172)
-- Name: message_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message_logs (
    log_id integer NOT NULL,
    customer_id integer,
    sale_id integer,
    message_text text,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.message_logs OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 17171)
-- Name: message_logs_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_logs_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.message_logs_log_id_seq OWNER TO postgres;

--
-- TOC entry 5106 (class 0 OID 0)
-- Dependencies: 248
-- Name: message_logs_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_logs_log_id_seq OWNED BY public.message_logs.log_id;


--
-- TOC entry 241 (class 1259 OID 17059)
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    payment_id integer NOT NULL,
    sale_id integer,
    payment_method character varying(50),
    payment_status character varying(50),
    payment_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 17058)
-- Name: payments_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_payment_id_seq OWNER TO postgres;

--
-- TOC entry 5107 (class 0 OID 0)
-- Dependencies: 240
-- Name: payments_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments.payment_id;


--
-- TOC entry 237 (class 1259 OID 17017)
-- Name: prescriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prescriptions (
    prescription_id integer NOT NULL,
    sale_id integer NOT NULL,
    patient_name character varying(100),
    doctor_name character varying(100),
    prescription_date date,
    notes text
);


ALTER TABLE public.prescriptions OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17016)
-- Name: prescriptions_prescription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.prescriptions ALTER COLUMN prescription_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.prescriptions_prescription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 239 (class 1259 OID 17034)
-- Name: purchase_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.purchase_items (
    purchase_item_id integer NOT NULL,
    purchase_id integer NOT NULL,
    medicine_id integer NOT NULL,
    quantity integer NOT NULL,
    cost_price numeric(10,2)
);


ALTER TABLE public.purchase_items OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17033)
-- Name: purchase_items_purchase_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.purchase_items ALTER COLUMN purchase_item_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.purchase_items_purchase_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 229 (class 1259 OID 16926)
-- Name: purchases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.purchases (
    purchase_id integer NOT NULL,
    branch_id integer NOT NULL,
    supplier_id integer NOT NULL,
    recorded_by integer NOT NULL,
    purchase_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    total_amount numeric(12,2)
);


ALTER TABLE public.purchases OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16925)
-- Name: purchases_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.purchases ALTER COLUMN purchase_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.purchases_purchase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 235 (class 1259 OID 16996)
-- Name: sale_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sale_items (
    sale_item_id integer NOT NULL,
    sale_id integer NOT NULL,
    medicine_id integer NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    subtotal numeric(12,2),
    CONSTRAINT check_quantity_positive CHECK ((quantity > 0))
);


ALTER TABLE public.sale_items OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16995)
-- Name: sale_items_sale_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.sale_items ALTER COLUMN sale_item_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.sale_items_sale_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 233 (class 1259 OID 16976)
-- Name: sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales (
    sale_id integer NOT NULL,
    branch_id integer NOT NULL,
    performed_by integer NOT NULL,
    sale_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    total_amount numeric(12,2),
    customer_id integer NOT NULL
);


ALTER TABLE public.sales OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16975)
-- Name: sales_sale_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.sales ALTER COLUMN sale_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.sales_sale_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 231 (class 1259 OID 16952)
-- Name: stock; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock (
    stock_id integer NOT NULL,
    branch_id integer NOT NULL,
    medicine_id integer NOT NULL,
    quantity integer DEFAULT 0 NOT NULL,
    last_updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_stock_positive CHECK ((quantity >= 0))
);


ALTER TABLE public.stock OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 17089)
-- Name: stock_batches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stock_batches (
    batch_id integer NOT NULL,
    branch_id integer NOT NULL,
    medicine_id integer NOT NULL,
    batch_number character varying(50),
    quantity integer NOT NULL,
    cost_price numeric(10,2) NOT NULL,
    expiry_date date
);


ALTER TABLE public.stock_batches OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17088)
-- Name: stock_batches_batch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.stock_batches ALTER COLUMN batch_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.stock_batches_batch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 16951)
-- Name: stock_stock_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.stock ALTER COLUMN stock_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.stock_stock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 223 (class 1259 OID 16884)
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.suppliers (
    supplier_id integer NOT NULL,
    supplier_name character varying(100) NOT NULL,
    contact_person character varying(100),
    phone character varying(20),
    email character varying(100),
    address character varying(255)
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16883)
-- Name: suppliers_supplier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.suppliers ALTER COLUMN supplier_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.suppliers_supplier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 16894)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    branch_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    role character varying(50),
    username character varying(50) NOT NULL,
    password text NOT NULL,
    email character varying(150)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16893)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4871 (class 2604 OID 17076)
-- Name: ai_safety_logs log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_safety_logs ALTER COLUMN log_id SET DEFAULT nextval('public.ai_safety_logs_log_id_seq'::regclass);


--
-- TOC entry 4873 (class 2604 OID 17167)
-- Name: customers customer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);


--
-- TOC entry 4874 (class 2604 OID 17175)
-- Name: message_logs log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_logs ALTER COLUMN log_id SET DEFAULT nextval('public.message_logs_log_id_seq'::regclass);


--
-- TOC entry 4869 (class 2604 OID 17062)
-- Name: payments payment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN payment_id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);


--
-- TOC entry 4910 (class 2606 OID 17082)
-- Name: ai_safety_logs ai_safety_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_safety_logs
    ADD CONSTRAINT ai_safety_logs_pkey PRIMARY KEY (log_id);


--
-- TOC entry 4879 (class 2606 OID 16882)
-- Name: branches branches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_pkey PRIMARY KEY (branch_id);


--
-- TOC entry 4914 (class 2606 OID 17170)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- TOC entry 4890 (class 2606 OID 16924)
-- Name: medicines medicines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicines
    ADD CONSTRAINT medicines_pkey PRIMARY KEY (medicine_id);


--
-- TOC entry 4918 (class 2606 OID 17181)
-- Name: message_logs message_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_logs
    ADD CONSTRAINT message_logs_pkey PRIMARY KEY (log_id);


--
-- TOC entry 4908 (class 2606 OID 17066)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);


--
-- TOC entry 4904 (class 2606 OID 17025)
-- Name: prescriptions prescriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_pkey PRIMARY KEY (prescription_id);


--
-- TOC entry 4906 (class 2606 OID 17042)
-- Name: purchase_items purchase_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_items
    ADD CONSTRAINT purchase_items_pkey PRIMARY KEY (purchase_item_id);


--
-- TOC entry 4892 (class 2606 OID 16935)
-- Name: purchases purchases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (purchase_id);


--
-- TOC entry 4902 (class 2606 OID 17005)
-- Name: sale_items sale_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale_items
    ADD CONSTRAINT sale_items_pkey PRIMARY KEY (sale_item_id);


--
-- TOC entry 4900 (class 2606 OID 16984)
-- Name: sales sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (sale_id);


--
-- TOC entry 4912 (class 2606 OID 17098)
-- Name: stock_batches stock_batches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_batches
    ADD CONSTRAINT stock_batches_pkey PRIMARY KEY (batch_id);


--
-- TOC entry 4895 (class 2606 OID 16962)
-- Name: stock stock_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (stock_id);


--
-- TOC entry 4881 (class 2606 OID 16892)
-- Name: suppliers suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id);


--
-- TOC entry 4897 (class 2606 OID 16964)
-- Name: stock unique_branch_medicine; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock
    ADD CONSTRAINT unique_branch_medicine UNIQUE (branch_id, medicine_id);


--
-- TOC entry 4916 (class 2606 OID 17255)
-- Name: customers unique_customer_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT unique_customer_email UNIQUE (email);


--
-- TOC entry 4883 (class 2606 OID 17112)
-- Name: users users_email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


--
-- TOC entry 4885 (class 2606 OID 16903)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4887 (class 2606 OID 16905)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4888 (class 1259 OID 17054)
-- Name: idx_medicine_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_medicine_name ON public.medicines USING btree (medicine_name);


--
-- TOC entry 4898 (class 1259 OID 17053)
-- Name: idx_sales_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sales_date ON public.sales USING btree (sale_date);


--
-- TOC entry 4893 (class 1259 OID 17055)
-- Name: idx_stock_branch; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_stock_branch ON public.stock USING btree (branch_id);


--
-- TOC entry 4950 (class 2620 OID 17032)
-- Name: sale_items trg_reduce_stock; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_reduce_stock AFTER INSERT ON public.sale_items FOR EACH ROW EXECUTE FUNCTION public.reduce_stock();


--
-- TOC entry 4942 (class 2606 OID 17083)
-- Name: ai_safety_logs ai_safety_logs_medicine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_safety_logs
    ADD CONSTRAINT ai_safety_logs_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id);


--
-- TOC entry 4943 (class 2606 OID 17238)
-- Name: stock_batches fk_batches_medicine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_batches
    ADD CONSTRAINT fk_batches_medicine FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id) ON DELETE CASCADE;


--
-- TOC entry 4946 (class 2606 OID 17243)
-- Name: message_logs fk_messages_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_logs
    ADD CONSTRAINT fk_messages_customer FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id) ON DELETE CASCADE;


--
-- TOC entry 4947 (class 2606 OID 17248)
-- Name: message_logs fk_messages_sale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_logs
    ADD CONSTRAINT fk_messages_sale FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id) ON DELETE CASCADE;


--
-- TOC entry 4940 (class 2606 OID 17233)
-- Name: payments fk_payments_sale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT fk_payments_sale FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id) ON DELETE CASCADE;


--
-- TOC entry 4935 (class 2606 OID 17026)
-- Name: prescriptions fk_prescription_sale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT fk_prescription_sale FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id) ON DELETE CASCADE;


--
-- TOC entry 4920 (class 2606 OID 16936)
-- Name: purchases fk_purchase_branch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT fk_purchase_branch FOREIGN KEY (branch_id) REFERENCES public.branches(branch_id);


--
-- TOC entry 4921 (class 2606 OID 16941)
-- Name: purchases fk_purchase_supplier; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT fk_purchase_supplier FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplier_id);


--
-- TOC entry 4922 (class 2606 OID 16946)
-- Name: purchases fk_purchase_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT fk_purchase_user FOREIGN KEY (recorded_by) REFERENCES public.users(user_id);


--
-- TOC entry 4936 (class 2606 OID 17228)
-- Name: purchase_items fk_purchaseitems_medicine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_items
    ADD CONSTRAINT fk_purchaseitems_medicine FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id) ON DELETE CASCADE;


--
-- TOC entry 4937 (class 2606 OID 17223)
-- Name: purchase_items fk_purchaseitems_purchase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_items
    ADD CONSTRAINT fk_purchaseitems_purchase FOREIGN KEY (purchase_id) REFERENCES public.purchases(purchase_id) ON DELETE CASCADE;


--
-- TOC entry 4925 (class 2606 OID 16985)
-- Name: sales fk_sale_branch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT fk_sale_branch FOREIGN KEY (branch_id) REFERENCES public.branches(branch_id);


--
-- TOC entry 4926 (class 2606 OID 16990)
-- Name: sales fk_sale_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT fk_sale_user FOREIGN KEY (performed_by) REFERENCES public.users(user_id);


--
-- TOC entry 4931 (class 2606 OID 17011)
-- Name: sale_items fk_saleitem_medicine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale_items
    ADD CONSTRAINT fk_saleitem_medicine FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id);


--
-- TOC entry 4932 (class 2606 OID 17006)
-- Name: sale_items fk_saleitem_sale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale_items
    ADD CONSTRAINT fk_saleitem_sale FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id) ON DELETE CASCADE;


--
-- TOC entry 4933 (class 2606 OID 17218)
-- Name: sale_items fk_saleitems_medicine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale_items
    ADD CONSTRAINT fk_saleitems_medicine FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id) ON DELETE CASCADE;


--
-- TOC entry 4934 (class 2606 OID 17213)
-- Name: sale_items fk_saleitems_sale; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sale_items
    ADD CONSTRAINT fk_saleitems_sale FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id) ON DELETE CASCADE;


--
-- TOC entry 4927 (class 2606 OID 17203)
-- Name: sales fk_sales_branch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT fk_sales_branch FOREIGN KEY (branch_id) REFERENCES public.branches(branch_id) ON DELETE CASCADE;


--
-- TOC entry 4928 (class 2606 OID 17198)
-- Name: sales fk_sales_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id) ON DELETE SET NULL;


--
-- TOC entry 4929 (class 2606 OID 17208)
-- Name: sales fk_sales_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT fk_sales_user FOREIGN KEY (performed_by) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 4923 (class 2606 OID 16965)
-- Name: stock fk_stock_branch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock
    ADD CONSTRAINT fk_stock_branch FOREIGN KEY (branch_id) REFERENCES public.branches(branch_id);


--
-- TOC entry 4924 (class 2606 OID 16970)
-- Name: stock fk_stock_medicine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock
    ADD CONSTRAINT fk_stock_medicine FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id);


--
-- TOC entry 4919 (class 2606 OID 16906)
-- Name: users fk_user_branch; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_user_branch FOREIGN KEY (branch_id) REFERENCES public.branches(branch_id);


--
-- TOC entry 4948 (class 2606 OID 17182)
-- Name: message_logs message_logs_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_logs
    ADD CONSTRAINT message_logs_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- TOC entry 4949 (class 2606 OID 17187)
-- Name: message_logs message_logs_sale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_logs
    ADD CONSTRAINT message_logs_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id);


--
-- TOC entry 4941 (class 2606 OID 17067)
-- Name: payments payments_sale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES public.sales(sale_id);


--
-- TOC entry 4938 (class 2606 OID 17048)
-- Name: purchase_items purchase_items_medicine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_items
    ADD CONSTRAINT purchase_items_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id);


--
-- TOC entry 4939 (class 2606 OID 17043)
-- Name: purchase_items purchase_items_purchase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.purchase_items
    ADD CONSTRAINT purchase_items_purchase_id_fkey FOREIGN KEY (purchase_id) REFERENCES public.purchases(purchase_id) ON DELETE CASCADE;


--
-- TOC entry 4930 (class 2606 OID 17193)
-- Name: sales sales_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- TOC entry 4944 (class 2606 OID 17099)
-- Name: stock_batches stock_batches_branch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_batches
    ADD CONSTRAINT stock_batches_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.branches(branch_id);


--
-- TOC entry 4945 (class 2606 OID 17104)
-- Name: stock_batches stock_batches_medicine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stock_batches
    ADD CONSTRAINT stock_batches_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES public.medicines(medicine_id);


-- Completed on 2026-03-03 11:21:19

--
-- PostgreSQL database dump complete
--

\unrestrict Y3c2L9sZQqb48V9MsfMrmDFhD9QGXnakNLUEywGUI6E69OixeBnTXxkyA4f9Afu

