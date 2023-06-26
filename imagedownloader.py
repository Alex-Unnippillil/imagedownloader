import os
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

def save_images(url, folder):
    # Send a GET request to the URL
    response = urlopen(url)
    
    # Read the HTML content
    html_content = response.read().decode('utf-8')
    
    # Find all <img> tags in the HTML
    img_start_tag = '<img'
    img_end_tag = '>'
    img_tags = []
    
    # Find all occurrences of <img> tags in the HTML
    start = 0
    while True:
        img_start_index = html_content.find(img_start_tag, start)
        if img_start_index == -1:
            break
        img_end_index = html_content.find(img_end_tag, img_start_index)
        img_tags.append(html_content[img_start_index:img_end_index+1])
        start = img_end_index + 1
    
    for img_tag in img_tags:
        # Find the source URL of the image
        src_start_tag = 'src="'
        src_end_tag = '"'
        src_start_index = img_tag.find(src_start_tag) + len(src_start_tag)
        src_end_index = img_tag.find(src_end_tag, src_start_index)
        img_url = img_tag[src_start_index:src_end_index]
        
        # Join the image URL with the base URL of the web page
        img_url = urljoin(url, img_url)
        
        # Get the filename from the URL
        img_filename = os.path.basename(urlparse(img_url).path)
        
        # Send a GET request to download the image
        img_response = urlopen(img_url)
        
        # Save the image to the specified folder
        img_path = os.path.join(folder, img_filename)
        with open(img_path, 'wb') as img_file:
            while True:
                chunk = img_response.read(1024)  # Read in chunks of 1024 bytes
                if not chunk:
                    break
                img_file.write(chunk)
        
        print(f'Saved image: {img_filename}')

# Menu with prompts
def menu():
    print("=== Image Downloader ===")
    url = input("Enter the website URL: ")
    folder = input("Enter the folder name to save the images: ")

    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Call the function to save the images
    save_images(url, folder)

# Run the menu
menu()
