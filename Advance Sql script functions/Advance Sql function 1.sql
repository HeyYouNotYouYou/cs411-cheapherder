CREATE OR REPLACE FUNCTION query_product(query_string varchar(255)) RETURNS TABLE (
item_code varchar(255),
product_name varchar(255),
description text,
quantity varchar(255),
package_size varchar(255),
gross_weight varchar(255),
category varchar(255),
image_url varchar(200)
)
AS $$
BEGIN
RETURN QUERY SELECT DISTINCT "CheapHerder_product".item_code,"CheapHerder_product".product_name,"CheapHerder_product".description,"CheapHerder_product".quantity,"CheapHerder_product".package_size,"CheapHerder_product".gross_weight,"CheapHerder_product".category,"CheapHerder_product".image_url from "CheapHerder_product" where (LOWER("CheapHerder_product".product_name) LIKE LOWER('%' || query_string || '%')); 
END; $$

LANGUAGE 'plpgsql';
