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


## Kostenreduzierung in Bezug zu der KI


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

Ideas for other fields:


**Agent**
Agent oder in anderen Wort eine Person mit bestimmten Skill, also nicht Person X, sondern eine Person die X kann.
Möglicherweise eine Messung in der Form. Der Agent kann X 9/10 gut, Y 4/10 gut, ... oder halt sowas wie IT-Profi Steuerberater

**Verfügbare Agenten** / **Liste an Agenten mit zugeordneten Tickets** 
In ZUsammenarbeit mit dekm Agent Feld, welche Agenten zum Zeitpunkt der Ticket Ersteööung, wie viele zugeordnete Tickets hatten

**Bearbeitungszeit**
Wie lange es ungefähr dauert das Ticket zu bearbeiten. Kann helfen damit hervorsagen darüber zu tätigen, wie lange es dauert bis ein Ticket bearbeitet wird.


**Zeit bis zur Fertigstellung**
Wie viele Zeit vom erstellen des Tickets bis zur Lösung vergangen ist. Ebenso:

**Zeit bis zur ersten Antwort**
**Zeit bis zu Status X** ...


**Status** Also ob das Ticket gelöst wurde oder nicht.

**Bounces** Wie oft das Ticket an jemand anderen weitergeleitet wurde.

**FAQ Resource bzw. Dokumentation Seite X war relevant**

**Kundenbenutzer** welcher das Ticket erstellt hat.
Mit jetzigemr Pipeline schwierig. Da zuerst Priorität Queue und Typ festgelegt werden. Obwohl man kann es auch so machen, das ein Kundenbenutzer ausgewählt wird jenachdem welche QUeue oder Typ gewählt wurde.

Es wäre nämlich sonst unlogisch, wenn es keine Korrelation zwischen dem Kundenbenutzer und den Queues geben würde.

**Agent Bearbeiter ID**
Umsetzung ist ziemlich einfach. Nachdem die Ticket Email im Ticketsystem ankommt. Entscheidet ChatGPT, welcher Agent das Ticket bearbeiten soll.
Dann könnt es halt auch wirklich so einen gewisses Skill Level von einem Agenten geben.

**Kundenzufriedenheit**
Ob Kunde zufrieden ist mit dem Ticket. Umsetzung wäre auch ziemlich einfach. ChatGPT fragen wie gut die Antwort ist und dann vielleicht auch noch Lösungszeit mit einbeziehen.

**Anzahl Kundennachrichten**

**Anzahl Agenten nachrichten**

**Anzahl Kundenanrufe**

**Communication Channel**
Umsetzung wäre nicht so extrem schwierig. Einach beim generieren der Nachricht den KOmmunikationskanal angeben. Bei Telefon, berichtet der Agent über einen erhaltenen Anruf.
Oder es ist ein internes Ticket

**Aufteilung des Kunden zu einen Status**

****


