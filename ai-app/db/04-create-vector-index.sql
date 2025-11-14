select * from sys.database_scoped_configurations
go

-- needed during Public Preview
alter database scoped configuration set maxdop = 16
go

-- 16vCore Hyperscale: ~30 minutes
create vector index ixv 
on [dbo].[grant_microsoft_chunks](EmbeddingText3Small)
with (
	metric = 'cosine', 
	type='DiskANN'
)

