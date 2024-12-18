USE [Inv]
GO
/****** Object:  StoredProcedure [dbo].[InsertAllData]    Script Date: 04-10-2024 13:00:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[InsertAllData]
    @WinClusterID INT,
    @WinClusterIP NVARCHAR(255),
    @WinClusterName NVARCHAR(255),
    @NodeID INT,
    @NodeIP NVARCHAR(255),
    @NodeName NVARCHAR(255),
    @NodeOSVersion NVARCHAR(255),
    @NodeComments NVARCHAR(255),
    @SQLClusterID INT,
    @SQLClusterIP NVARCHAR(255),
    @SQLClusterName NVARCHAR(255),
    @SQLType NVARCHAR(255),
    @SQLInstanceName NVARCHAR(255),
    @SQLPort NVARCHAR(255),
    @SQLServerVersion NVARCHAR(255),
    @NARsRaised NVARCHAR(255),
    @SQLComments NVARCHAR(255),
    @SQLServerEdition NVARCHAR(255),
    @MSDTCIP NVARCHAR(255),
    @ApplicationID INT,
    @AppName NVARCHAR(255),
    @AppOwner NVARCHAR(255),
    @AppOwnerEmail NVARCHAR(255),
    @AppVersion NVARCHAR(255),
    @AppDepartment NVARCHAR(255),
    @AppComments NVARCHAR(255),
    @AppCriticality NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Insert into WindowsCluster if not exists (if you want to maintain existing)
        IF NOT EXISTS (SELECT 1 FROM WindowsCluster WHERE WinClusterID = @WinClusterID)
        BEGIN
            INSERT INTO WindowsCluster (WinClusterID, WinClusterIP, WinClusterName)
            VALUES (@WinClusterID, @WinClusterIP, @WinClusterName);
        END

        -- Insert into Node if not exists
        IF NOT EXISTS (SELECT 1 FROM Node WHERE NodeID = @NodeID)
        BEGIN
            INSERT INTO Node (NodeID, NodeIP, NodeName, NodeOSVersion, NodeComments, WinClusterID)
            VALUES (@NodeID, @NodeIP, @NodeName, @NodeOSVersion, @NodeComments, @WinClusterID);
        END

        -- Insert into SQLCluster if not exists
        IF NOT EXISTS (SELECT 1 FROM SQLCluster WHERE SQLClusterID = @SQLClusterID)
        BEGIN
            INSERT INTO SQLCluster (SQLClusterID, SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP)
            VALUES (@SQLClusterID, @SQLClusterIP, @SQLClusterName, @SQLType, @SQLInstanceName, @SQLPort, @SQLServerVersion, @NARsRaised, @SQLComments, @SQLServerEdition, @MSDTCIP);
        END

        -- Insert into Application if not exists
        IF NOT EXISTS (SELECT 1 FROM Application WHERE ApplicationID = @ApplicationID)
        BEGIN
            INSERT INTO Application (ApplicationID, AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality)
            VALUES (@ApplicationID, @AppName, @AppOwner, @AppOwnerEmail, @AppVersion, @AppDepartment, @AppComments, @AppCriticality);
        END

        -- Insert into NodeSQLCluster Join Table
        INSERT INTO NodeSQLCluster (NodeID, SQLClusterID)
        VALUES (@NodeID, @SQLClusterID);

        -- Insert into SQLClusterApplication Join Table
        INSERT INTO SQLClusterApplication (SQLClusterID, ApplicationID)
        VALUES (@SQLClusterID, @ApplicationID);
        
        -- Optional: Return the inserted IDs
        SELECT @WinClusterID AS WinClusterID, @NodeID AS NodeID, @SQLClusterID AS SQLClusterID, @ApplicationID AS ApplicationID;
    END TRY
    BEGIN CATCH
        -- Error handling
        SELECT 
            ERROR_NUMBER() AS ErrorNumber,
            ERROR_MESSAGE() AS ErrorMessage;
        -- You can choose to RAISE or RETURN as needed.
        RETURN;
    END CATCH
END;
