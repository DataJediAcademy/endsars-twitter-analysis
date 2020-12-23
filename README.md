# #EndSARS Twitter Analysis
Sentiment and Network Analysis of the #EndSARS protest movement that occured in October 2020 in Nigeria.

## Brief
You just got hired as a data scientist at the Soro Soke initiative International, an organization focused on promoting equality and enforcing human rights.

The team is excited to have a data scientist on board and eager to see what can be done with the vast amount of data they currently have access to. The team is particularly very interested in the recent Endsars movement. A week after your resumption, you get a mail from your boss with the following details:

> Hello,
> 
> Welcome on board... We believe the #EndSARS movement is one of the most powerful movements in Africa over the last two decades. We want to quantify this impact and need your help with doing analysis to answer some of these questions:
>
> - What locations was the hashtag popular?
> - How far did the hashtag reach and how deep was this reach?
> - When the did movement start on social media? When did it reach critical mass?
> - What were the most popular words or terms used during the movement?
> - Who were the key influences and proponents involved in the movement?
>   - What was the most popular tweet?
> - What is the general sentiment of the tweets about the movement? How has this changed from the start of the movement till now?
> - Were there any bots or bad actors spreading fake news around the movement?
>   - What are some examples of this fake news?
> 
> Apart from these questions, if you could use your initiative to also do more analysis and come up with more inisghts then that would be even better.
>
> Please provide us with a visual report with the insights above

### Tools and Technologies
- Plotly Dash for visualization and automated reports.
- Python
- Natural Language Processing (NLP).
- Network Analysis.

### Tasks
- Create a dashboard we can use to explore the answers to the questions in the brief.
- Scrape tweets related to the movement using [Twitters API](https://developer.twitter.com/en)
- Create a sentiment analysis algorithm trained on the tweets you've collected.
- Use network analysis to determine the relationship between tweeters to help locate a fake news factory.

### Deliverables
- Dashboard where a user can interact with the data.
- Inisghtful commentary based on your findings.

### Additional Tasks (compulsory for Data/ML Engineers but optional for Data Scientists)

- Use a pre-trained language model and modify it to work with Tweets using Naija Slang and emojis. (**for ML Engineers**)
- Turn the custom sentiment analysis model into an API.
- Test your API using Postman.
- Integrate the Models API into the Dash App so a user can post a tweet and get a sentiment score.
- Deploy the model and the Dash app on a cloud server using docker.


### Additional Deliverables (compulsory for Data/ML engineers but optional for data scientists)
- Sentiment Analysis Model that recognises nuances of naija slangs and emojis. (**for ML Engineers**)
- Dash app where a user can interact with the data and post a tweet which it classifies live. 


