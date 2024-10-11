CREATE PROCEDURE InsertOrMapData
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

    DECLARE @NewWinClusterID INT;
    DECLARE @NewNodeID INT;
    DECLARE @NewSQLClusterID INT;
    DECLARE @NewApplicationID INT;

    -- Check and Insert or Map Windows Cluster
    IF EXISTS (SELECT 1 FROM WindowsCluster WHERE WinClusterID = @WinClusterID)
    BEGIN
        SET @NewWinClusterID = @WinClusterID;  -- Use existing ID
    END
    ELSE
    BEGIN
        INSERT INTO WindowsCluster (WinClusterID, WinClusterIP, WinClusterName)
        VALUES (@WinClusterID,@WinClusterIP, @WinClusterName);
        
        SET @NewWinClusterID = SCOPE_IDENTITY();  -- Get the new ID
    END

    -- Check and Insert or Map Node
    IF EXISTS (SELECT 1 FROM Node WHERE NodeID = @NodeID)
    BEGIN
        SET @NewNodeID = @NodeID;  -- Use existing ID
    END
    ELSE
    BEGIN
        INSERT INTO Node (NodeID,NodeIP, NodeName, NodeOSVersion, NodeComments, WinClusterID)
        VALUES (@NodeID,@NodeIP, @NodeName, @NodeOSVersion, @NodeComments, @NewWinClusterID);
        
        SET @NewNodeID = SCOPE_IDENTITY();  -- Get the new ID
    END

    -- Check and Insert or Map SQL Cluster
    IF EXISTS (SELECT 1 FROM SQLCluster WHERE SQLClusterID = @SQLClusterID)
    BEGIN
        SET @NewSQLClusterID = @SQLClusterID;  -- Use existing ID
    END
    ELSE
    BEGIN
        INSERT INTO SQLCluster (SQLClusterID,SQLClusterIP, SQLClusterName, SQLType, SQLInstanceName, SQLPort, SQLServerVersion, NARsRaised, SQLComments, SQLServerEdition, MSDTCIP)
        VALUES (@SQLClusterID ,@SQLClusterIP, @SQLClusterName, @SQLType, @SQLInstanceName, @SQLPort, @SQLServerVersion, @NARsRaised, @SQLComments, @SQLServerEdition, @MSDTCIP);
        
        SET @NewSQLClusterID = SCOPE_IDENTITY();  -- Get the new ID
    END

    -- Check and Insert or Map Application
    IF EXISTS (SELECT 1 FROM Application WHERE ApplicationID = @ApplicationID)
    BEGIN
        SET @NewApplicationID = @ApplicationID;  -- Use existing ID
    END
    ELSE
    BEGIN
        INSERT INTO Application (ApplicationID,AppName, AppOwner, AppOwnerEmail, AppVersion, AppDepartment, AppComments, AppCriticality)
        VALUES (@ApplicationID, @AppName, @AppOwner, @AppOwnerEmail, @AppVersion, @AppDepartment, @AppComments, @AppCriticality);
        
        SET @NewApplicationID = SCOPE_IDENTITY();  -- Get the new ID
    END

    -- Insert into the join table Node_SQLCluster
    IF NOT EXISTS (SELECT 1 FROM NodeSQLCluster WHERE NodeID = @NewNodeID AND SQLClusterID = @NewSQLClusterID)
    BEGIN
        INSERT INTO NodeSQLCluster (NodeID, SQLClusterID)
        VALUES (@NodeID, @SQLClusterID);
    END

    -- Insert into the join table SQLCluster_Application
    IF NOT EXISTS (SELECT 1 FROM SQLClusterApplication WHERE SQLClusterID = @NewSQLClusterID AND ApplicationID = @NewApplicationID)
    BEGIN
        INSERT INTO SQLClusterApplication (SQLClusterID, ApplicationID)
        VALUES (@SQLClusterID, @ApplicationID);
    END

    PRINT 'Data inserted/mapped successfully into all tables.';
END;
