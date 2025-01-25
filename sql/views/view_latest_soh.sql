-- View: public.view_latest_soh

-- DROP VIEW public.view_latest_soh;

CREATE OR REPLACE VIEW public.view_latest_soh
 AS
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
           FROM tbl_stock_on_hand soh
             JOIN tbl_raw_materials rm ON soh.rm_code_id = rm.id
             JOIN tbl_warehouses wh ON soh.warehouse_id = wh.id
             LEFT JOIN tbl_droplist status ON soh.status_id = status.id
        )
 SELECT rankedrecords.warehouseid,
    rankedrecords.warehousename,
    rankedrecords.warehousenumber,
    rankedrecords.rawmaterialid,
    rankedrecords.rmcode,
    rankedrecords.beginningbalance,
    rankedrecords.statusname,
    rankedrecords.statusid,
    rankedrecords.stockchangedate
   FROM rankedrecords
  WHERE rankedrecords.row_num = 1;

ALTER TABLE public.view_latest_soh
    OWNER TO postgres;
