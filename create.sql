drop table if exists Item; 
drop table if exists Category; 
drop table if exists User; 
drop table if exists Bids; 
 
create table Category(
    ItemID INTEGER NOT NULL, 
    Category CHAR(500), 
    PRIMARY KEY (ItemID,Category), 
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID));

create table User(
    UserID CHAR(500) PRIMARY KEY, 
    Rating INTEGER NOT NULL, 
    Location CHAR(500), 
    Country CHAR(500)); 

create table Bids(
    ItemID INTEGER NOT NULL, 
    UserID CHAR(500), 
    Time TIMESTAMP NOT NULL, 
    Amount DECIMAL NOT NULL, 
    PRIMARY KEY(ItemID,UserID,Amount),
    FOREIGN KEY(UserID) REFERENCES User(UserID), 
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)); 

create table Item(
    ItemID INTEGER NOT NULL PRIMARY KEY, 
    SellerID CHAR(500) NOT NULL, 
    Name CHAR(500) NOT NULL, 
    Currently DECIMAL NOT NULL,
    First_Bid DECIMAL NOT NULL, 
    Number_Of_Bids INTEGER NOT NULL, 
    Started TIMESTAMP NOT NULL, 
    Ends TIMESTAMP NOT NULL, 
    Description TEXT); 

