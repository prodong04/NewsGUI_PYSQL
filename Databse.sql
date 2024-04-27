-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Press`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Press` (
  `Press_ID` INT NOT NULL,
  `Channel` VARCHAR(45) NULL,
  `FollowNumber` INT NULL,
  PRIMARY KEY (`Press_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Reporter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Reporter` (
  `Reporter_ID` INT NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  `Article_ID` INT NOT NULL,
  `Press_Press_ID` INT NOT NULL,
  PRIMARY KEY (`Reporter_ID`, `Press_Press_ID`),
  INDEX `fk_Reporter_Press1_idx` (`Press_Press_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Reporter_Press1`
    FOREIGN KEY (`Press_Press_ID`)
    REFERENCES `mydb`.`Press` (`Press_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Article`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Article` (
  `Article_ID` INT NOT NULL,
  `Title` VARCHAR(45) NOT NULL,
  `Date` DATE NOT NULL,
  `Content` LONGTEXT NOT NULL,
  `Recommendations` INT NULL,
  `Comments` INT NULL,
  `Press_Press_ID` INT NOT NULL,
  `Reporter_Reporter_ID` INT NOT NULL,
  `Reporter_Press_Press_ID` INT NOT NULL,
  PRIMARY KEY (`Article_ID`, `Press_Press_ID`, `Reporter_Reporter_ID`, `Reporter_Press_Press_ID`),
  INDEX `fk_Article_Press1_idx` (`Press_Press_ID` ASC) VISIBLE,
  INDEX `fk_Article_Reporter1_idx` (`Reporter_Reporter_ID` ASC, `Reporter_Press_Press_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Article_Press1`
    FOREIGN KEY (`Press_Press_ID`)
    REFERENCES `mydb`.`Press` (`Press_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Article_Reporter1`
    FOREIGN KEY (`Reporter_Reporter_ID` , `Reporter_Press_Press_ID`)
    REFERENCES `mydb`.`Reporter` (`Reporter_ID` , `Press_Press_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Keyword`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Keyword` (
  `Keyword_ID` INT NOT NULL,
  `Keyword` VARCHAR(45) NOT NULL,
  `Article_Article_ID` INT NOT NULL,
  PRIMARY KEY (`Keyword_ID`, `Article_Article_ID`),
  INDEX `fk_Keyword_Article1_idx` (`Article_Article_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Keyword_Article1`
    FOREIGN KEY (`Article_Article_ID`)
    REFERENCES `mydb`.`Article` (`Article_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
