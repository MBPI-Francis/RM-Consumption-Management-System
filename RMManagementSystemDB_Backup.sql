PGDMP      5    
            }            RMManagementSystemDB    16.2    16.4 �    Y           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            Z           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            [           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            \           1262    51262    RMManagementSystemDB    DATABASE     �   CREATE DATABASE "RMManagementSystemDB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
 &   DROP DATABASE "RMManagementSystemDB";
                postgres    false            �            1259    60187    tbl_computed_details    TABLE     }   CREATE TABLE public.tbl_computed_details (
    id uuid NOT NULL,
    date_computed date NOT NULL,
    computed_by_id uuid
);
 (   DROP TABLE public.tbl_computed_details;
       public         heap    postgres    false            �            1259    51308    tbl_departments    TABLE       CREATE TABLE public.tbl_departments (
    id uuid NOT NULL,
    name character varying(150) NOT NULL,
    description character varying(300) NOT NULL,
    is_deleted boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);
 #   DROP TABLE public.tbl_departments;
       public         heap    postgres    false            �            1259    51403    tbl_droplist    TABLE     k  CREATE TABLE public.tbl_droplist (
    id uuid NOT NULL,
    name character varying(150) NOT NULL,
    description character varying(300),
    is_deleted boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    deleted_at timestamp without time zone
);
     DROP TABLE public.tbl_droplist;
       public         heap    postgres    false            �            1259    68954    tbl_held_forms    TABLE     S  CREATE TABLE public.tbl_held_forms (
    id uuid NOT NULL,
    rm_code_id uuid NOT NULL,
    warehouse_id uuid NOT NULL,
    rm_soh_id uuid,
    current_status_id uuid,
    new_status_id uuid,
    change_status_date date NOT NULL,
    ref_number character varying(50) NOT NULL,
    qty_kg numeric(10,2) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    is_computed boolean DEFAULT false,
    date_computed date,
    is_cleared boolean
);
 "   DROP TABLE public.tbl_held_forms;
       public         heap    postgres    false            �            1259    69838 	   tbl_notes    TABLE     	  CREATE TABLE public.tbl_notes (
    id uuid NOT NULL,
    product_code character varying(80) NOT NULL,
    lot_number character varying(80) NOT NULL,
    product_kind_id character varying(10) NOT NULL,
    is_deleted boolean,
    stock_change_date date NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    is_computed boolean DEFAULT false,
    date_computed date,
    is_cleared boolean
);
    DROP TABLE public.tbl_notes;
       public         heap    postgres    false            �            1259    60413    tbl_outgoing_reports    TABLE        CREATE TABLE public.tbl_outgoing_reports (
    id uuid NOT NULL,
    rm_code_id uuid NOT NULL,
    warehouse_id uuid NOT NULL,
    rm_soh_id uuid,
    ref_number character varying(50) NOT NULL,
    outgoing_date date NOT NULL,
    qty_kg numeric(10,2) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    is_computed boolean DEFAULT false,
    date_computed date,
    is_cleared boolean
);
 (   DROP TABLE public.tbl_outgoing_reports;
       public         heap    postgres    false            �            1259    60596    tbl_preparation_forms    TABLE     _  CREATE TABLE public.tbl_preparation_forms (
    id uuid NOT NULL,
    rm_code_id uuid NOT NULL,
    warehouse_id uuid NOT NULL,
    rm_soh_id uuid,
    ref_number character varying(50) NOT NULL,
    preparation_date date NOT NULL,
    qty_prepared numeric(10,2) NOT NULL,
    qty_return numeric(10,2) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    is_computed boolean DEFAULT false,
    date_computed date,
    is_cleared boolean DEFAULT false
);
 )   DROP TABLE public.tbl_preparation_forms;
       public         heap    postgres    false            �            1259    51565    tbl_product_kind    TABLE     b  CREATE TABLE public.tbl_product_kind (
    id character varying(10) NOT NULL,
    name character varying(80) NOT NULL,
    description character varying(300),
    is_deleted boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid
);
 $   DROP TABLE public.tbl_product_kind;
       public         heap    postgres    false            �            1259    51378    tbl_raw_materials    TABLE     j  CREATE TABLE public.tbl_raw_materials (
    id uuid NOT NULL,
    rm_code character varying(50) NOT NULL,
    rm_name character varying(150),
    description character varying(300),
    is_deleted boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid
);
 %   DROP TABLE public.tbl_raw_materials;
       public         heap    postgres    false            �            1259    60256    tbl_receiving_reports    TABLE     0  CREATE TABLE public.tbl_receiving_reports (
    id uuid NOT NULL,
    rm_code_id uuid NOT NULL,
    warehouse_id uuid NOT NULL,
    rm_soh_id uuid,
    ref_number character varying(50) NOT NULL,
    receiving_date date NOT NULL,
    qty_kg numeric(10,2) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    is_computed boolean DEFAULT false,
    date_computed date,
    is_cleared boolean DEFAULT false
);
 )   DROP TABLE public.tbl_receiving_reports;
       public         heap    postgres    false            �            1259    59852    tbl_stock_on_hand    TABLE     �  CREATE TABLE public.tbl_stock_on_hand (
    id uuid NOT NULL,
    rm_code_id uuid NOT NULL,
    warehouse_id uuid NOT NULL,
    rm_soh numeric(10,2) NOT NULL,
    description character varying(300),
    is_deleted boolean,
    stock_change_date timestamp without time zone NOT NULL,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    status_id uuid,
    date_computed date
);
 %   DROP TABLE public.tbl_stock_on_hand;
       public         heap    postgres    false            �            1259    69053    tbl_transfer_forms    TABLE     �  CREATE TABLE public.tbl_transfer_forms (
    id uuid NOT NULL,
    rm_code_id uuid NOT NULL,
    from_warehouse_id uuid NOT NULL,
    to_warehouse_id uuid NOT NULL,
    from_rm_soh_id uuid,
    to_rm_soh_id uuid,
    status_id uuid,
    ref_number character varying(50) NOT NULL,
    transfer_date date NOT NULL,
    qty_kg numeric(10,2) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid,
    is_computed boolean DEFAULT false,
    date_computed date,
    is_cleared boolean DEFAULT false
);
 &   DROP TABLE public.tbl_transfer_forms;
       public         heap    postgres    false            �            1259    51326 	   tbl_users    TABLE     �  CREATE TABLE public.tbl_users (
    id uuid NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    user_name character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deavtivated_by_id uuid,
    department_id uuid
);
    DROP TABLE public.tbl_users;
       public         heap    postgres    false            �            1259    51353    tbl_warehouses    TABLE     e  CREATE TABLE public.tbl_warehouses (
    id uuid NOT NULL,
    wh_number smallint NOT NULL,
    wh_name character varying(150) NOT NULL,
    description character varying(300),
    is_deleted boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    created_by_id uuid,
    updated_by_id uuid,
    deleted_by_id uuid
);
 "   DROP TABLE public.tbl_warehouses;
       public         heap    postgres    false            �            1259    71141    view_beginning_soh    VIEW     �  CREATE VIEW public.view_beginning_soh AS
 WITH rankedrecords AS (
         SELECT soh.warehouse_id AS warehouseid,
            wh.wh_name AS warehousename,
            wh.wh_number AS warehousenumber,
            soh.rm_code_id AS rawmaterialid,
            rm.rm_code AS rmcode,
            soh.rm_soh AS beginningbalance,
            soh.stock_change_date AS stockchangedate,
            COALESCE(status.name, ''::character varying) AS statusname,
            soh.status_id AS statusid,
            row_number() OVER (PARTITION BY soh.warehouse_id, soh.rm_code_id, soh.status_id ORDER BY soh.stock_change_date DESC) AS row_num
           FROM (((public.tbl_stock_on_hand soh
             JOIN public.tbl_raw_materials rm ON ((soh.rm_code_id = rm.id)))
             JOIN public.tbl_warehouses wh ON ((soh.warehouse_id = wh.id)))
             LEFT JOIN public.tbl_droplist status ON ((soh.status_id = status.id)))
        )
 SELECT warehouseid,
    warehousename,
    warehousenumber,
    rawmaterialid,
    rmcode,
    beginningbalance,
    statusname,
    statusid,
    stockchangedate
   FROM rankedrecords
  WHERE (row_num = 1)
  ORDER BY rmcode, stockchangedate DESC;
 %   DROP VIEW public.view_beginning_soh;
       public          postgres    false    217    219    218    218    221    221    221    217    221    221    219    217            �            1259    71147    view_ending_stocks_balance    VIEW     ?  CREATE VIEW public.view_ending_stocks_balance AS
 WITH initialbalance AS (
         WITH rankedrecords AS (
                 SELECT soh.warehouse_id AS warehouseid,
                    wh.wh_name AS warehousename,
                    wh.wh_number AS warehousenumber,
                    soh.rm_code_id AS rawmaterialid,
                    rm.rm_code AS rmcode,
                    soh.rm_soh AS beginningbalance,
                    soh.stock_change_date AS stockchangedate,
                    status.name AS statusname,
                    soh.status_id AS statusid,
                    row_number() OVER (PARTITION BY soh.warehouse_id, soh.rm_code_id, soh.status_id ORDER BY soh.stock_change_date DESC) AS row_num
                   FROM (((public.tbl_stock_on_hand soh
                     JOIN public.tbl_raw_materials rm ON ((soh.rm_code_id = rm.id)))
                     JOIN public.tbl_warehouses wh ON ((soh.warehouse_id = wh.id)))
                     LEFT JOIN public.tbl_droplist status ON ((soh.status_id = status.id)))
                )
         SELECT rankedrecords.warehouseid,
            rankedrecords.warehousename,
            rankedrecords.warehousenumber,
            rankedrecords.rawmaterialid,
            rankedrecords.rmcode,
            rankedrecords.beginningbalance,
            rankedrecords.stockchangedate,
            rankedrecords.statusname,
            rankedrecords.statusid
           FROM rankedrecords
          WHERE (rankedrecords.row_num = 1)
        ), ogr_adjustments AS (
         SELECT ogr.warehouse_id AS warehouseid,
            ogr.rm_code_id AS rawmaterialid,
            sum(ogr.qty_kg) AS total_ogr_quantity,
            ogr.date_computed AS datecomputed
           FROM (public.tbl_outgoing_reports ogr
             JOIN public.tbl_warehouses wh ON ((ogr.warehouse_id = wh.id)))
          WHERE (((ogr.is_cleared IS NULL) OR (ogr.is_cleared = false)) AND ((ogr.is_deleted IS NULL) OR (ogr.is_deleted = false)) AND (ogr.date_computed IS NULL))
          GROUP BY ogr.warehouse_id, ogr.rm_code_id, ogr.date_computed
        ), pf_adjustments AS (
         SELECT pf.warehouse_id AS warehouseid,
            pf.rm_code_id AS rawmaterialid,
            sum(pf.qty_prepared) AS total_prepared,
            sum(pf.qty_return) AS total_returned,
            pf.date_computed AS datecomputed
           FROM (public.tbl_preparation_forms pf
             JOIN public.tbl_warehouses wh ON ((pf.warehouse_id = wh.id)))
          WHERE (((pf.is_cleared IS NULL) OR (pf.is_cleared = false)) AND ((pf.is_deleted IS NULL) OR (pf.is_deleted = false)) AND (pf.date_computed IS NULL))
          GROUP BY pf.warehouse_id, pf.rm_code_id, pf.date_computed
        ), transferred_from AS (
         SELECT tf.from_warehouse_id AS warehouseid,
            tf.rm_code_id AS rawmaterialid,
            (- sum(tf.qty_kg)) AS transferred_from_qty,
            tf.date_computed AS datecomputed,
            status.id AS statusid,
            status.name AS statusname
           FROM ((public.tbl_transfer_forms tf
             JOIN public.tbl_warehouses wh_from ON ((tf.from_warehouse_id = wh_from.id)))
             LEFT JOIN public.tbl_droplist status ON ((tf.status_id = status.id)))
          WHERE (((tf.is_cleared IS NULL) OR (tf.is_cleared = false)) AND ((tf.is_deleted IS NULL) OR (tf.is_deleted = false)) AND (tf.date_computed IS NULL))
          GROUP BY tf.from_warehouse_id, tf.rm_code_id, tf.date_computed, status.id, status.name
        ), transferred_to AS (
         SELECT tf.to_warehouse_id AS warehouseid,
            tf.rm_code_id AS rawmaterialid,
            sum(tf.qty_kg) AS transferred_to_qty,
            tf.date_computed AS datecomputed,
            status.id AS statusid,
            status.name AS statusname
           FROM ((public.tbl_transfer_forms tf
             JOIN public.tbl_warehouses wh_to ON ((tf.to_warehouse_id = wh_to.id)))
             LEFT JOIN public.tbl_droplist status ON ((tf.status_id = status.id)))
          WHERE (((tf.is_cleared IS NULL) OR (tf.is_cleared = false)) AND ((tf.is_deleted IS NULL) OR (tf.is_deleted = false)) AND (tf.date_computed IS NULL))
          GROUP BY tf.to_warehouse_id, tf.rm_code_id, tf.date_computed, status.id, status.name
        ), rr_adjustments AS (
         SELECT rr.warehouse_id AS warehouseid,
            rr.rm_code_id AS rawmaterialid,
            sum(rr.qty_kg) AS total_received,
            rr.date_computed AS datecomputed
           FROM (public.tbl_receiving_reports rr
             JOIN public.tbl_warehouses wh ON ((rr.warehouse_id = wh.id)))
          WHERE (((rr.is_cleared IS NULL) OR (rr.is_cleared = false)) AND ((rr.is_deleted IS NULL) OR (rr.is_deleted = false)) AND (rr.date_computed IS NULL))
          GROUP BY rr.warehouse_id, rr.rm_code_id, rr.date_computed
        ), status_adjustments_eval AS (
         SELECT hf.warehouse_id AS warehouseid,
            hf.rm_code_id AS rawmaterialid,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'held : contaminated'::text) THEN hf.qty_kg
                    WHEN ((new_status.name)::text ~~ 'held : reject'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_held,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'good%'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_released,
            hf.date_computed AS datecomputed
           FROM (((public.tbl_held_forms hf
             JOIN public.tbl_warehouses wh ON ((hf.warehouse_id = wh.id)))
             JOIN public.tbl_droplist current_status ON ((hf.current_status_id = current_status.id)))
             JOIN public.tbl_droplist new_status ON ((hf.new_status_id = new_status.id)))
          WHERE (((hf.is_cleared IS NULL) OR (hf.is_cleared = false)) AND ((hf.is_deleted IS NULL) OR (hf.is_deleted = false)) AND (hf.date_computed IS NULL) AND (((new_status.name)::text = 'held : under evaluation'::text) OR ((current_status.name)::text = 'held : under evaluation'::text)))
          GROUP BY hf.warehouse_id, hf.rm_code_id, hf.date_computed
        ), status_adjustments_conta AS (
         SELECT hf.warehouse_id AS warehouseid,
            hf.rm_code_id AS rawmaterialid,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'held : under evaluation'::text) THEN hf.qty_kg
                    WHEN ((new_status.name)::text ~~ 'held : reject'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_held,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'good%'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_released,
            hf.date_computed AS datecomputed
           FROM (((public.tbl_held_forms hf
             JOIN public.tbl_warehouses wh ON ((hf.warehouse_id = wh.id)))
             JOIN public.tbl_droplist current_status ON ((hf.current_status_id = current_status.id)))
             JOIN public.tbl_droplist new_status ON ((hf.new_status_id = new_status.id)))
          WHERE (((hf.is_cleared IS NULL) OR (hf.is_cleared = false)) AND ((hf.is_deleted IS NULL) OR (hf.is_deleted = false)) AND (hf.date_computed IS NULL) AND (((new_status.name)::text = 'held : contaminated'::text) OR ((current_status.name)::text = 'held : contaminated'::text)))
          GROUP BY hf.warehouse_id, hf.rm_code_id, hf.date_computed
        ), status_adjustments_rejec AS (
         SELECT hf.warehouse_id AS warehouseid,
            hf.rm_code_id AS rawmaterialid,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'held : under evaluation'::text) THEN hf.qty_kg
                    WHEN ((new_status.name)::text ~~ 'held : contaminated'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_held,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'good%'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_released,
            hf.date_computed AS datecomputed
           FROM (((public.tbl_held_forms hf
             JOIN public.tbl_warehouses wh ON ((hf.warehouse_id = wh.id)))
             JOIN public.tbl_droplist current_status ON ((hf.current_status_id = current_status.id)))
             JOIN public.tbl_droplist new_status ON ((hf.new_status_id = new_status.id)))
          WHERE (((hf.is_cleared IS NULL) OR (hf.is_cleared = false)) AND ((hf.is_deleted IS NULL) OR (hf.is_deleted = false)) AND (hf.date_computed IS NULL) AND (((new_status.name)::text = 'held : reject'::text) OR ((current_status.name)::text = 'held : reject'::text)))
          GROUP BY hf.warehouse_id, hf.rm_code_id, hf.date_computed
        ), status_adjustments_good AS (
         SELECT hf.warehouse_id AS warehouseid,
            hf.rm_code_id AS rawmaterialid,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'held%'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_held,
            sum(
                CASE
                    WHEN ((new_status.name)::text ~~ 'good%'::text) THEN hf.qty_kg
                    ELSE (0)::numeric
                END) AS total_released,
            hf.date_computed AS datecomputed
           FROM (((public.tbl_held_forms hf
             JOIN public.tbl_warehouses wh ON ((hf.warehouse_id = wh.id)))
             JOIN public.tbl_droplist current_status ON ((hf.current_status_id = current_status.id)))
             JOIN public.tbl_droplist new_status ON ((hf.new_status_id = new_status.id)))
          WHERE (((hf.is_cleared IS NULL) OR (hf.is_cleared = false)) AND ((hf.is_deleted IS NULL) OR (hf.is_deleted = false)) AND (hf.date_computed IS NULL) AND (((new_status.name)::text = 'good'::text) OR ((current_status.name)::text = 'good'::text)))
          GROUP BY hf.warehouse_id, hf.rm_code_id, hf.date_computed
        ), held_status_details AS (
         SELECT hf.rm_code_id AS rawmaterialid,
            wh.wh_name AS warehousename,
            wh.id AS warehouseid,
            wh.wh_number AS warehousenumber,
            rm.rm_code AS rmcode,
            sum(hf.qty_kg) AS heldquantity,
            new_status.name AS status,
            hf.date_computed,
            hf.new_status_id AS statusid
           FROM (((public.tbl_held_forms hf
             JOIN public.tbl_raw_materials rm ON ((hf.rm_code_id = rm.id)))
             JOIN public.tbl_warehouses wh ON ((hf.warehouse_id = wh.id)))
             JOIN public.tbl_droplist new_status ON ((hf.new_status_id = new_status.id)))
          WHERE (((new_status.name)::text ~~ 'held%'::text) AND ((hf.is_cleared IS NULL) OR (hf.is_cleared = false)) AND ((hf.is_deleted IS NULL) OR (hf.is_deleted = false)) AND (hf.date_computed IS NULL))
          GROUP BY hf.rm_code_id, wh.wh_name, wh.wh_number, rm.rm_code, new_status.name, hf.date_computed, wh.id, hf.new_status_id
        ), computed_statement AS (
         SELECT ib.rawmaterialid,
            ib.rmcode,
            ib.warehouseid,
            ib.warehousename,
            ib.warehousenumber,
            ((ib.beginningbalance + COALESCE(rr.total_received, (0)::numeric)) +
                CASE
                    WHEN ((ib.statusname)::text = 'held : reject'::text) THEN ((((- COALESCE(rej.total_held, (0)::numeric)) - COALESCE(rej.total_released, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tf.statusname)::text = 'held : reject'::text) THEN tf.transferred_from_qty
                        ELSE NULL::numeric
                    END, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tt.statusname)::text = 'held : reject'::text) THEN tt.transferred_to_qty
                        ELSE NULL::numeric
                    END, (0)::numeric))
                    WHEN ((ib.statusname)::text = 'held : under evaluation'::text) THEN ((((- COALESCE(eval.total_held, (0)::numeric)) - COALESCE(eval.total_released, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tf.statusname)::text = 'held : under evaluation'::text) THEN tf.transferred_from_qty
                        ELSE NULL::numeric
                    END, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tt.statusname)::text = 'held : under evaluation'::text) THEN tt.transferred_to_qty
                        ELSE NULL::numeric
                    END, (0)::numeric))
                    WHEN ((ib.statusname)::text = 'held : contaminated'::text) THEN ((((- COALESCE(cs.total_held, (0)::numeric)) - COALESCE(cs.total_released, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tf.statusname)::text = 'held : contaminated'::text) THEN tf.transferred_from_qty
                        ELSE NULL::numeric
                    END, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tt.statusname)::text = 'held : contaminated'::text) THEN tt.transferred_to_qty
                        ELSE NULL::numeric
                    END, (0)::numeric))
                    WHEN ((ib.statusname)::text = 'good'::text) THEN (((((((- COALESCE(good.total_held, (0)::numeric)) - COALESCE(ogr.total_ogr_quantity, (0)::numeric)) + COALESCE(good.total_released, (0)::numeric)) + COALESCE(pf.total_returned, (0)::numeric)) - COALESCE(pf.total_prepared, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tf.statusname)::text = 'good'::text) THEN tf.transferred_from_qty
                        ELSE NULL::numeric
                    END, (0)::numeric)) + COALESCE(
                    CASE
                        WHEN ((tt.statusname)::text = 'good'::text) THEN tt.transferred_to_qty
                        ELSE NULL::numeric
                    END, (0)::numeric))
                    ELSE NULL::numeric
                END) AS new_beginning_balance,
            COALESCE(ib.statusname, ''::character varying) AS status,
            ib.statusid
           FROM (((((((((initialbalance ib
             LEFT JOIN ogr_adjustments ogr ON (((ib.warehouseid = ogr.warehouseid) AND (ib.rawmaterialid = ogr.rawmaterialid))))
             LEFT JOIN pf_adjustments pf ON (((ib.warehouseid = pf.warehouseid) AND (ib.rawmaterialid = pf.rawmaterialid))))
             LEFT JOIN transferred_from tf ON (((ib.warehouseid = tf.warehouseid) AND (ib.rawmaterialid = tf.rawmaterialid) AND (ib.statusid = tf.statusid))))
             LEFT JOIN transferred_to tt ON (((ib.warehouseid = tt.warehouseid) AND (ib.rawmaterialid = tt.rawmaterialid) AND (ib.statusid = tt.statusid))))
             LEFT JOIN rr_adjustments rr ON (((ib.warehouseid = rr.warehouseid) AND (ib.rawmaterialid = rr.rawmaterialid))))
             LEFT JOIN status_adjustments_conta cs ON (((ib.warehouseid = cs.warehouseid) AND (ib.rawmaterialid = cs.rawmaterialid))))
             LEFT JOIN status_adjustments_eval eval ON (((ib.warehouseid = eval.warehouseid) AND (eval.rawmaterialid = cs.rawmaterialid))))
             LEFT JOIN status_adjustments_rejec rej ON (((ib.warehouseid = rej.warehouseid) AND (ib.rawmaterialid = rej.rawmaterialid))))
             LEFT JOIN status_adjustments_good good ON (((ib.warehouseid = good.warehouseid) AND (ib.rawmaterialid = good.rawmaterialid))))
        UNION ALL
         SELECT hs.rawmaterialid,
            hs.rmcode,
            hs.warehouseid,
            hs.warehousename,
            hs.warehousenumber,
            hs.heldquantity AS new_beginning_balance,
            hs.status,
            hs.statusid
           FROM held_status_details hs
  ORDER BY 2, 4, 5, 7 NULLS FIRST
        )
 SELECT rawmaterialid,
    rmcode,
    warehouseid,
    warehousename,
    warehousenumber,
    sum(new_beginning_balance) AS new_beginning_balance,
    COALESCE(status, ''::character varying) AS status,
    statusid
   FROM computed_statement
  GROUP BY rawmaterialid, rmcode, warehouseid, warehousename, warehousenumber, status, statusid
  ORDER BY rmcode;
 -   DROP VIEW public.view_ending_stocks_balance;
       public          postgres    false    223    223    223    223    223    223    221    221    221    221    221    219    219    218    218    217    217    217    227    227    227    227    227    227    227    227    226    226    226    226    226    226    226    226    225    225    225    225    225    225    225    224    224    224    224    224    224            �            1259    70903    view_latest_soh_v1    VIEW     L  CREATE VIEW public.view_latest_soh_v1 AS
 WITH rankedrecords AS (
         SELECT soh.warehouse_id AS warehouseid,
            wh.wh_name AS warehousename,
            wh.wh_number AS warehousenumber,
            soh.rm_code_id AS rawmaterialid,
            rm.rm_code AS rmcode,
            soh.rm_soh AS beginningbalance,
            soh.stock_change_date AS stockchangedate,
            status.name AS statusname,
            soh.status_id AS statusid,
            row_number() OVER (PARTITION BY soh.warehouse_id, soh.rm_code_id, soh.status_id ORDER BY soh.stock_change_date DESC) AS row_num
           FROM (((public.tbl_stock_on_hand soh
             JOIN public.tbl_raw_materials rm ON ((soh.rm_code_id = rm.id)))
             JOIN public.tbl_warehouses wh ON ((soh.warehouse_id = wh.id)))
             LEFT JOIN public.tbl_droplist status ON ((soh.status_id = status.id)))
        )
 SELECT warehouseid,
    warehousename,
    warehousenumber,
    rawmaterialid,
    rmcode,
    beginningbalance,
    statusname,
    statusid,
    stockchangedate
   FROM rankedrecords
  WHERE (row_num = 1);
 %   DROP VIEW public.view_latest_soh_v1;
       public          postgres    false    217    217    217    218    218    219    219    221    221    221    221    221            P          0    60187    tbl_computed_details 
   TABLE DATA           Q   COPY public.tbl_computed_details (id, date_computed, computed_by_id) FROM stdin;
    public          postgres    false    222   �       I          0    51308    tbl_departments 
   TABLE DATA           d   COPY public.tbl_departments (id, name, description, is_deleted, created_at, updated_at) FROM stdin;
    public          postgres    false    215   !      M          0    51403    tbl_droplist 
   TABLE DATA           �   COPY public.tbl_droplist (id, name, description, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, deleted_at) FROM stdin;
    public          postgres    false    219   S"      T          0    68954    tbl_held_forms 
   TABLE DATA             COPY public.tbl_held_forms (id, rm_code_id, warehouse_id, rm_soh_id, current_status_id, new_status_id, change_status_date, ref_number, qty_kg, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, is_computed, date_computed, is_cleared) FROM stdin;
    public          postgres    false    226   #      V          0    69838 	   tbl_notes 
   TABLE DATA           �   COPY public.tbl_notes (id, product_code, lot_number, product_kind_id, is_deleted, stock_change_date, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, is_computed, date_computed, is_cleared) FROM stdin;
    public          postgres    false    228   :#      R          0    60413    tbl_outgoing_reports 
   TABLE DATA           �   COPY public.tbl_outgoing_reports (id, rm_code_id, warehouse_id, rm_soh_id, ref_number, outgoing_date, qty_kg, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, is_computed, date_computed, is_cleared) FROM stdin;
    public          postgres    false    224   W#      S          0    60596    tbl_preparation_forms 
   TABLE DATA           	  COPY public.tbl_preparation_forms (id, rm_code_id, warehouse_id, rm_soh_id, ref_number, preparation_date, qty_prepared, qty_return, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, is_computed, date_computed, is_cleared) FROM stdin;
    public          postgres    false    225   t#      N          0    51565    tbl_product_kind 
   TABLE DATA           �   COPY public.tbl_product_kind (id, name, description, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id) FROM stdin;
    public          postgres    false    220   �#      L          0    51378    tbl_raw_materials 
   TABLE DATA           �   COPY public.tbl_raw_materials (id, rm_code, rm_name, description, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id) FROM stdin;
    public          postgres    false    218   $      Q          0    60256    tbl_receiving_reports 
   TABLE DATA           �   COPY public.tbl_receiving_reports (id, rm_code_id, warehouse_id, rm_soh_id, ref_number, receiving_date, qty_kg, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, is_computed, date_computed, is_cleared) FROM stdin;
    public          postgres    false    223   D      O          0    59852    tbl_stock_on_hand 
   TABLE DATA           �   COPY public.tbl_stock_on_hand (id, rm_code_id, warehouse_id, rm_soh, description, is_deleted, stock_change_date, created_by_id, updated_by_id, deleted_by_id, status_id, date_computed) FROM stdin;
    public          postgres    false    221   .D      U          0    69053    tbl_transfer_forms 
   TABLE DATA           %  COPY public.tbl_transfer_forms (id, rm_code_id, from_warehouse_id, to_warehouse_id, from_rm_soh_id, to_rm_soh_id, status_id, ref_number, transfer_date, qty_kg, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id, is_computed, date_computed, is_cleared) FROM stdin;
    public          postgres    false    227   KD      J          0    51326 	   tbl_users 
   TABLE DATA           �   COPY public.tbl_users (id, first_name, last_name, user_name, password, is_active, created_at, updated_at, created_by_id, updated_by_id, deavtivated_by_id, department_id) FROM stdin;
    public          postgres    false    216   hD      K          0    51353    tbl_warehouses 
   TABLE DATA           �   COPY public.tbl_warehouses (id, wh_number, wh_name, description, is_deleted, created_at, updated_at, created_by_id, updated_by_id, deleted_by_id) FROM stdin;
    public          postgres    false    217   E      f           2606    60191 .   tbl_computed_details tbl_computed_details_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.tbl_computed_details
    ADD CONSTRAINT tbl_computed_details_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.tbl_computed_details DROP CONSTRAINT tbl_computed_details_pkey;
       public            postgres    false    222            F           2606    51314 (   tbl_departments tbl_departments_name_key 
   CONSTRAINT     c   ALTER TABLE ONLY public.tbl_departments
    ADD CONSTRAINT tbl_departments_name_key UNIQUE (name);
 R   ALTER TABLE ONLY public.tbl_departments DROP CONSTRAINT tbl_departments_name_key;
       public            postgres    false    215            H           2606    51312 $   tbl_departments tbl_departments_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.tbl_departments
    ADD CONSTRAINT tbl_departments_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.tbl_departments DROP CONSTRAINT tbl_departments_pkey;
       public            postgres    false    215            [           2606    51409 "   tbl_droplist tbl_droplist_name_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.tbl_droplist
    ADD CONSTRAINT tbl_droplist_name_key UNIQUE (name);
 L   ALTER TABLE ONLY public.tbl_droplist DROP CONSTRAINT tbl_droplist_name_key;
       public            postgres    false    219            ]           2606    51407    tbl_droplist tbl_droplist_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.tbl_droplist
    ADD CONSTRAINT tbl_droplist_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.tbl_droplist DROP CONSTRAINT tbl_droplist_pkey;
       public            postgres    false    219            r           2606    68958 '   tbl_held_forms tbl_held_forms_temp_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_pkey PRIMARY KEY (id);
 Q   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_pkey;
       public            postgres    false    226            x           2606    69842    tbl_notes tbl_notes_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.tbl_notes
    ADD CONSTRAINT tbl_notes_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.tbl_notes DROP CONSTRAINT tbl_notes_pkey;
       public            postgres    false    228            l           2606    60417 3   tbl_outgoing_reports tbl_outgoing_reports_temp_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_pkey PRIMARY KEY (id);
 ]   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_pkey;
       public            postgres    false    224            o           2606    60600 5   tbl_preparation_forms tbl_preparation_forms_temp_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_pkey PRIMARY KEY (id);
 _   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_pkey;
       public            postgres    false    225            `           2606    51569 &   tbl_product_kind tbl_product_kind_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.tbl_product_kind
    ADD CONSTRAINT tbl_product_kind_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.tbl_product_kind DROP CONSTRAINT tbl_product_kind_pkey;
       public            postgres    false    220            V           2606    51384 (   tbl_raw_materials tbl_raw_materials_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.tbl_raw_materials
    ADD CONSTRAINT tbl_raw_materials_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.tbl_raw_materials DROP CONSTRAINT tbl_raw_materials_pkey;
       public            postgres    false    218            X           2606    51386 /   tbl_raw_materials tbl_raw_materials_rm_code_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.tbl_raw_materials
    ADD CONSTRAINT tbl_raw_materials_rm_code_key UNIQUE (rm_code);
 Y   ALTER TABLE ONLY public.tbl_raw_materials DROP CONSTRAINT tbl_raw_materials_rm_code_key;
       public            postgres    false    218            i           2606    60260 5   tbl_receiving_reports tbl_receiving_reports_temp_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_pkey PRIMARY KEY (id);
 _   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_pkey;
       public            postgres    false    223            c           2606    59856 (   tbl_stock_on_hand tbl_stock_on_hand_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_stock_on_hand_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_stock_on_hand_pkey;
       public            postgres    false    221            u           2606    69057 /   tbl_transfer_forms tbl_transfer_forms_temp_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_pkey PRIMARY KEY (id);
 Y   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_pkey;
       public            postgres    false    227            L           2606    51330    tbl_users tbl_users_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_users_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.tbl_users DROP CONSTRAINT tbl_users_pkey;
       public            postgres    false    216            O           2606    51357 "   tbl_warehouses tbl_warehouses_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.tbl_warehouses
    ADD CONSTRAINT tbl_warehouses_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.tbl_warehouses DROP CONSTRAINT tbl_warehouses_pkey;
       public            postgres    false    217            Q           2606    51361 )   tbl_warehouses tbl_warehouses_wh_name_key 
   CONSTRAINT     g   ALTER TABLE ONLY public.tbl_warehouses
    ADD CONSTRAINT tbl_warehouses_wh_name_key UNIQUE (wh_name);
 S   ALTER TABLE ONLY public.tbl_warehouses DROP CONSTRAINT tbl_warehouses_wh_name_key;
       public            postgres    false    217            S           2606    51359 +   tbl_warehouses tbl_warehouses_wh_number_key 
   CONSTRAINT     k   ALTER TABLE ONLY public.tbl_warehouses
    ADD CONSTRAINT tbl_warehouses_wh_number_key UNIQUE (wh_number);
 U   ALTER TABLE ONLY public.tbl_warehouses DROP CONSTRAINT tbl_warehouses_wh_number_key;
       public            postgres    false    217            d           1259    60197    ix_tbl_computed_details_id    INDEX     `   CREATE UNIQUE INDEX ix_tbl_computed_details_id ON public.tbl_computed_details USING btree (id);
 .   DROP INDEX public.ix_tbl_computed_details_id;
       public            postgres    false    222            D           1259    51315    ix_tbl_departments_id    INDEX     V   CREATE UNIQUE INDEX ix_tbl_departments_id ON public.tbl_departments USING btree (id);
 )   DROP INDEX public.ix_tbl_departments_id;
       public            postgres    false    215            Y           1259    51425    ix_tbl_droplist_id    INDEX     P   CREATE UNIQUE INDEX ix_tbl_droplist_id ON public.tbl_droplist USING btree (id);
 &   DROP INDEX public.ix_tbl_droplist_id;
       public            postgres    false    219            p           1259    68999    ix_tbl_held_forms_temp_id    INDEX     Y   CREATE UNIQUE INDEX ix_tbl_held_forms_temp_id ON public.tbl_held_forms USING btree (id);
 -   DROP INDEX public.ix_tbl_held_forms_temp_id;
       public            postgres    false    226            v           1259    69863    ix_tbl_notes_id    INDEX     J   CREATE UNIQUE INDEX ix_tbl_notes_id ON public.tbl_notes USING btree (id);
 #   DROP INDEX public.ix_tbl_notes_id;
       public            postgres    false    228            j           1259    60450    ix_tbl_outgoing_reports_temp_id    INDEX     e   CREATE UNIQUE INDEX ix_tbl_outgoing_reports_temp_id ON public.tbl_outgoing_reports USING btree (id);
 3   DROP INDEX public.ix_tbl_outgoing_reports_temp_id;
       public            postgres    false    224            m           1259    60631     ix_tbl_preparation_forms_temp_id    INDEX     g   CREATE UNIQUE INDEX ix_tbl_preparation_forms_temp_id ON public.tbl_preparation_forms USING btree (id);
 4   DROP INDEX public.ix_tbl_preparation_forms_temp_id;
       public            postgres    false    225            ^           1259    51585    ix_tbl_product_kind_id    INDEX     X   CREATE UNIQUE INDEX ix_tbl_product_kind_id ON public.tbl_product_kind USING btree (id);
 *   DROP INDEX public.ix_tbl_product_kind_id;
       public            postgres    false    220            T           1259    51402    ix_tbl_raw_materials_id    INDEX     Z   CREATE UNIQUE INDEX ix_tbl_raw_materials_id ON public.tbl_raw_materials USING btree (id);
 +   DROP INDEX public.ix_tbl_raw_materials_id;
       public            postgres    false    218            g           1259    60293     ix_tbl_receiving_reports_temp_id    INDEX     g   CREATE UNIQUE INDEX ix_tbl_receiving_reports_temp_id ON public.tbl_receiving_reports USING btree (id);
 4   DROP INDEX public.ix_tbl_receiving_reports_temp_id;
       public            postgres    false    223            a           1259    59882    ix_tbl_stock_on_hand_id    INDEX     Z   CREATE UNIQUE INDEX ix_tbl_stock_on_hand_id ON public.tbl_stock_on_hand USING btree (id);
 +   DROP INDEX public.ix_tbl_stock_on_hand_id;
       public            postgres    false    221            s           1259    69103    ix_tbl_transfer_forms_temp_id    INDEX     a   CREATE UNIQUE INDEX ix_tbl_transfer_forms_temp_id ON public.tbl_transfer_forms USING btree (id);
 1   DROP INDEX public.ix_tbl_transfer_forms_temp_id;
       public            postgres    false    227            I           1259    51351    ix_tbl_users_id    INDEX     J   CREATE UNIQUE INDEX ix_tbl_users_id ON public.tbl_users USING btree (id);
 #   DROP INDEX public.ix_tbl_users_id;
       public            postgres    false    216            J           1259    51352    ix_tbl_users_user_name    INDEX     X   CREATE UNIQUE INDEX ix_tbl_users_user_name ON public.tbl_users USING btree (user_name);
 *   DROP INDEX public.ix_tbl_users_user_name;
       public            postgres    false    216            M           1259    51377    ix_tbl_warehouses_id    INDEX     T   CREATE UNIQUE INDEX ix_tbl_warehouses_id ON public.tbl_warehouses USING btree (id);
 (   DROP INDEX public.ix_tbl_warehouses_id;
       public            postgres    false    217            �           2606    70173 "   tbl_raw_materials fk_created_by_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_raw_materials
    ADD CONSTRAINT fk_created_by_id FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id) NOT VALID;
 L   ALTER TABLE ONLY public.tbl_raw_materials DROP CONSTRAINT fk_created_by_id;
       public          postgres    false    4684    216    218            �           2606    70183 "   tbl_raw_materials fk_deleted_by_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_raw_materials
    ADD CONSTRAINT fk_deleted_by_id FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id) NOT VALID;
 L   ALTER TABLE ONLY public.tbl_raw_materials DROP CONSTRAINT fk_deleted_by_id;
       public          postgres    false    218    216    4684            �           2606    70178 "   tbl_raw_materials fk_updated_by_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_raw_materials
    ADD CONSTRAINT fk_updated_by_id FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id) NOT VALID;
 L   ALTER TABLE ONLY public.tbl_raw_materials DROP CONSTRAINT fk_updated_by_id;
       public          postgres    false    216    218    4684            �           2606    60192 =   tbl_computed_details tbl_computed_details_computed_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_computed_details
    ADD CONSTRAINT tbl_computed_details_computed_by_id_fkey FOREIGN KEY (computed_by_id) REFERENCES public.tbl_users(id);
 g   ALTER TABLE ONLY public.tbl_computed_details DROP CONSTRAINT tbl_computed_details_computed_by_id_fkey;
       public          postgres    false    222    216    4684            �           2606    51410 ,   tbl_droplist tbl_droplist_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_droplist
    ADD CONSTRAINT tbl_droplist_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 V   ALTER TABLE ONLY public.tbl_droplist DROP CONSTRAINT tbl_droplist_created_by_id_fkey;
       public          postgres    false    219    216    4684            �           2606    51420 ,   tbl_droplist tbl_droplist_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_droplist
    ADD CONSTRAINT tbl_droplist_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 V   ALTER TABLE ONLY public.tbl_droplist DROP CONSTRAINT tbl_droplist_deleted_by_id_fkey;
       public          postgres    false    219    216    4684            �           2606    70220 &   tbl_stock_on_hand tbl_droplist_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_droplist_id_fkey FOREIGN KEY (status_id) REFERENCES public.tbl_droplist(id) NOT VALID;
 P   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_droplist_id_fkey;
       public          postgres    false    219    4701    221            �           2606    51415 ,   tbl_droplist tbl_droplist_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_droplist
    ADD CONSTRAINT tbl_droplist_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 V   ALTER TABLE ONLY public.tbl_droplist DROP CONSTRAINT tbl_droplist_updated_by_id_fkey;
       public          postgres    false    216    4684    219            �           2606    68984 5   tbl_held_forms tbl_held_forms_temp_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 _   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_created_by_id_fkey;
       public          postgres    false    4684    226    216            �           2606    68974 9   tbl_held_forms tbl_held_forms_temp_current_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_current_status_id_fkey FOREIGN KEY (current_status_id) REFERENCES public.tbl_droplist(id);
 c   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_current_status_id_fkey;
       public          postgres    false    4701    219    226            �           2606    68994 5   tbl_held_forms tbl_held_forms_temp_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 _   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_deleted_by_id_fkey;
       public          postgres    false    226    4684    216            �           2606    68979 5   tbl_held_forms tbl_held_forms_temp_new_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_new_status_id_fkey FOREIGN KEY (new_status_id) REFERENCES public.tbl_droplist(id);
 _   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_new_status_id_fkey;
       public          postgres    false    4701    219    226            �           2606    68959 2   tbl_held_forms tbl_held_forms_temp_rm_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_rm_code_id_fkey FOREIGN KEY (rm_code_id) REFERENCES public.tbl_raw_materials(id);
 \   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_rm_code_id_fkey;
       public          postgres    false    226    218    4694            �           2606    68969 1   tbl_held_forms tbl_held_forms_temp_rm_soh_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_rm_soh_id_fkey FOREIGN KEY (rm_soh_id) REFERENCES public.tbl_stock_on_hand(id);
 [   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_rm_soh_id_fkey;
       public          postgres    false    4707    221    226            �           2606    68989 5   tbl_held_forms tbl_held_forms_temp_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 _   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_updated_by_id_fkey;
       public          postgres    false    216    4684    226            �           2606    68964 4   tbl_held_forms tbl_held_forms_temp_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_held_forms
    ADD CONSTRAINT tbl_held_forms_temp_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.tbl_warehouses(id);
 ^   ALTER TABLE ONLY public.tbl_held_forms DROP CONSTRAINT tbl_held_forms_temp_warehouse_id_fkey;
       public          postgres    false    4687    226    217            �           2606    69848 &   tbl_notes tbl_notes_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_notes
    ADD CONSTRAINT tbl_notes_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 P   ALTER TABLE ONLY public.tbl_notes DROP CONSTRAINT tbl_notes_created_by_id_fkey;
       public          postgres    false    4684    228    216            �           2606    69858 &   tbl_notes tbl_notes_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_notes
    ADD CONSTRAINT tbl_notes_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 P   ALTER TABLE ONLY public.tbl_notes DROP CONSTRAINT tbl_notes_deleted_by_id_fkey;
       public          postgres    false    228    216    4684            �           2606    69843 (   tbl_notes tbl_notes_product_kind_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_notes
    ADD CONSTRAINT tbl_notes_product_kind_id_fkey FOREIGN KEY (product_kind_id) REFERENCES public.tbl_product_kind(id);
 R   ALTER TABLE ONLY public.tbl_notes DROP CONSTRAINT tbl_notes_product_kind_id_fkey;
       public          postgres    false    228    4704    220            �           2606    69853 &   tbl_notes tbl_notes_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_notes
    ADD CONSTRAINT tbl_notes_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 P   ALTER TABLE ONLY public.tbl_notes DROP CONSTRAINT tbl_notes_updated_by_id_fkey;
       public          postgres    false    4684    228    216            �           2606    60435 A   tbl_outgoing_reports tbl_outgoing_reports_temp_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 k   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_created_by_id_fkey;
       public          postgres    false    4684    216    224            �           2606    60445 A   tbl_outgoing_reports tbl_outgoing_reports_temp_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 k   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_deleted_by_id_fkey;
       public          postgres    false    4684    224    216            �           2606    60420 >   tbl_outgoing_reports tbl_outgoing_reports_temp_rm_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_rm_code_id_fkey FOREIGN KEY (rm_code_id) REFERENCES public.tbl_raw_materials(id);
 h   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_rm_code_id_fkey;
       public          postgres    false    218    224    4694            �           2606    60430 =   tbl_outgoing_reports tbl_outgoing_reports_temp_rm_soh_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_rm_soh_id_fkey FOREIGN KEY (rm_soh_id) REFERENCES public.tbl_stock_on_hand(id);
 g   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_rm_soh_id_fkey;
       public          postgres    false    224    4707    221            �           2606    60440 A   tbl_outgoing_reports tbl_outgoing_reports_temp_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 k   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_updated_by_id_fkey;
       public          postgres    false    224    4684    216            �           2606    60425 @   tbl_outgoing_reports tbl_outgoing_reports_temp_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_outgoing_reports
    ADD CONSTRAINT tbl_outgoing_reports_temp_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.tbl_warehouses(id);
 j   ALTER TABLE ONLY public.tbl_outgoing_reports DROP CONSTRAINT tbl_outgoing_reports_temp_warehouse_id_fkey;
       public          postgres    false    224    217    4687            �           2606    60616 C   tbl_preparation_forms tbl_preparation_forms_temp_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 m   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_created_by_id_fkey;
       public          postgres    false    216    4684    225            �           2606    60626 C   tbl_preparation_forms tbl_preparation_forms_temp_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 m   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_deleted_by_id_fkey;
       public          postgres    false    225    4684    216            �           2606    60601 @   tbl_preparation_forms tbl_preparation_forms_temp_rm_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_rm_code_id_fkey FOREIGN KEY (rm_code_id) REFERENCES public.tbl_raw_materials(id);
 j   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_rm_code_id_fkey;
       public          postgres    false    225    4694    218            �           2606    60611 ?   tbl_preparation_forms tbl_preparation_forms_temp_rm_soh_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_rm_soh_id_fkey FOREIGN KEY (rm_soh_id) REFERENCES public.tbl_stock_on_hand(id);
 i   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_rm_soh_id_fkey;
       public          postgres    false    221    225    4707            �           2606    60621 C   tbl_preparation_forms tbl_preparation_forms_temp_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 m   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_updated_by_id_fkey;
       public          postgres    false    4684    225    216            �           2606    60606 B   tbl_preparation_forms tbl_preparation_forms_temp_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_preparation_forms
    ADD CONSTRAINT tbl_preparation_forms_temp_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.tbl_warehouses(id);
 l   ALTER TABLE ONLY public.tbl_preparation_forms DROP CONSTRAINT tbl_preparation_forms_temp_warehouse_id_fkey;
       public          postgres    false    4687    217    225            �           2606    51570 4   tbl_product_kind tbl_product_kind_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_product_kind
    ADD CONSTRAINT tbl_product_kind_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 ^   ALTER TABLE ONLY public.tbl_product_kind DROP CONSTRAINT tbl_product_kind_created_by_id_fkey;
       public          postgres    false    220    216    4684            �           2606    51580 4   tbl_product_kind tbl_product_kind_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_product_kind
    ADD CONSTRAINT tbl_product_kind_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 ^   ALTER TABLE ONLY public.tbl_product_kind DROP CONSTRAINT tbl_product_kind_deleted_by_id_fkey;
       public          postgres    false    216    220    4684            �           2606    51575 4   tbl_product_kind tbl_product_kind_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_product_kind
    ADD CONSTRAINT tbl_product_kind_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 ^   ALTER TABLE ONLY public.tbl_product_kind DROP CONSTRAINT tbl_product_kind_updated_by_id_fkey;
       public          postgres    false    216    220    4684            �           2606    60278 C   tbl_receiving_reports tbl_receiving_reports_temp_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 m   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_created_by_id_fkey;
       public          postgres    false    223    216    4684            �           2606    60288 C   tbl_receiving_reports tbl_receiving_reports_temp_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 m   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_deleted_by_id_fkey;
       public          postgres    false    223    216    4684            �           2606    60263 @   tbl_receiving_reports tbl_receiving_reports_temp_rm_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_rm_code_id_fkey FOREIGN KEY (rm_code_id) REFERENCES public.tbl_raw_materials(id);
 j   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_rm_code_id_fkey;
       public          postgres    false    218    223    4694            �           2606    60273 ?   tbl_receiving_reports tbl_receiving_reports_temp_rm_soh_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_rm_soh_id_fkey FOREIGN KEY (rm_soh_id) REFERENCES public.tbl_stock_on_hand(id);
 i   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_rm_soh_id_fkey;
       public          postgres    false    4707    223    221            �           2606    60283 C   tbl_receiving_reports tbl_receiving_reports_temp_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 m   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_updated_by_id_fkey;
       public          postgres    false    223    216    4684            �           2606    60268 B   tbl_receiving_reports tbl_receiving_reports_temp_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_receiving_reports
    ADD CONSTRAINT tbl_receiving_reports_temp_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.tbl_warehouses(id);
 l   ALTER TABLE ONLY public.tbl_receiving_reports DROP CONSTRAINT tbl_receiving_reports_temp_warehouse_id_fkey;
       public          postgres    false    217    4687    223            �           2606    59867 6   tbl_stock_on_hand tbl_stock_on_hand_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_stock_on_hand_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 `   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_stock_on_hand_created_by_id_fkey;
       public          postgres    false    221    216    4684            �           2606    59877 6   tbl_stock_on_hand tbl_stock_on_hand_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_stock_on_hand_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 `   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_stock_on_hand_deleted_by_id_fkey;
       public          postgres    false    4684    221    216            �           2606    59857 3   tbl_stock_on_hand tbl_stock_on_hand_rm_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_stock_on_hand_rm_code_id_fkey FOREIGN KEY (rm_code_id) REFERENCES public.tbl_raw_materials(id);
 ]   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_stock_on_hand_rm_code_id_fkey;
       public          postgres    false    218    221    4694            �           2606    59872 6   tbl_stock_on_hand tbl_stock_on_hand_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_stock_on_hand_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 `   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_stock_on_hand_updated_by_id_fkey;
       public          postgres    false    216    4684    221            �           2606    59862 5   tbl_stock_on_hand tbl_stock_on_hand_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_stock_on_hand
    ADD CONSTRAINT tbl_stock_on_hand_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.tbl_warehouses(id);
 _   ALTER TABLE ONLY public.tbl_stock_on_hand DROP CONSTRAINT tbl_stock_on_hand_warehouse_id_fkey;
       public          postgres    false    217    4687    221            �           2606    69088 =   tbl_transfer_forms tbl_transfer_forms_temp_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 g   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_created_by_id_fkey;
       public          postgres    false    216    4684    227            �           2606    69098 =   tbl_transfer_forms tbl_transfer_forms_temp_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 g   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_deleted_by_id_fkey;
       public          postgres    false    227    4684    216            �           2606    69073 >   tbl_transfer_forms tbl_transfer_forms_temp_from_rm_soh_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_from_rm_soh_id_fkey FOREIGN KEY (from_rm_soh_id) REFERENCES public.tbl_stock_on_hand(id);
 h   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_from_rm_soh_id_fkey;
       public          postgres    false    221    227    4707            �           2606    69063 A   tbl_transfer_forms tbl_transfer_forms_temp_from_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_from_warehouse_id_fkey FOREIGN KEY (from_warehouse_id) REFERENCES public.tbl_warehouses(id);
 k   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_from_warehouse_id_fkey;
       public          postgres    false    227    4687    217            �           2606    69058 :   tbl_transfer_forms tbl_transfer_forms_temp_rm_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_rm_code_id_fkey FOREIGN KEY (rm_code_id) REFERENCES public.tbl_raw_materials(id);
 d   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_rm_code_id_fkey;
       public          postgres    false    4694    218    227            �           2606    69083 9   tbl_transfer_forms tbl_transfer_forms_temp_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.tbl_droplist(id);
 c   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_status_id_fkey;
       public          postgres    false    219    227    4701            �           2606    69078 <   tbl_transfer_forms tbl_transfer_forms_temp_to_rm_soh_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_to_rm_soh_id_fkey FOREIGN KEY (to_rm_soh_id) REFERENCES public.tbl_stock_on_hand(id);
 f   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_to_rm_soh_id_fkey;
       public          postgres    false    221    227    4707            �           2606    69068 ?   tbl_transfer_forms tbl_transfer_forms_temp_to_warehouse_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_to_warehouse_id_fkey FOREIGN KEY (to_warehouse_id) REFERENCES public.tbl_warehouses(id);
 i   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_to_warehouse_id_fkey;
       public          postgres    false    217    4687    227            �           2606    69093 =   tbl_transfer_forms tbl_transfer_forms_temp_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_transfer_forms
    ADD CONSTRAINT tbl_transfer_forms_temp_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 g   ALTER TABLE ONLY public.tbl_transfer_forms DROP CONSTRAINT tbl_transfer_forms_temp_updated_by_id_fkey;
       public          postgres    false    216    4684    227            y           2606    51331 &   tbl_users tbl_users_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_users_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 P   ALTER TABLE ONLY public.tbl_users DROP CONSTRAINT tbl_users_created_by_id_fkey;
       public          postgres    false    216    4684    216            z           2606    51341 *   tbl_users tbl_users_deavtivated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_users_deavtivated_by_id_fkey FOREIGN KEY (deavtivated_by_id) REFERENCES public.tbl_users(id);
 T   ALTER TABLE ONLY public.tbl_users DROP CONSTRAINT tbl_users_deavtivated_by_id_fkey;
       public          postgres    false    216    216    4684            {           2606    51346 &   tbl_users tbl_users_department_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_users_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.tbl_departments(id);
 P   ALTER TABLE ONLY public.tbl_users DROP CONSTRAINT tbl_users_department_id_fkey;
       public          postgres    false    215    216    4680            |           2606    51336 &   tbl_users tbl_users_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_users_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 P   ALTER TABLE ONLY public.tbl_users DROP CONSTRAINT tbl_users_updated_by_id_fkey;
       public          postgres    false    216    216    4684            }           2606    51362 0   tbl_warehouses tbl_warehouses_created_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_warehouses
    ADD CONSTRAINT tbl_warehouses_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.tbl_users(id);
 Z   ALTER TABLE ONLY public.tbl_warehouses DROP CONSTRAINT tbl_warehouses_created_by_id_fkey;
       public          postgres    false    216    217    4684            ~           2606    51372 0   tbl_warehouses tbl_warehouses_deleted_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_warehouses
    ADD CONSTRAINT tbl_warehouses_deleted_by_id_fkey FOREIGN KEY (deleted_by_id) REFERENCES public.tbl_users(id);
 Z   ALTER TABLE ONLY public.tbl_warehouses DROP CONSTRAINT tbl_warehouses_deleted_by_id_fkey;
       public          postgres    false    217    216    4684                       2606    51367 0   tbl_warehouses tbl_warehouses_updated_by_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tbl_warehouses
    ADD CONSTRAINT tbl_warehouses_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.tbl_users(id);
 Z   ALTER TABLE ONLY public.tbl_warehouses DROP CONSTRAINT tbl_warehouses_updated_by_id_fkey;
       public          postgres    false    4684    216    217            P   N   x���� �w��2���K>(�	��)i���L�LC�]%���z���1x=�g�KGl�6��n�'}/�Ik�      I   <  x�}��N1뻧��i���_/@CCc��)$�����( !�z�����o���[�Pr�b���\��g}޿����4o�f��mX�ux���#$4`쀒0$�F�d����?흘U�-�3�R�B�6�S���Đ�����a��I�E����H>"�e�/ړ)�[��[m�Q"��3D��N�*�iCwW7���^'�-ۏn9��Ib�0���o{H̉��D����@�p̵@T�!(��`�������Zu�˼�=���`ZW1�«4�)��>�נSWh}���B�ɨ���T_���OgH��'1N�8�i�8�}�	�S��      M   �   x���=�0�9=Ew�*v�{N��m\(�T*��������G��	i��`)iC!�y�#yI��Qι��i-�/K�*Y{5+��@#�m5�dz�%oB���&����d Gz6'�g�{�H8v�|e�7�^b^�[ɲ�r��벖��XuX��_Clr���kݖr��aR�L�y����i���y      T      x������ � �      V      x������ � �      R      x������ � �      S      x������ � �      N   s   x�sq�t)�Tp���/���L�4202�50�54Q04�26�2�г40666�'�
F\�N����%�EI�%�P��K�2��17�25�374056G�2��21�3�475�@���� ��(�      L      x��]]�U7�}>��O��lɲy��@�!�"L2T�����fi_�B.=UiSݕ&}�G����Z��MQ"g�!k��;�P)���J#G�{���ۿ~���[�IB��ң؞Dz"�8f�X�+�������ׯ?��"�R�+]:�l�2G��Z�=�H�2��D}���<`��~2*��n-�އN�����bj1���ݨ<d�ⓜ�pz�8	}��>�dv�!1/	i�l$�׸�H����h�͖���ql��7���O?��0��jP���+��%���Z=��s�Y}p��$ӓ$�)�$��j����'[���[rwb١�5B�{��(i]n�~�l�����A������LMsIa�u�PK͡��W:2�R<k�[���4��r���>�ܢƶ��i~أ��Uk��ƦΝ�X��5�2g\QG��v�����!+uh�������۰͚(Mkh�X���ZhF���D��Å�����G�nw��I��EZ��Pp���؁~�ֺ0\�������8��h�0)w�Z��^�p���>��&�y+�9C�\G���:�q��J+�W�A ��(1��^��+\;0)TY�������M˙�L���
l�Y'1��V\Z�����c����
)�6�����.�b�oO�t�h��.�~<W���WW�Q�h�7=����-�{��)}�
����S�b:�������J��/�2!rF�Ñ���+I�M��Z��dqiL,����s�4�2];�M������.���G(�K����#��21h�� �d�����
�VnO_�x���������j�`N9;>騡�:m�VV��3:���,�:B���rr�z@BO����3:�O*ö�(@�a0��M2E�I�l��p��ʣ�Y����a��!pK��]c�۳t��0�<��B�� �+8L.�|T{?K�wx��>��c�5�i�� uf������L�&�2{����v�i̹���n��anJ���j	��  T@��DuÃ��zc��rr <=���H�S����4V��4u�r��<�{]5s�u��|O�q1�~��_�8� �,1ښt{��4P@���Yg��p��X. 
T��-s��i����k
;��J	T�p�h5����5V.eR�����5@�'��� �fO+J]d�VȶP!�sѰ�@������c�]�Ҡ�A(�d	��T���Vэ'���Z�=��B�6졻�r�8v��n�����-C�!���,��хW* B��l:�Q�H���od��`V��pWEvX����S����V�ѐPY�Y�iƺ@��ٞ�y�=�C��e��r������h����
�ԑ�F\	V�Qc,�Q�em<�ק�̴�@VWH��l���"�m�"��f��<�V��bD�NИ@,_�i�Ż�=luX� 	 QH �9i�)nƯ�'�����1"z.�T��b�@�!V�ܞ�M�e4���q��qA�gW$1O�f������p������f����նԚ�u�����P�s��YaH�1+�I@S��:ر�^��Y`��;a�#�4�3T^q)E!N:����`�<�����>�hc&�9��M����9 �ZN!���0������J�9S��?����4-_��5��&nh���.�PQl�e�p���`�x1w r\� c�r��"<���?^�y��?(x�mu��#x! /W� �I#�~��f�y�Ǐ?�=ͧf����#N��eZ���s�m��^�.�^3�b��4��u2*+T6��n/O��X�#�m�R���{���0�PKQ`����$+(/o���v���W:�_��I��1�;�/H��%����h�R���<̤Z����C&'��-@�8���c��v����J�
elP��SAڡ[ہ�L�N#��?�D���K��C��U�0�=����	�AuH�X�*z<��*e./�������fH���4�tﰬ?��\��=zs%� R��T��R^S�g�#����=���݋��w�V;8����U�-�O�[׼��GO_�Od6�d #~)��J��x�wK_����w/�v��Yd�I���"o�2e�/��������_O'��m��
����*��22��i(�PC�:]@Bly���K/K")y�,$d�7Jj�n�N'��78 �,m` Юm�0#QM��_�N s���A'Ls�34�]E�`J�d�>-�GO�f:V��%�F���Ӧa�zXu�l�Bxp��2�0!}��:�U>,�K�9@b{a0������1�J;|�����^Fג��y�js�F�Z�Ǟ�MOO��&�;{~��ރe�W��������iF�b�{b��$���'�lЇ��w߶&̞��oJ�<�H���*�wF�HQP�n�0X�����Ǎ���c����&�n6!�z��B��ӴP3�"� ����������@���u�:KX�M1O˗K��]�a�l�a���Dr�d�zl��������k/��n�N[e�������]�Q�\�7�pǓ�i!M�QKYS�[?��G����@��^�p��TT�z+�Wr)����	�8�>g�0�GK�Uw09���`Ґ���tK�$��V��fC�ya�A��!��4��4�F���K��~ϊ�)��T?aF4#��
��#�V�=�j	Q��d`� �oz]4�^՗^f�ˢ� SIS��[��IQJ�b�J�Ɏ!r8M Hvy�Ҽ���㐭!n�ݨ�-�fC��L�v�\	{���U�
�7d�Xv.�#>���K�6H�h	����!v�	����t�����BR�;�W��;���w�mD�S���G�5�7Ù\n��k��0�d��HY5h<Z�%���V���rZ]�D�0�]�� �h��T<̛]�"���S&�Ց��>F�U
g�\K�c���0�6�e{�ӞrX���� �W����A:xq�r�K4��ӍG�ƫ�r�b�,�'g�閼Ӹ���G݀����
��:Mt��x,�~]f��gS���H�9�@1�^�B��Hc�헧o^>���ۻ�u.��d1l������!A�����n��>Lĸe-~�U��٦���^������G�^����0�P��?M�X��z�v�*�F�~}���-�n��Mf�����[y�F	.��t�!�W&5�=;�	�����X��$=���zSAc[P)�(��L����LÒظ���|vU��ks�
�J)�.j��^J���$2�j�p,�UG.|M�����Osw�-(� ,�)���K�=�I���al.��0GƖzKu��{��W�%�2���k��	����	�X	٨��Xjp����T#5�kw)$�`$��#C����Һ��iqԐt�P�˂��l���X�D;�����Aq�EcB� hf,�!�Lӊ'�noNwoh�.��VuB�H�Xj�SΫ�u{�N��b��+Ժ66��e4��I��1����ݸV^�K(59'pW�#o-4����� ܘ�aK	Ɏ�UIYa[�9��dH�7ǻ����Zh��{L`SH��>��������h#H�;5�V�JF�%��Ta�0='(;0S��!�(��됢���Ñ���5C�nO  m����ݻպ��`�p�Hl}	UW����])���X=M��?�o�zz]�C5��,=w�D���6�g:W{�ȯ#�:�E% �u'��9��/�����u���m^��S��C��鳚\��z���Ľ��ʆ�[�)�~��&l�N(j�7Q����ε�z��2����~B��L���¯`�3"����a� ꩗�B������]��5�X(C~�~{��/wg͎�]2�LOp�y�F� BL��NoN���Ʒ;��W��J����U�	h$R�e���� 	���f��]�
�uGE����O?b����[�x��aMk6���=]��E�|�P���R {��S6���r��>���9e��qӛ�u1ʛ�l_�>���λ8{�W�7�}`�ER<x�7�}j� ¢ �  �B�@���kH=��3��
�ܳ \�i�;��x��r�|s:�]'�t�p��E�İ�H�V�)e��]��j_�`rJ����"l�f�5��oo�1��?�O�����@��c��0�LN���Ƒ���=o�ul�@������9\�͞�Z�M��w�F�N�z��*5a�r��=}�̌���뺺��9��ϛ�������@h<��j��n\j%�)�U��Uq���ݪ&st	��[a�UMI#�`�t��}3���A��S� #s�1��f�7YM೟d/���6Hn�͞�K|T��=}8Ց�N���X��3%)�/B��aO^�$b`"8�OX���aݠ\���^n����E �rȼM2u�����"���ɧ/�m�^��a_��8^�P�Ž'�{88���V���Cq8J����1/et���|�w_�����s�h{C�	�V2a�5;&���4�I���� ��q�>���@��#�(-�\�3��i�	�-o|�07{8n�����Bx�QA����W���EX���%�b�"a;\�$��
'β����IR���tL?�)%�лN��4��no�we(z��I|���H;dh��SݑO��X!"�+}���kJ�B���*�r1��f4Ic�,����B������ܰz؋S{3U/T/D|`_�2�x�T�D̞>207����'���:.��(ȍr����1Y	���s�ж_�������tCD���@D
N�u�/$���`�
�8�Q-�:j��V���ժ��C7b	�X��^+�&">�,y�����.�$��zzn^&�(Z������˃�̨4���x����y
t�5���T� 6#^E/!�x��������\F}"�w�uAߕU��X=��h��}�˯]v�b#Zm:+ �����nSh��-���Aȭ�)r�NqJ˽�m��J�b�=z��eo`���C���z���Ց�. �
��s=�w� 2v��:���/w�^���5���9��^4�|��?�Z�o�������g���yoО�Q)�U��l��5�q�c��=z��o/=��F~{$���}]���Rb*�H�N�sa����z��%��{�9�t@ҡ~�=��1���f�� ڨ~����KȈd��Q����kE�D |�-��-���˫�~4}:�W�A��R�u�
T��.>g-�����dm�V���ݽ��I9h׾��*ߛ��=�R�
S�7qW�YHȑɠ�2���өqD��B'@Vcó��d��h%P�2�M��,گn�1ųŪ����2 .��	���4/�&�c��(�>��&��v��*v���ݳ;�z���`3Ux�~�?䍶~�k��fV˷w���>-���Z��W�y���RH:3�n�=񬟿���<L���ߚ�+�3]���fH��~q!��y�Û��2�O���B���'��ȝ����R�"�{�b��j��h1Q�����O�6d�>�2����Z�* �b1�>���ӝ�[�� f��[�7h��_4[�W]O�|�D��R��В[�e�YՇ@�����i�*�K~��1Ǭ��~�{�Ry���6��MgP]3�Ov���2�$S����t:}�/��,��O�) Q��QS)���{wA����VN�����\��B_/Tt���}0}:��zN�2�4�z�!��R�zo:�v3�>�ˇ}M� Sl;�Z��ho\L�u7����Ƙ�H��|y��e@x��M�V�A[:��Rh��J�Y�����?������殐���圲]y����p���r^xo�𪉪�f@d �����^���[Ao�~���p�F�{0�]��h����P#-!Uw������:�N�WJ#,O_�3?���~��_&q{�Ǖ��7SAX�k2����P>��l�lF����4�;�}U�8�z>�� P�\BH7�N�ê����Y�W�غ�78J���GӇ�^Qf����򡖒#��mv��������M�d���H�rt�*û!�W^}��ޛ>��j��Mm����e��R�i�stҙ�����Ӆuț�u��>�Ȧ�e( �SM0W�������BS�6 �p4S�����}n��+��.�t��)�O���p
�����/���s�e:��E�3���!��5���Dg���<��c|0-��4.�X�-"�����їU����0}���o���ؽΟ���I�!��[���L����>��_��-)<�{�d7�@3��������<���F��T�}]P`�e�\ׇU�x8}T�2�ܐk�6h!m$ꆬ��}4}�����j�_�ģ��h�O~�u<ӽn�sz:�O�퓀����p3�]Y�D���Gj�L@�`64Ȝ M��g���O�z��B7#U�mW:k-�BL^*�F���O�S�i�!���@{Z>$T?֒SbX=�֬Ʉć�z_����mڱM2���C�+���B���2�{�����:�~�t�~|,�N�R�U��" Z�N~	��>�����06�V4V�l�O��}/��v���m�=�l�
ɶ���OCg�aU�حT|
��S�B��K��:��,$�@\M�NAu���'�~vG	����)�	;|Z"gU5�ew���)?�,,{���=����k���%���O�ݰ
�!}*��=}u+�y���l�	�$�� >?�2~j0{��@ޏ�垙�Rrr��J�D`���fOߏ�Uk�1(�eBk�݋\9T��=��=��3�hS�4���o[�	�RgS�-~d��ӥ�F�*x�ȇ���A[����������q��ƗȮi����|�M�n�j9�{��2�`�רİ��>��-z��<�r��a�t	�5!���x#L��0k*�r�P)n�t�H)>l!oo�x�-[��32�������?��]�����f����[n����=�f�YO�ZrV~͐��;�u��w��}���@ն��U�'��{�� �ʵ�ӕ�1W-2CY~�^|�\m�sp�Q�q{��2�Z�2�#W�N��R��h���N��E���7*xA���|��x!��ޟ&ǣ�%蔮)������j�=�μ<�����P�)k|��1��J�{k]��O�����dq��>4��6���DV�����nE��IεV]�j�����%�Wz�/���}^�����
��lmfE����^��/e���E�v�O�i}$�=���t�U���$A�ߙ�
�[S�]�����ݘ�1
�MP�3~ɲ����2�eE���ap�3YEr��6�g��m4��%S8��CQA��Ř�W�+B�/ai���Bu����Z|�>�֧�xs5H�R��� r{ߎ���V���^�71ɢ!`�l���Xl;ݲ5�R/�d�f��7��,��Q����u&�H8p�+����Վ�k��.p�����O�^���a�3��ޙ�~cuL�(�8��Y��]oOO��@jQ�A+��3�[���|ښկ56ǧ���G�~yy�t����G%?'x�K$� B����	���M@�G����$��"�T�l�[�~�������|7Tm�R��
�
���Zw��ב��s~m�?h�O�~��#{ASA�7����)�J��;�y������,��T�Dy��Iʟ�>��g�Z�*o����~�&�}���b�l����r/+���<I�$��15��K��9�1��!>������o����V�����ڏ���$�ǵ	B�V���3��7)[���N�.ʲ�!A��	�vR�5<~��"�k"���?}�y�u4�7<���oo [�ls7H��|�ڷ����j$В�կ>�d�'�G�p8nNT#�t$�n䞻�Q�0>}�>���jy��W�~����O:�����?�q3rv�T��p{Ky�ק/�O(?N�U��_}���GP(�/*q��ſ0ۗ�}���폿�/�7��?��~����.�`K}�4'��B�a,�Ky���]�&_Ot�W�G�>�G7�@���?�d�_������      Q      x������ � �      O      x������ � �      U      x������ � �      J   �   x����
�@ 뻯��{��GZ��/H���  Q���Bka���{3bh�"HSk0sIC�;o�^�ݝlm�Ͷ�~*`p���}��잎�0@���q$X�p9b�S���)�I5�(�PzmP���Rc���'�/�      K   �   x���1�0�9=E%F�*v'�!XY�8M,6$����HHl�_�ߦQ+%I��jP<)����2aN�Yo�r}��x@���9��#`�Hs�0����?R�bM)@�$��#l�=���	�ղ��?}�h��忀�)��وk^�
ڰk��jr���	Gs���TR���[�^�5/�0O�Nh     