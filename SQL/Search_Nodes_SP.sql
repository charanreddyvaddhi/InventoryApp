USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_Nodes]    Script Date: 09-11-2024 01:13:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






CREATE PROCEDURE [dbo].[Search_Nodes]
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold results
    CREATE TABLE #SearchResults (
	[NodeID] [int] NOT NULL,
	[NodeIP] [varchar](15) NULL,
	[NodeName] [varchar](255) NULL,
	[NodeOSVersion] [varchar](255) NULL,
	[NodeComments] [varchar](255) NULL
    );

    -- Search in Windows Cluster Table
    INSERT INTO #SearchResults (NodeID,NodeIP,NodeName,NodeOSVersion,NodeComments)
	SELECT NodeID, NodeIP, NodeName, NodeOSVersion, NodeOSVersion from [dbo].Node
    WHERE 
		 NodeName LIKE '%' + @SearchTerm + '%'
		OR NodeIP LIKE '%' + @SearchTerm + '%'
		OR NodeComments LIKE '%' + @SearchTerm + '%'
		OR NodeName LIKE '%' + @SearchTerm + '%'
		OR NodeOSVersion LIKE '%' + @SearchTerm + '%'
		
    -- Return the results
    SELECT NodeID,NodeIP,NodeName,NodeOSVersion,NodeComments FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


