DELIMITER $$

CREATE TRIGGER prevent_second_admin_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
  IF NEW.role = 'admin' THEN
    IF (SELECT COUNT(*) FROM users WHERE role = 'admin') > 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Only one admin is allowed.';
    END IF;
  END IF;
END$$

CREATE TRIGGER prevent_second_admin_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
  IF NEW.role = 'admin' AND OLD.role != 'admin' THEN
    IF (SELECT COUNT(*) FROM users WHERE role = 'admin') > 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Only one admin is allowed.';
    END IF;
  END IF;
END$$

DELIMITER ;
