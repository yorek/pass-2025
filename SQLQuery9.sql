

insert into 
	dbo.grant_microsoft_chunks (GrantID, ChunkID, TextChunk, EmbeddingText3Small)
select 
	GrantID,
	chunk_order as ChunkID,
	chunk as TextChunk,
	AI_GENERATE_EMBEDDINGS(c.TextChunk use model Text3Small) as EmbeddingText3Small
from 
	[dbo].[grant_microsoft] as g
cross apply
	AI_GENERATE_CHUNKS(
		source = [Title] || ' ' || [Description], 
		chunk_type = fixed, 
		chunk_size = 1000, 
		overlap = 10
	) as c
go


