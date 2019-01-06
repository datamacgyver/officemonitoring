USE [environment]
GO
/****** Object:  Table [dbo].[cpu_temp]    Script Date: 06/01/2019 20:10:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[cpu_temp](
	[timestamp] [datetime] NOT NULL,
	[cpu_temp] [decimal](4, 1) NOT NULL,
 CONSTRAINT [PK_cpu_temp] PRIMARY KEY CLUSTERED 
(
	[timestamp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[hivecommands]    Script Date: 06/01/2019 20:10:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[hivecommands](
	[timestamp] [datetime] NOT NULL,
	[command] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_hivecommands] PRIMARY KEY CLUSTERED 
(
	[timestamp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[lastrecorded]    Script Date: 06/01/2019 20:10:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[lastrecorded](
	[timestamp] [datetime] NULL,
	[variable] [varchar](50) NULL,
	[reading] [decimal](4, 1) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[room_humidity]    Script Date: 06/01/2019 20:10:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[room_humidity](
	[timestamp] [datetime] NOT NULL,
	[room_humidity] [decimal](4, 1) NOT NULL,
 CONSTRAINT [PK_room_humidity] PRIMARY KEY CLUSTERED 
(
	[timestamp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[room_temp]    Script Date: 06/01/2019 20:10:44 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[room_temp](
	[timestamp] [datetime] NOT NULL,
	[room_temp] [decimal](4, 1) NOT NULL,
 CONSTRAINT [PK_room_temp] PRIMARY KEY CLUSTERED 
(
	[timestamp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[stub]    Script Date: 06/01/2019 20:10:45 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[stub](
	[timestamp] [datetime] NOT NULL,
	[stub] [decimal](4, 1) NULL,
 CONSTRAINT [PK_stub] PRIMARY KEY CLUSTERED 
(
	[timestamp] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
