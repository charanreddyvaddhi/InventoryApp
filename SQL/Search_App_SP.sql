USE [Inv]
GO

/****** Object:  StoredProcedure [dbo].[Search_App]    Script Date: 09-11-2024 01:13:40 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE PROCEDURE [dbo].[Search_App]
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold results
    CREATE TABLE #SearchResults (
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
    INSERT INTO #SearchResults (ApplicationID,AppName,AppOwner,AppOwnerEmail,AppVersion,AppDepartment,AppComments,AppCriticality)
	SELECT ApplicationID,AppName,AppOwner,AppOwnerEmail,AppVersion,AppDepartment,AppComments,AppCriticality  from [dbo].[Application]
    WHERE
		AppName LIKE '%' + @SearchTerm + '%'
		OR AppOwner LIKE '%' + @SearchTerm + '%'
		OR AppComments LIKE '%' + @SearchTerm + '%'
		OR AppCriticality LIKE '%' + @SearchTerm + '%'
		OR AppVersion LIKE '%' + @SearchTerm + '%'
		OR AppDepartment LIKE '%' + @SearchTerm + '%'

    -- Return the results
    SELECT * FROM #SearchResults;

    -- Clean up
    DROP TABLE #SearchResults;
END;
GO


