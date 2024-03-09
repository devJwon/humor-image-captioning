import os
import pandas as pd
import random
import json
from dotenv import load_dotenv
import logging
import httpx
import base64
import anthropic

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the ANTHROPIC_API_KEY in the .env file.")

def fetch_and_encode_image(url):
    response = httpx.get(url, follow_redirects=True)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        logging.error(f"Failed to fetch image from {url}")
        return None

def load_image_data_from_csvs(csv_file_paths):
    data_frames = []
    for csv_file_path in csv_file_paths:
        df = pd.read_csv(csv_file_path)
        data_frames.append(df)
    combined_data = pd.concat(data_frames, ignore_index=False, axis=1)
    return combined_data

def shuffle_captions(row):
    captions = [row['real_caption'], row['random_caption'], row['description']]
    random.shuffle(captions)
    return captions

def get_image_caption(client, image_data, captions, language='en'):
    prompt = f"""
[Task] Select the most humorous caption related to the provided image. The chosen caption should humorously describe the image and be relevant to its context.

[Instructions]
- Evaluate the humor of each provided caption.
- Ensure the caption is directly related to the image.
- Avoid captions that merely describe the image without humor.
- Choose the caption that is most humorous and relevant.

[Output Format]
Return the chosen caption in JSON format: {{selected caption number:'caption text'}}.

[captions]
1: {captions[0]}
2: {captions[1]}
3: {captions[2]}

[Choose the most humorous caption]
    """ if language == 'en' else f"""
[과제] 제공된 이미지와 관련된 가장 재미있는 제목을 선택합니다. 선택한 제목은 이미지를 유머러스하게 설명해야 하며 이미지의 맥락과 관련이 있어야 합니다.

[지침]
- 제공된 각 제목의 유머를 평가합니다.
- 제목이 이미지와 직접 관련이 있는지 확인합니다.
- 유머 없이 단순히 이미지를 설명하는 제목은 피하세요.
- 가장 유머러스하고 관련성이 높은 제목을 선택하세요.

[출력 형식]
선택한 제목을 JSON 형식으로 반환합니다: {{'제목 번호':'제목 텍스트'}}.

[제목]
1: {captions[0]}
2: {captions[1]}
3: {captions[2]}

[가장 재미있는 제목]
    """   
    try:
        # Assuming the client can handle base64 encoded images directly; adjust as necessary.
        response = client.messages.create(
            model="claude-3-opus-20240229",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        logging.info(f"Sending request to Anthropic with base64 encoded image and captions: {captions}")
        print(response.content)
        response_text = response.content[0].text
        logging.info("Received response from Anthropic")
        logging.info(f"Response: {response_text}")
        return response_text
    except Exception as e:
        logging.error(f"Error processing image. Error: {e}")
        return json.dumps({"error": str(e)})

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Use your anthropic client initialization here
    client = anthropic.Anthropic(api_key=api_key)  # Adjusted to use the Anthropics client with an API key
    error_rows = []
    logging.info("Loading image data from CSV files...")
    csv_file_paths = ['data/pilot2/kor_0.csv', 'data/pilot2/kor_1.csv', 'data/pilot2/kor_2.csv', 'data/pilot2/kor_3.csv']
    combined_data = load_image_data_from_csvs(csv_file_paths)
    combined_data[['caption1', 'caption2', 'caption3']] = combined_data.apply(lambda row: pd.Series(shuffle_captions(row)), axis=1)
    
    results_dir = 'result'
    os.makedirs(results_dir, exist_ok=True)
    results_file_path = os.path.join(results_dir, 'claude_Ko_response_texts.csv')
    
    logging.info(f"Processing images for humor evaluation...")
    for index, row in combined_data.iterrows():
        logging.info(f"Processing image {index + 1}/{len(combined_data)}...")
        image_data = fetch_and_encode_image(row['url'])
        if image_data:
            captions = [row['caption1'], row['caption2'], row['caption3']]
            response_text = get_image_caption(client, image_data, captions, 'ko')
            if "error" not in response_text:
                combined_data.at[index, 'response_text'] = response_text
            else:
                error_rows.append(index)
                logging.error(f"Error processing row {index}: {response_text}")
        else:
            error_rows.append(index)
            logging.error(f"Error fetching or encoding image for row {index}")

    combined_data.to_csv(results_file_path, index=False, encoding='utf-8')
    logging.info(f"Responses have been saved to {results_file_path}")
    if error_rows:
        logging.error(f"Errors occurred in the following rows: {error_rows}")

if __name__ == "__main__":
    main()
