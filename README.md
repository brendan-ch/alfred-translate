# Alfred-Translate

An Alfred workflow that translates text using Google Translate. Results appear directly in Alfred, so there is no need to open the Google Translate website.

## Setup

You must have a Google Account to use this workflow.

1. Go to https://console.cloud.google.com/projectcreate and create a new project.
2. Go to https://console.cloud.google.com/apis/library/translate.googleapis.com. On the top left, make sure the project you just created is selected. Then, click "Enable".
3. Go to https://console.cloud.google.com/apis/credentials and click "Create credentials" near the top left. In the dropdown menu, select "API key". Then, copy the API key.
4. Once your API key has been created, you may import the workflow and use the keyword "gtset" to set the API key.

## Usage

- `gt [text]`: Translate text using the Google Translate API.
- `gtset [source?] [target]`: Quickly set source and target language codes. The [source] argument is optional; if only one language is entered, only the target will be set.
- `gtsource [source?]`: Filter through languages to use as the source. Leave [source] blank to set source to automatic.
- `gttarget [target]`: Filter through languages to use as the target.
- `gtkey`: Set the API key used by Google Cloud Platform.