CREATE OR REPLACE FUNCTION ensure_monthly_partition(tbl TEXT, year INT, month INT) RETURNS VOID AS $$
DECLARE
    start_date DATE := make_date(year, month, 1);
    end_date DATE := (make_date(year, month, 1) + interval '1 month');
    part_name TEXT := format('%s_%s_%s', tbl, year, lpad(month::text, 2, '0'));
    sql TEXT;
BEGIN
    sql := format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L);',
        part_name, tbl, start_date, end_date
    );
    EXECUTE sql;
END;
$$ LANGUAGE plpgsql;
