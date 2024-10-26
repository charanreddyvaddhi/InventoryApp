USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_All_Clusters]    Script Date: 26-10-2024 18:38:25 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[Search_All_Clusters]
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold results
    CREATE TABLE #SearchResults (
        SourceTable NVARCHAR(50),
        ID INT,
        Name NVARCHAR(255),
        AdditionalInfo NVARCHAR(255)
    );

    -- Search in Windows Cluster Table
    INSERT INTO #SearchResults (SourceTable, ID, Name, AdditionalInfo)
    SELECT 'WindowsCluster', WinClusterID, WinClusterName, WinClusterIP
    FROM WindowsCluster
    WHERE WinClusterName LIKE '%' + @SearchTerm + '%'
       OR WinClusterIP LIKE '%' + @SearchTerm + '%';

    -- Search in Node Table
    INSERT INTO #SearchResults (SourceTable, ID, Name, AdditionalInfo)
    SELECT 'Node', NodeID, NodeName, NodeComments
    FROM Node
    WHERE NodeName LIKE '%' + @SearchTerm + '%'
       OR NodeIP LIKE '%' + @SearchTerm + '%'
       OR NodeComments LIKE '%' + @SearchTerm + '%';

    -- Search in SQL Cluster Table
    INSERT INTO #SearchResults (SourceTable, ID, Name, AdditionalInfo)
    SELECT 'SQLCluster', SQLClusterID, SQLClusterName, SQLClusterIP
    FROM SQLCluster
    WHERE SQLClusterName LIKE '%' + @SearchTerm + '%'
       OR SQLClusterIP LIKE '%' + @SearchTerm + '%'
       OR SQLComments LIKE '%' + @SearchTerm + '%';

    -- Search in Application Table
    INSERT INTO #SearchResults (SourceTable, ID, Name, AdditionalInfo)
    SELECT 'Application', ApplicationID, AppName, AppOwner
    FROM Application
    WHERE AppName LIKE '%' + @SearchTerm + '%'
       OR AppOwner LIKE '%' + @SearchTerm + '%'
       OR AppComments LIKE '%' + @SearchTerm + '%'
       OR AppCriticality LIKE '%' + @SearchTerm + '%';

    -- Return the results
    SELECT * FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


