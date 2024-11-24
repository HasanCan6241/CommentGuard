# YouTube CommentGuard

**YouTube CommentGuard** is a web-based application that automatically classifies YouTube comments into categories such as Neutral, Insult/Hate Speech, Sexism, and Racism. This project uses the **Hugging Face "nanelimon/bert-base-turkish-bullying"** model for Turkish text classification. It aims to enhance content moderation by identifying harmful comments and providing a cleaner, safer environment for users.

![Project Banner]([https://example.com/path/to/your/image.png](https://cdn.prod.website-files.com/623952e7f678f72edd96fd42/64af90e5414541a57da1edc0_How%20NLP%20is%20being%20used%20to%20keep%20Youtube%20comments%20safe.svg))  <!-- You can replace this with your actual banner image path -->

## Features

- **Home Page**: A brief introduction to the project and its functionality.
- **YouTube Analysis Page**: Users can input YouTube video links to extract comments, video titles, descriptions, and images. The system then classifies the comments into one of the predefined categories.
- **YouTube Search Page**: Displays a list of previously analyzed videos, showing detailed information about each video, including the comments, comment authors, and classification results.
  
## Technologies Used

- **Django**: A powerful web framework for building web applications, handling user authentication, and database interactions.
- **Transformers**: Hugging Face library used to leverage pre-trained models like BERT for sentiment analysis and comment classification.
- **google-api-python-client**: Used to interact with the YouTube API to fetch video data such as comments, titles, and images.

## Usage

- **Register/Login**: Users need to register and log in to access the analysis pages.
- **YouTube Analysis**: Paste a YouTube video URL to fetch and analyze comments. The comments will be classified into one of the following categories:
  - Neutral
  - Insult/Hate Speech
  - Sexism
  - Racism
- **YouTube Search**: View previously analyzed videos, with detailed information about each comment, author, and classification.

## Screenshots

### Home Page
<img src="images/Anasayfa.png" alt="Anasayfa" width="850" height="400"/>

### YouTube Analysis Page
<img src="images/youtube-analiz.png" alt="Youtube Analiz" width="850" height="400"/>

### YouTube Search Page
<img src="images/video-search.png" alt="Video Search" width="850" height="400"/>

### Video Details
<img src="images/video-detail.png" alt="Video Detail" width="850" height="400"/>


## Contributing

Contributions are welcome! If you want to improve or add new features, feel free to fork this repository and submit a pull request.

Please follow the guidelines below when contributing:
- Ensure that your code follows PEP 8 style guidelines.
- Write unit tests for new features.
- Provide clear commit messages.

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/HasanCan6241/YouTube-CommentGuard.git
   cd YouTube-CommentGuard