# DateApp
Date app.

When the user enters the site sees the log-in form. If he has an account he can log in, otherwise he will need to register(there is a button for it below). 

![изображение](https://user-images.githubusercontent.com/72472295/119332393-2e6b5d00-bc91-11eb-984e-939d615bd3f4.png)

On the registration page the user needs to enter his username, name, e-mail, gender, city, country, date of birth and password. Also he needs to select a gender of the person he is looking for. Then he can log in.

![изображение](https://user-images.githubusercontent.com/72472295/119333007-07f9f180-bc92-11eb-8b72-6206080fbe3a.png)

When a user logs in he goes to his profile page. Here he can write a description for his profile, choose the desired age range, gender (female, male, or not important), place (his city, country or the whole world). Also here he can upload a photo for his profile if he clicks on the upload photo button. 

![изображение](https://user-images.githubusercontent.com/72472295/119334170-74c1bb80-bc93-11eb-848a-de272ef91fcd.png)

On the photo upload page, he can select the photos he wants to upload.

![изображение](https://user-images.githubusercontent.com/72472295/119336292-28c44600-bc96-11eb-9314-095027b0b36a.png)

When the user has selected the desired photos, he must click the green button to upload a photo.

![изображение](https://user-images.githubusercontent.com/72472295/119335968-afc4ee80-bc95-11eb-8858-6e62232420c7.png)

All photos uploaded by the user appear on this page, here he can delete them. Maximum user can have 8 photos. 

![изображение](https://user-images.githubusercontent.com/72472295/119336068-cbc89000-bc95-11eb-9514-ac7875c2c2c3.png)

In the "people" tab, the profiles of other users are displayed, which you can skip or like. After any of these actions, the profile will no longer be displayed in this tab. But it will appear again in a day if the profile is skipped. If you like the profile and there is no mutual like within a week, the like will be reset and the profile will be displayed again. Celery is userd for this.

![изображение](https://user-images.githubusercontent.com/72472295/119642119-10cdfd00-be23-11eb-897b-3ef39b8e36d5.png)

In case of mutual likes:
1) Both users receive notifications 

![изображение](https://user-images.githubusercontent.com/72472295/119649344-2e9f6000-be2b-11eb-80ee-561fb74a2042.png)

2) The user is added to the "matches" tab

![изображение](https://user-images.githubusercontent.com/72472295/119649446-5262a600-be2b-11eb-8fc0-625126a2954a.png)

3) A chat is created between the users.

![изображение](https://user-images.githubusercontent.com/72472295/119649550-6e664780-be2b-11eb-8e48-c97add426496.png)


