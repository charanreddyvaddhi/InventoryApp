USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_WinClusters]    Script Date: 09-11-2024 01:15:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



CREATE PROCEDURE [dbo].[Search_WinClusters]
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold results
    CREATE TABLE #SearchResults(
        [WinClusterID] [int],
        [WinClusterIP] [varchar](15),
		[WinClusterName] [varchar](255)
        
    );

    -- Search in Windows Cluster Table
    INSERT INTO #SearchResults (WinClusterID, WinClusterIP, WinClusterName)
    SELECT [WinClusterID], [WinClusterIP], [WinClusterName]
    FROM [Inv].[dbo].[WindowsCluster]
    WHERE  
        WinClusterID = TRY_CAST(@SearchTerm AS INT) OR
        WinClusterIP LIKE '%' + @SearchTerm + '%' OR
        WinClusterName LIKE '%' + @SearchTerm + '%' ;
    
    -- Return the results
    SELECT * FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


