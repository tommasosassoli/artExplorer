CREATE TABLE Artwork(
    artpediaId INT PRIMARY KEY,
    description TEXT);

CREATE TABLE Association(
    artworkId INT,
    startX INT,
    startY INT,
    endX INT,
    endY INT,
    startCh INT,
    endCh INT,
    FOREIGN KEY (artworkId) REFERENCES Artwork(artpediaId)
    )