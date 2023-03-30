# Website and UI for AIRS (Artificial Intelligence in Respiratory Sounds)

## Key contents
- Requirements
  - User
  - Website
- Frontend
- Backend

## Requirements for the user
The following conditions should be followed by users when submitting the recordings - 

- The website will be operated only using a mobile phone or on a laptop device with external mic connected to it. 
- The permission to record audio sound should be provided when prompted. 
- There will be at least three cough recordings that should be recorded.
 

## Requirements for the website
The following requirements should be taken care of when creating the website - 

- Handle atleast 75 concurrent users at the same time. (A total of 15 centers will be used for recording)
- Password protected credentials for each institute, with at max 10 users being able to login using the credentials.
- Each entry in the website should have a unique ID associated with it (UUID). 
- Upload images and audio recordings to aws s3.

## Frontend Specifications
The following things will be present in the UI-

- Three pages where 
  - First page will contain a form with the details present in the [form](https://forms.gle/HonWpr7G3j7SMu8cA) 
  - Second page will record audio for various sounds
  - Third page will collect image proofs of the diagnosis
- A unique key will be associated to each form (By using patient ID and center ID)

The three sections of UI will look as follows

#First page
