-- Run 
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