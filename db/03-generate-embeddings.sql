-- Generate Embeddings (may take long time depending on throttling)
set nocount on
while (1=1)
begin
	update top(50)
		[dbo].[grant_microsoft_chunks]
	set
		EmbeddingText3Small = AI_GENERATE_EMBEDDINGS(TextChunk use model Text3Small)
	where
		EmbeddingText3Small is null
	option (maxdop 1) -- needed during Public Preview

	if (@@ROWCOUNT = 0) begin return end
end


