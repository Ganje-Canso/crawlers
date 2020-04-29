CREATE OR REPLACE PROCEDURE save_home_data(_token bigint, _source_id integer, _time integer, _title character, _category character, _sub_category character, _province character, _city character, _neighbourhood character, _advertiser character, _production integer, _room integer, _area integer, _price bigint, _deposit bigint, _rent bigint, _description character, _url character, _thumbnail character, _latitude double precision, _longitude double precision, _tell character, _swap boolean, _administrative_document boolean, _parking boolean, _elevator boolean, _storeroom boolean, _swap_deposit_rent boolean, _balcony boolean, _estate_floor integer, _estate_direction character, _package boolean, _kitchen character, _cooler boolean, _floor_covering character)
LANGUAGE 'plpgsql' AS $$
BEGIN

INSERT INTO home (token, source_id, time, title ,category ,sub_category ,province ,city , neighbourhood ,advertiser ,production , room, area, price , deposit, rent, description, url, thumbnail, latitude, longitude, tell, swap, administrative_document, parking, elevator, storeroom, swap_deposit_rent, balcony, estate_floor, estate_direction, package, kitchen, cooler, floor_covering)
VALUES (_token, _source_id, _time, _title ,_category ,_sub_category ,_province ,_city , _neighbourhood ,_advertiser ,_production , _room, _area, _price , _deposit, _rent, _description, _url, _thumbnail, _latitude, _longitude, _tell, _swap, _administrative_document, _parking, _elevator, _storeroom, _swap_deposit_rent, _balcony, _estate_floor, _estate_direction, _package, _kitchen, _cooler, _floor_covering);


END;
$$;



CREATE OR REPLACE PROCEDURE save_car_data(_token bigint, _source_id integer, _time integer, _title character, _category character, _sub_category character, _province character, _city character, _neighbourhood character, _production integer, _price bigint, _description character, _url character, _thumbnail character, _latitude double precision, _longitude double precision, _tell character, _swap boolean, _brand character, _consumption bigint, _color character, _cash_installment character, _gear_box character, _company character, _chassis_type character, _model character, _body_condition character, _fuel character)
LANGUAGE 'plpgsql' AS $$
BEGIN

INSERT INTO home (token, source_id, time, title, category, sub_category, province, city, neighbourhood, production, price, description, url, thumbnail, latitude, longitude, tell, swap, brand, consumption, color, cash_installment, gear_box, company, chassis_type, model, body_condition, fuel)
VALUES (_token, _source_id, _time, _title, _category, _sub_category, _province, _city, _neighbourhood, _production, _price, _description, _url, _thumbnail, _latitude, _longitude, _tell, _swap, _brand, _consumption, _color, _cash_installment, _gear_box, _company, _chassis_type, _model, _body_condition, _fuel);
COMMIT;

END;
$$;
