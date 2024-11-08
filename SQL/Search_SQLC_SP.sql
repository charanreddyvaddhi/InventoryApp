USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_SQLC]    Script Date: 09-11-2024 01:14:18 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






CREATE PROCEDURE [dbo].[Search_SQLC]
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold results
    CREATE TABLE #SearchResults (
	[SQLClusterID] [int] NOT NULL,
	[SQLClusterIP] [varchar](15) NULL,
	[SQLClusterName] [varchar](255) NULL,
	[SQLType] [nvarchar](100) NULL,
	[SQLInstanceName] [nvarchar](100) NULL,
	[SQLPort] [bigint] NULL,
	[SQLServerVersion] [nvarchar](100) NULL,
	[NARsRaised] [nvarchar](50) NULL,
	[SQLComments] [nvarchar](255) NULL,
	[SQLServerEdition] [nvarchar](50) NULL,
	[MSDTCIP] [nchar](15) NULL
    );

    -- Search in Windows Cluster Table
    INSERT INTO #SearchResults (
	SQLClusterID,SQLClusterIP,SQLClusterName,SQLType,SQLInstanceName,SQLPort,SQLServerVersion,NARsRaised,
	SQLComments,SQLServerEdition,MSDTCIP)
	SELECT SQLClusterID,SQLClusterIP,SQLClusterName,SQLType,SQLInstanceName,SQLPort,SQLServerVersion,NARsRaised,
	SQLComments,SQLServerEdition,MSDTCIP  from [dbo].SQLCluster
    WHERE
		SQLClusterName LIKE '%' + @SearchTerm + '%'
		OR SQLInstanceName LIKE '%' + @SearchTerm + '%'
		OR SQLClusterIP LIKE '%' + @SearchTerm + '%'
		OR SQLComments LIKE '%' + @SearchTerm + '%'
		OR SQLType  LIKE '%' + @SearchTerm + '%'
		OR SQLServerVersion LIKE '%' + @SearchTerm + '%'
		OR NARsRaised LIKE '%' + @SearchTerm + '%'
		OR SQLServerEdition LIKE '%' + @SearchTerm + '%'
		OR MSDTCIP LIKE '%' + @SearchTerm + '%'

		
    -- Return the results
    SELECT * FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


