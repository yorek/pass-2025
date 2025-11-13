select count(*) from [dbo].[grant_microsoft_chunks] where EmbeddingText3Small is null

select format(count(*),'n0') 
from [dbo].[grant_microsoft_chunks] 
