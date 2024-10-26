USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Select_All_Data_old]    Script Date: 26-10-2024 18:39:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



 

 
 


-- SELECT data
CREATE PROCEDURE [dbo].[Select_All_Data_old]
AS
SELECT

--   --WindowsCluster.WinClusterID,

--   WindowsCluster.WinClusterIP,

--   WindowsCluster.WinClusterName,

            ----Node.NodeID,

--   Node.NodeIP,

--   Node.NodeName,

            --Node.BackupIP,

            --Node.OS_Version,

--   --SQLCluster.SQLClusterID,

--   SQLCluster.SQLClusterIP,

--   SQLCluster.SQLClusterName,

            --SQLCluster.SQLServerVersion,

--   --Application.ApplicationID,

--   Application.ApplicationName

[dbo].[WindowsCluster].*,[dbo].[Node].*,[dbo].[SQLCluster].*,[dbo].[Application].*

  

FROM

    WindowsCluster

JOIN

    Node ON WindowsCluster.WinClusterID = Node.WinClusterID

JOIN

    NodeSQLCluster ON Node.NodeID = NodeSQLCluster.NodeID

JOIN

    SQLCluster ON NodeSQLCluster.SQLClusterID = SQLCluster.SQLClusterID

JOIN

    SQLClusterApplication ON SQLCluster.SQLClusterID = SQLClusterApplication.SQLClusterID

JOIN

    Application ON SQLClusterApplication.ApplicationID = Application.ApplicationID;

GO


