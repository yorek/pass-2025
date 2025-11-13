set statistics time on
go

select count(*) from [dbo].[grant_microsoft]
go

alter database scoped configuration set PREVIEW_FEATURES = on

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

set nocount on
while (1=1)
begin
	update top(50)
		[dbo].[grant_microsoft_chunks]
	set
		EmbeddingText3Small = AI_GENERATE_EMBEDDINGS(TextChunk use model Text3Small)
	where
		EmbeddingText3Small is null
	option (maxdop 1)

	if (@@ROWCOUNT = 0) begin return end
end


declare @qv vector(1536) = AI_GENERATE_EMBEDDINGS(
	'similar image identification using approximate nearest neighbor to find duplicate photos' 
	use model Text3Small);
select top(50)
	g.Title,
	c.GrantId, ChunkId, TextChunk,
	VECTOR_DISTANCE('cosine', @qv, EmbeddingText3Small) as Distance
from 
	[dbo].[grant_microsoft_chunks] c
inner join
	[dbo].[grant_microsoft] g on c.GrantID = g.GrantID
where
	 EmbeddingText3Small is not null
order by
	Distance
go


declare @qv vector(1536) = AI_GENERATE_EMBEDDINGS(
	'similar image identification using approximate nearest neighbor to find duplicate photos' 
	use model Text3Small);
select top(50)
	g.GrantID,
	g.Title,
	vs.Distance
from
	vector_search(
		table = [dbo].[grant_microsoft_chunks] as c,
		column = EmbeddingText3Small,
		similar_to = @qv,
		metric = 'cosine',
		top_n=50
	) as vs
inner join
	[dbo].[grant_microsoft] g on c.GrantID = g.GrantID
order by
	Distance
