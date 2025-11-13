select * from sys.database_scoped_configurations
go

alter database scoped configuration set maxdop = 16
go

create vector index ixv 
on [dbo].[grant_microsoft_chunks](EmbeddingText3Small)
with (
	metric = 'cosine', 
	type='DiskANN'
)

-- 30 minutes