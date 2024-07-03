import json
from openai import OpenAI


def fetch_location_name(openai_client: OpenAI, image_url: str):
    print(f"Fetching location name for image URL: {image_url}")
    completion = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Which location is this? Give me the locations name only in the response except any of the texts.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
    )
    response = completion.choices[0].message.content
    print(f"Received location name: {response}")
    return response


def process_tours(data, openai_client):
    openai_destinations_list = []
    cdns_list = []
    for tour in data:
        print(
            f"\nProcessing Tour ID: {tour['tour_id']}\nTour Name: {tour['tour_name']}"
        )
        for image in tour["images"]:
            location_name = fetch_location_name(openai_client, image["url"])
            image["location_name"] = location_name
            openai_destinations_list.append(location_name)
            cdns_list.append(image["url"])
        print(f"Updated tour images with location names for Tour ID: {tour['tour_id']}")

        # Save the updated tour data to a file
        with open(f"updated_tour_{tour['tour_id']}.json", "w") as f:
            json.dump(tour, f, indent=2)
        print(f"Updated data for Tour ID: {tour['tour_id']} saved successfully.")
    return openai_destinations_list, cdns_list


if __name__ == "__main__":
    openai_client = OpenAI(api_key="api_key")
    print("Loading tours data from proto_tours.json")
    with open("proto_tours.json", "r") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} tours from proto_tours.json")

    print("Processing tours to fetch location names for images...")
    openai_destinations_list, cdns_list = process_tours(data, openai_client)

    print("Processing completed. All tours data have been updated and saved.")
