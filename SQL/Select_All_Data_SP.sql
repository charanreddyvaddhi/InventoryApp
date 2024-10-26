USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Select_All_Data]    Script Date: 26-10-2024 18:39:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


-- SELECT data
CREATE PROCEDURE [dbo].[Select_All_Data]
AS
SELECT
	[WindowsCluster].[WinClusterIP] AS WinCluster_IP ,
	[WindowsCluster].[WinClusterName] AS WinCluster_Name,
	[Node].[NodeIP] AS Device_IP ,
	[Node].[NodeName] Hostname  ,
	[SQLCluster].[SQLClusterIP] AS DB_IP , 
	[SQLCluster].[SQLClusterName] AS SQLCluster_Name , 
	[SQLCluster].[SQLInstanceName] AS SQLInstance_Name, 
	[SQLCluster].[SQLPort] AS DB_Port,
	[SQLCluster].[SQLType] AS SQL_Type,     
	[Application].[AppName] AS Application_Name , 
	[Application].[AppOwner], 
	[Application].[AppOwnerEmail], 
	[Application].[AppVersion], 
	[Application].[AppDepartment], 
	[Application].[AppCriticality],
	
	[Node].[NodeOSVersion] AS OS_Version,
	[SQLCluster].[SQLServerVersion] AS SQL_Version,
	[SQLCluster].[SQLServerEdition] AS SQL_Edition,
	[SQLCluster].[MSDTCIP],
	[SQLCluster].[NARsRaised],
	[Node].[NodeComments],
	[SQLCluster].[SQLComments],
	[Application].[AppComments], 
	
	[WindowsCluster].[WinClusterID],
	[Node].[NodeID],
	[Node].[WinClusterID] AS WinClusterID_Node,
	[SQLCluster].[SQLClusterID],
	[Application].[ApplicationID]
FROM
    [WindowsCluster]

JOIN
    [Node] ON [WindowsCluster].[WinClusterID] = [Node].[WinClusterID]
JOIN
    [NodeSQLCluster] ON [Node].[NodeID] = [NodeSQLCluster].[NodeID]
JOIN
    [SQLCluster] ON [NodeSQLCluster].[SQLClusterID] = [SQLCluster].[SQLClusterID]
JOIN
    [SQLClusterApplication] ON [SQLCluster].[SQLClusterID] = [SQLClusterApplication].[SQLClusterID]
JOIN
    [Application] ON [SQLClusterApplication].[ApplicationID] =[Application].[ApplicationID]
GO


