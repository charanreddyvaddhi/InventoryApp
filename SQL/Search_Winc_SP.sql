USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_Winc]    Script Date: 09-11-2024 01:14:47 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






CREATE PROCEDURE [dbo].[Search_Winc]
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold results
    CREATE TABLE #SearchResults (
    [WinClusterID] [int] NOT NULL,
	[WinClusterIP] [varchar](15) NULL,
	[WinClusterName] [varchar](255) NULL
    );

    -- Search in Windows Cluster Table
    INSERT INTO #SearchResults (WinClusterID,WinClusterIP,WinClusterName)
	SELECT WinClusterID,WinClusterIP,WinClusterName  from [dbo].WindowsCluster
    WHERE WinClusterName LIKE '%' + @SearchTerm + '%'
		OR WinClusterIP LIKE '%' + @SearchTerm + '%'


    -- Return the results
    SELECT 
	[WinClusterID] AS WinClusterID, 
	[WinClusterIP] AS WinCluster_IP ,
	[WinClusterName] AS WinCluster_Name
	FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


