# Dataset Version 3

## Overview
The completely new idea regarding the new dataset version is: Using Chatbots to generate an output which is again used as input.
So that there is a graph structure of chatbots which give there ouput as input to another chatbot.
The architecture is designed to be easily extendable.

## Architecture
The architecture is a pipeline with a shared context. Value Objects are passed on in the chain.
Then there are chatbots which use Value Objects as an input and creaate or modify the Value Objects. 
But Value Objects are also merged into Aggregates/Composite Value Objects.
Also there are multiple Random Generators, that use Input/Output Distribution Tables to generate a random output.

## Fields/Features
- subject
- text
- ticket type (NEW)
- priority
- queue
- first answer (NEW)
- language (meta data)
subcategory is removed from before

The 3 priorities will stay the same. Likely this will not change soon. I think 3 priorities is enough.
The only think that might make sense is to have a 2d priority: Urgency and Importance. But this is not needed for now.

Of course there could also be spam mails, but I think most mail clients already have a spam filter. So this is not needed.

But for queues, with the new architecture the plan is that the queues should be easily extandable.
For the kaggle data I think 10 queues would be a good amount.

The ticket type is a new feature. This is the type of the ticket. This could be a question, a problem, a feature request, etc.
There will be 4 types for now.

Also there is a new approach for the subject and text. The core text and subject generator will stay the same, but
the subject and text of the ticket will then be rewritten again. Always using the same base text but different instructions.
I think using 8 different instructions should work. Then these instructions will also be translated into different languages.

Hopefully this will make the texts more diverse, while also reducing the costs, by using gpt-4o mini for the rewriting and translating.

Then this text and subject will be given as input to chatgpt assistant that acts as a Customer Agent. Writing the first answer to the ticket.
So this is like a first level support. In the future maybe there will be iterations of user and agent adding text.

The costs for this should be about 8x the costs of the original text generation. Before it was like 4€/1k tickets now it should be 0.50cts for 1k tickets.


### Easily Extendable

The number of queues, the number of ticket types, the number of languages should be easily adoptable.

Easy to add ticket attributes are: company type, Ticket Tags/Categories, Timestamp information.



## Ideas

Subject, Text, Customer Name, CustomerID, Type of Day, Time of Day, Queue, Priority, Agent, Sub-Category, Type, Language, Product Name 

Maybe:
IP Adress or Location?
Channel (Email, Phone, Chat, etc)
Extra Customer Data like, amount previous tickets, average priority. list of previous tickets.


What company is the ticket system for??

Or is it like from multiple companies. If its from a lot of companies then there will be so many agents,
that the agent doesnt really make sense.
Ot