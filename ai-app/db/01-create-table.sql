set statistics time on
go

select count(*) from [dbo].[grant_microsoft]
go

alter database scoped configuration set PREVIEW_FEATURES = on
go

drop table if exists dbo.grant_microsoft_chunks;
create table dbo.grant_microsoft_chunks
(
	Id int not null primary key identity,
	GrantID nvarchar(20) not null,
	ChunkID int not null,
	TextChunk nvarchar(1100),
	EmbeddingText3Small vector(1536)
)
go

insert into 
	dbo.grant_microsoft_chunks (GrantID, ChunkID, TextChunk)
select 
	GrantID,
	chunk_order as ChunkID,
	chunk as TextChunk
from 
	[dbo].[grant_microsoft] as g
cross apply
	ai_generate_chunks(source = [Title] || ' ' || [Description], chunk_type = fixed, chunk_size = 1000, overlap = 10) as c
go

-- Make sure there aren't empty embeddings
delete from
[dbo].[grant_microsoft_chunks] 
where EmbeddingText3Small is null 
or trim(EmbeddingText3Small) = ''
go

-- Count total chunks
select format(count(*),'n0') 
from [dbo].[grant_microsoft_chunks] 
go