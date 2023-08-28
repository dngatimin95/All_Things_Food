# All Things Food: Revolutionizing Dining Exploration

Discovering new dining spots around the world is an exciting adventure, but the process of saving and sharing these places can be time-consuming and cumbersome. I used to go through the manual process of saving places I found on Google Maps, which took quite abit of time from having to search for the place, ensure that it was correct and then saving it to a list. To address this, I wanted to find a way that simplifies the way I save, organize, and recommend dining locations. Thus, this project was born.

## So what does this repo do?
This repository focuses on developing my understanding of APIs and backend capabilities by creating a user-friendly API. Its primary purpose is to enable users to effortlessly save and retrieve places they're interested in visiting. Users will also be able to prioritze the place they want to visit as well. Powered by basic CRUD operations, the API seamlessly interacts with a MongoDB Atlas Cloud instance. The user interface is a Telegram bot that facilitates easy input and retrieval of stored locations.

## So how does it work?
1. User Interaction: Users engage with the Telegram bot to input place names and set priority scores for their visits.
2. Automatic Enrichment: The project interfaces with the Google Maps API to extract essential information about the saved places, including name, address, URL, and restaurant type.
3. Data Storage: Information will be sent to the API and MongoDB Atlas Cloud instance stores all place-related data, ensuring secure and organized storage.
4. Location Queries: Users can retrieve saved places based on priority and proximity (To Be Built).

## Why MongoDB? Why not PostgresSQL?
Instead of opting for traditional relational databases like PostgresSQL, I chose MongoDB for its NoSQL capabilities. This choice was motivated by a desire to explore dynamic schemas and adaptability to unstructured data. MongoDB's compatibility with Flask APIs and its flexibility further solidified its suitability for the project.

## So what's next to do?
- [ ] Understand how to use Docker and dockerize appl so that it can be used in other environments
- [ ] Build the proximity and recommendation aspect of this list
