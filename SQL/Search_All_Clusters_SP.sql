USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_All_Clusters]    Script Date: 08-11-2024 10:48:23 ******/
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
    [WinClusterID] [int] NOT NULL,
	[WinClusterIP] [varchar](15) NULL,
	[WinClusterName] [varchar](255) NULL,
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
	[MSDTCIP] [nchar](15) NULL,
	[NodeID] [int] NOT NULL,
	[NodeIP] [varchar](15) NULL,
	[NodeName] [varchar](255) NULL,
	[NodeOSVersion] [varchar](255) NULL,
	[NodeComments] [varchar](255) NULL,
	[ApplicationID] [int] NOT NULL,
	[AppName] [varchar](255) NULL,
	[AppOwner] [nvarchar](255) NULL,
	[AppOwnerEmail] [nvarchar](255) NULL,
	[AppVersion] [nvarchar](255) NULL,
	[AppDepartment] [nvarchar](255) NULL,
	[AppComments] [nvarchar](255) NULL,
	[AppCriticality] [nchar](50) NULL
    );

    -- Search in Windows Cluster Table
    INSERT INTO #SearchResults (WinClusterID,WinClusterIP,WinClusterName,
	SQLClusterID,SQLClusterIP,SQLClusterName,SQLType,SQLInstanceName,SQLPort,SQLServerVersion,NARsRaised,
	SQLComments,SQLServerEdition,MSDTCIP,NodeID,NodeIP,NodeName,NodeOSVersion,NodeComments,ApplicationID,AppName,
	AppOwner,AppOwnerEmail,AppVersion,AppDepartment,AppComments,AppCriticality)
	SELECT *  from [dbo].[Search_View]
    WHERE WinClusterName LIKE '%' + @SearchTerm + '%'
		OR WinClusterIP LIKE '%' + @SearchTerm + '%'

		OR NodeName LIKE '%' + @SearchTerm + '%'
		OR NodeIP LIKE '%' + @SearchTerm + '%'
		OR NodeComments LIKE '%' + @SearchTerm + '%'
		OR NodeName LIKE '%' + @SearchTerm + '%'
		OR NodeOSVersion LIKE '%' + @SearchTerm + '%'
		
		OR SQLClusterName LIKE '%' + @SearchTerm + '%'
		OR SQLInstanceName LIKE '%' + @SearchTerm + '%'
		OR SQLClusterIP LIKE '%' + @SearchTerm + '%'
		OR SQLComments LIKE '%' + @SearchTerm + '%'
		OR SQLType  LIKE '%' + @SearchTerm + '%'
		OR SQLServerVersion LIKE '%' + @SearchTerm + '%'
		OR NARsRaised LIKE '%' + @SearchTerm + '%'
		OR SQLServerEdition LIKE '%' + @SearchTerm + '%'
		OR MSDTCIP LIKE '%' + @SearchTerm + '%'

		OR AppName LIKE '%' + @SearchTerm + '%'
		OR AppOwner LIKE '%' + @SearchTerm + '%'
		OR AppComments LIKE '%' + @SearchTerm + '%'
		OR AppCriticality LIKE '%' + @SearchTerm + '%'
		OR AppVersion LIKE '%' + @SearchTerm + '%'
		OR AppDepartment LIKE '%' + @SearchTerm + '%'

    -- Return the results
    SELECT 
	[WinClusterIP] AS WinCluster_IP ,
	[WinClusterName] AS WinCluster_Name,
	[NodeIP] AS Device_IP ,
	[NodeName] Hostname  ,
	[SQLClusterIP] AS DB_IP , 
	[SQLClusterName] AS SQLCluster_Name , 
	[SQLInstanceName] AS SQLInstance_Name, 
	[SQLPort] AS DB_Port,
	[SQLType] AS SQL_Type,     
	[AppName] AS Application_Name , 
	[AppOwner], 
	[AppOwnerEmail], 
	[AppVersion], 
	[AppDepartment], 
	[AppCriticality],
	
	[NodeOSVersion] AS OS_Version,
	[SQLServerVersion] AS SQL_Version,
	[SQLServerEdition] AS SQL_Edition,
	[MSDTCIP],
	[NARsRaised],
	[NodeComments],
	[SQLComments],
	[AppComments], 
	
	[WinClusterID],
	[NodeID],
	[WinClusterID] AS WinClusterID_Node,
	[SQLClusterID],
	[ApplicationID] FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


