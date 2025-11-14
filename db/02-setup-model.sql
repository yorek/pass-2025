alter database current set compatibility_level = 170
go

--drop external model Text3Small
--drop database scoped credential [https://dm-open-ai-3.openai.azure.com/]
select * from sys.database_scoped_credentials
select * from sys.external_models
go

create database scoped credential [https://ms-open-ai-3.openai.azure.com/]
with 
    identity = 'Managed Identity', 
    secret = '{"resourceid":"https://cognitiveservices.azure.com"}';
go

create external model Text3Small
with ( 
      location = 'https://ms-open-ai-3.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15',
      credential = [https://ms-open-ai-3.openai.azure.com/],
      api_format = 'Azure OpenAI',
      model_type = embeddings,
      model = 'embeddings'
);
go

select top(10)
    cast(AI_GENERATE_EMBEDDINGS(substring([Title] || ' ' || [Description],1, 500) use model Text3Small) as vector(1536))
from
    [dbo].[grant_microsoft]
go