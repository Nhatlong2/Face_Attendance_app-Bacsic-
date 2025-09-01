DELETE FROM dbo.Attendance;
DBCC CHECKIDENT ('dbo.Attendance', RESEED, 0);

DELETE FROM dbo.Faces;
DBCC CHECKIDENT ('dbo.Faces', RESEED, 0);

DELETE FROM dbo.Users;
DBCC CHECKIDENT ('dbo.Users', RESEED, 0);