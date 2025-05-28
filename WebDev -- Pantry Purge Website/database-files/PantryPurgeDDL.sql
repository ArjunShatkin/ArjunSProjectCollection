CREATE DATABASE IF NOT EXISTS PantryPurgeDB;
USE PantryPurgeDB;

CREATE TABLE IF NOT EXISTS User (
    UserID int PRIMARY KEY NOT NULL,
    Username varchar(30) NOT NULL,
    Password varchar(30) NOT NULL,
    DateCreated DATE,
    UserStatus varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS CasualCook (
    CookID int PRIMARY KEY NOT NULL,
    PhoneNum varchar(15) NOT NULL,
    Email varchar(50) NOT NULL,
    FirstName varchar(50),
    LastName varchar(50),
    SkillLevel varchar (15),
    DietPrefer varchar(50),
    -- Make a separate table for dietPrefer? Could be a many-to-many relationship to dietary preferences
    -- Same thing with permissions
    NewsOptIn tinyint(1),
    FOREIGN KEY (CookID) REFERENCES User (UserID) ON DELETE CASCADE,
    UNIQUE INDEX uq_idx_id (CookID)
);

CREATE TABLE IF NOT EXISTS Chef (
    ChefID int PRIMARY KEY NOT NULL,
    PhoneNum varchar(15) NOT NULL,
    Email varchar(50) NOT NULL,
    DateJoined date NOT NULL,
    FirstName varchar(50),
    LastName varchar(50),
    NumEndorsements int,
    CuisineSpecialty varchar(15),
    YearsExp smallint,
    SocialTag varchar(30),
    Bio varchar(600),
    City varchar(20),
    StateName varchar(20),
    Country varchar (50),
    FOREIGN KEY (ChefID) REFERENCES User(UserID) ON DELETE CASCADE,
    UNIQUE INDEX uq_idx_chefId (ChefID)
);

CREATE TABLE IF NOT EXISTS Recipe (
    RecipeID int PRIMARY KEY AUTO_INCREMENT,
    Servings smallint,
    Difficulty varchar(15),
    Calories int,
    RecipeName varchar(50) NOT NULL,
    PublishDate date,
    Description varchar(1000),
    Cuisine varchar(15),
    PrepTimeMins int,
    CookTimeMins int,
    VideoUrl varchar(100),
    NumReviews int,
    -- aggregateRate - not sure what this is, don't know how to format
    NumViews int,
    NumShares int,
    NewsSubStat varchar(15),
    IsFeatured tinyint(1),
    ChefID int,
    FOREIGN KEY (ChefID) REFERENCES Chef(ChefID) ON DELETE CASCADE,
    UNIQUE INDEX uq_idx_recipeId (recipeID)
);

CREATE TABLE IF NOT EXISTS Ingredient (
    IngredientID int PRIMARY KEY NOT NULL,
    IngredientName varchar(30),
    CalPerUnit int,
    -- should dietary restriction category be here? if so it might need to be in another table
    MeasureUnit varchar(20),
    CostPerUnit numeric(8, 2),
    UNIQUE INDEX uq_idx_ingId (IngredientID)
);

CREATE TABLE IF NOT EXISTS RecipeIngredient (
    RecipeID int NOT NULL,
    IngredientID int NOT NULL,
    Quantity decimal(8, 2),
    PRIMARY KEY (RecipeID, IngredientID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe (RecipeID)
    ON DELETE CASCADE,
    FOREIGN KEY (IngredientID) REFERENCES Ingredient (IngredientID),
    INDEX idx_recipeId (RecipeID),
    INDEX idx_ingredientId (IngredientID)
);

CREATE TABLE IF NOT EXISTS Substitute (
    SubbedOutID int NOT NULL,
    SubbedWithID int NOT NULL,
    SubstituteReason varchar(50),
    FOREIGN KEY (SubbedOutID) REFERENCES Ingredient (IngredientID),
    FOREIGN KEY (SubbedWithID) REFERENCES Ingredient (IngredientID),
    PRIMARY KEY (SubbedOutID, SubbedWithID),
    INDEX idx_subbedOutId (SubbedOutID),
    INDEX idx_subbedWithId (SubbedWithID)
);

CREATE TABLE IF NOT EXISTS Follows (
    FollowerID int NOT NULL,
    FolloweeID int NOT NULL,
    DateFollowed date,
    FOREIGN KEY (FollowerID) REFERENCES CasualCook (CookID),
    FOREIGN KEY (FolloweeID) REFERENCES Chef (ChefID),
    PRIMARY KEY (FollowerID, FolloweeID),
    INDEX idx_followerId (FollowerID),
    INDEX idx_followeeId (FolloweeID)
);

CREATE TABLE IF NOT EXISTS Review (
    CookID int NOT NULL,
    RecipeID int NOT NULL,
    Rating smallint,
    -- Should we include a subject line for the review?
    ReviewText varchar(800),
    ReviewDate date,
    FOREIGN KEY (CookID) REFERENCES CasualCook (CookID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe (RecipeID) ON DELETE CASCADE,
    PRIMARY KEY (CookID, RecipeID),
    INDEX idx_cookId (CookID),
    INDEX idx_recipeId (RecipeID)
);

CREATE TABLE IF NOT EXISTS Shares (
    CookID int NOT NULL,
    RecipeID int NOT NULL,
    SharePlatform varchar(20),
    ShareDate date,
    FOREIGN KEY (CookID) REFERENCES CasualCook (CookID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe (recipeID) ON DELETE CASCADE,
    PRIMARY KEY (CookID, RecipeID),
    INDEX idx_cookId (CookID),
    INDEX idx_recipeId (RecipeID)
);

CREATE TABLE IF NOT EXISTS OffsiteTraffic (
    TrafficID int PRIMARY KEY NOT NULL,
    RecipeID int NOT NULL,
    SrcName  varchar(20),
    DateTracked date,
    ClickCount int,
    FOREIGN KEY (RecipeID) 
        REFERENCES Recipe (RecipeID) 
        ON DELETE CASCADE,
    UNIQUE INDEX uq_idx_trafficId (TrafficID)
);


CREATE TABLE IF NOT EXISTS Endorses (
    EndorsingChefID int NOT NULL,
    EndorsedChefID int NOT NULL,
    DateEndorsed date,
    EndorseMessage varchar(300),

    -- Are the  following two lines redundant?
    FOREIGN KEY (EndorsingChefID) REFERENCES Chef (chefID),
    PRIMARY KEY (EndorsingChefID, EndorsedChefID),
    INDEX idx_endorsingChefId (EndorsingChefID),
    INDEX idx_endorsedChefId (EndorsedChefID)

);


CREATE TABLE IF NOT EXISTS Analyst (
    AnalysisID int NOT NULL,
    Name varchar(50) NOT NULL,
    Permissions varchar(100),
    PhoneNum varchar(20),
    Department varchar(100),
    HireDate date,
    FOREIGN KEY (AnalysisID) REFERENCES User (UserID) ON DELETE CASCADE,
    UNIQUE INDEX uq_idx_AnalysisId (AnalysisID)
);

CREATE TABLE IF NOT EXISTS Administrator (
    AdminID int NOT NULL,
    Name varchar(50) NOT NULL,
    Permissions varchar(100),
    PhoneNum varchar(20),
    Department varchar(100),
    HireDate date,
    FOREIGN KEY (AdminID) REFERENCES User (UserID) ON DELETE CASCADE,
    UNIQUE INDEX uq_idx_AdminId (AdminID)
);

CREATE TABLE IF NOT EXISTS Issue (
    IssueID int NOT NULL,
    UserID int NOT NULL,
    EnteredTime datetime,
    Priority varchar(20),
    Status varchar(30),
    Title varchar(40),
    Description varchar(500),
    ResolvedDate datetime,
    FOREIGN KEY (UserID) REFERENCES User (UserID),
    UNIQUE INDEX uq_idx_IssueID (IssueID)
);

CREATE TABLE IF NOT EXISTS Search (
    SearchId int PRIMARY KEY NOT NULL,
    CookID int NOT NULL,
    AppliedFilters TEXT,
    SearchDate datetime,
    QueryText varchar(200),
    FOREIGN KEY (CookID) REFERENCES CasualCook (CookID)
);

CREATE TABLE IF NOT EXISTS SearchIngredient (
    IngredientID int NOT NULL,
    SearchID int,
    PRIMARY KEY (IngredientID,SearchID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredient (IngredientID),
    FOREIGN KEY (SearchID) REFERENCES Search (SearchID)
);

CREATE TABLE IF NOT EXISTS DietaryRestrictions (
    DietRestID int PRIMARY KEY NOT NULL,
    RestName varchar(30) NOT NULL,
    Description varchar(500)
);
CREATE TABLE IF NOT EXISTS SearchDiet (
    SearchID int NOT NULL,
    DietRestID int,
    PRIMARY KEY (SearchID,DietRestID),
    FOREIGN KEY (SearchID) REFERENCES Search (SearchID),
    FOREIGN KEY (DietRestID) REFERENCES DietaryRestrictions (DietRestID)
);

CREATE TABLE IF NOT EXISTS DietRecipe (
    DietRestID int,
    RecipeID int,
    PRIMARY KEY (DietRestID, RecipeID),
    FOREIGN KEY (DietRestID) REFERENCES DietaryRestrictions (DietRestID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe (RecipeID)
);

CREATE TABLE IF NOT EXISTS Newsletter (
    ChefID int,
    RecipeID int,
    SubID int PRIMARY KEY AUTO_INCREMENT,
    SubStatus varchar(30),
    SubDate datetime,
    FOREIGN KEY (ChefID) REFERENCES Chef (ChefID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (RecipeID) REFERENCES Recipe (RecipeID) ON DELETE CASCADE ON UPDATE CASCADE
);

