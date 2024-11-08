USE [Inv]
GO

/****** Object:  View [dbo].[Search_View]    Script Date: 08-11-2024 10:48:11 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE VIEW [dbo].[Search_View] AS
SELECT
		windowscluster.WinClusterID,	WinClusterIP,	WinClusterName,	sqlcluster.SQLClusterID, 	SQLClusterIP,  	SQLClusterName, 	SQLType, 	SQLInstanceName, 	SQLPort, 	SQLServerVersion,
NARsRaised, 	SQLComments, 	SQLServerEdition, 	MSDTCIP, 	node.NodeID,	NodeIP, 	NodeName, 	NodeOSVersion, 	NodeComments, 	application.ApplicationID, 	AppName, 	AppOwner, 	AppOwnerEmail, 	AppVersion, 	AppDepartment, 	AppComments, 	AppCriticality
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


