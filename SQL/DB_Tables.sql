USE [Inv]
GO
/****** Object:  Table [dbo].[Application]    Script Date: 26-10-2024 18:40:49 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Application](
	[ApplicationID] [int] NOT NULL,
	[AppName] [varchar](255) NULL,
	[AppOwner] [nvarchar](255) NULL,
	[AppOwnerEmail] [nvarchar](255) NULL,
	[AppVersion] [nvarchar](255) NULL,
	[AppDepartment] [nvarchar](255) NULL,
	[AppComments] [nvarchar](255) NULL,
	[AppCriticality] [nchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[ApplicationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Node]    Script Date: 26-10-2024 18:40:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Node](
	[NodeID] [int] NOT NULL,
	[NodeIP] [varchar](15) NULL,
	[NodeName] [varchar](255) NULL,
	[NodeOSVersion] [varchar](255) NULL,
	[NodeComments] [varchar](255) NULL,
	[WinClusterID] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[NodeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[NodeSQLCluster]    Script Date: 26-10-2024 18:40:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[NodeSQLCluster](
	[NodeID] [int] NOT NULL,
	[SQLClusterID] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[NodeID] ASC,
	[SQLClusterID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SQLCluster]    Script Date: 26-10-2024 18:40:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SQLCluster](
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
PRIMARY KEY CLUSTERED 
(
	[SQLClusterID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SQLClusterApplication]    Script Date: 26-10-2024 18:40:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SQLClusterApplication](
	[SQLClusterID] [int] NOT NULL,
	[ApplicationID] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[SQLClusterID] ASC,
	[ApplicationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[WindowsCluster]    Script Date: 26-10-2024 18:40:50 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[WindowsCluster](
	[WinClusterID] [int] NOT NULL,
	[WinClusterIP] [varchar](15) NULL,
	[WinClusterName] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[WinClusterID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Node]  WITH CHECK ADD FOREIGN KEY([WinClusterID])
REFERENCES [dbo].[WindowsCluster] ([WinClusterID])
GO
ALTER TABLE [dbo].[NodeSQLCluster]  WITH CHECK ADD FOREIGN KEY([NodeID])
REFERENCES [dbo].[Node] ([NodeID])
GO
ALTER TABLE [dbo].[NodeSQLCluster]  WITH CHECK ADD FOREIGN KEY([SQLClusterID])
REFERENCES [dbo].[SQLCluster] ([SQLClusterID])
GO
ALTER TABLE [dbo].[SQLClusterApplication]  WITH CHECK ADD FOREIGN KEY([ApplicationID])
REFERENCES [dbo].[Application] ([ApplicationID])
GO
ALTER TABLE [dbo].[SQLClusterApplication]  WITH CHECK ADD FOREIGN KEY([SQLClusterID])
REFERENCES [dbo].[SQLCluster] ([SQLClusterID])
GO
