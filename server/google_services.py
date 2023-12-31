from google.cloud import storage
import sys


def upload_blob(video_file, video_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket("dss-bucket")
    blob = bucket.blob(destination_blob_name)

    if __name__ == "__main__":
      video_file = open(video_file, "rb")

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_file(video_file, if_generation_match=generation_match_precondition)
  
    return f"https://storage.googleapis.com/dss-bucket/videos/{video_name}"

def get_blobs():
  storage_client = storage.Client()
  bucket = storage_client.bucket("dss-bucket")
  blobs = bucket.list_blobs(max_results=100)
  for blob in blobs:
    yield blob.name

if __name__ == "__main__":
    upload_blob(*sys.argv[1:])
    print("it worked!")

