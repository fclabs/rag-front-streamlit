## System Performance

### Retrieval accuracy and relevance

### LLM response quality

### System latency and efficiency

## Ethical considerations and mitigation strategies for your system.

## Suggest future improvements or features for the assistant.
### RAG

* Current implementation only support similarity searches. Searcg could be improved by using an hybrid searches, that combine similarity and metadata.
* The system uses a calcualted id based on fielname and chuck. This could be improved by using a hash of the file content, so it performs better on docuemnt updates. 

### Chat with History

* Short-term memory is stored in the session state. This could be improved by using a database to store the memory, so it can be used in different sessions across differente servers.
* Long-term memory could be added to the system, so it can store information for longer periods of time, using summarization to keep updated information from past sessions without storing the whole conversation.

### Tuneable model

* Multi-model support could be added to the system, so it can use different models from different vendor for different tasks.