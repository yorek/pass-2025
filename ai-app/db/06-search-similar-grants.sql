-- Return all the relevant grants given the provided search text
create procedure dbo.SearchSimilarGrants
@SearchText nvarchar(max)
as

declare @qv vector(1536) = AI_GENERATE_EMBEDDINGS(@SearchText use model Text3Small);
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
		top_n = 50
	) as vs
inner join
	[dbo].[grant_microsoft] g on c.GrantID = g.GrantID
order by
	Distance
go

-- Usage sample
execute dbo.SearchSimilarGrants 'similar image identification using approximate nearest neighbor to find duplicate photos' 
