CREATE OR REPLACE FUNCTION update_pmt_status()
  RETURNS trigger AS
$$
BEGIN
UPDATE "CheapHerder_payment" SET status='cancelled'
	where "CheapHerder_payment".payment_id IN 
	(select payment_id_id from "CheapHerder_pledge" where "CheapHerder_pledge".group_id_id=OLD.group_id_id);
RETURN OLD;
END;

$$
LANGUAGE 'plpgsql';



CREATE TRIGGER prep_delete 
BEFORE DELETE 
ON "CheapHerder_pledge"
FOR EACH ROW
EXECUTE PROCEDURE update_pmt_status();
