def upload_to_gcs(project, src_file, dst_bucket, dst_blob_name, make_public=True):
    from google.cloud import storage
    client = storage.Client(project=project)
    # https://console.cloud.google.com/storage/browser/[bucket-id]/
    bucket = client.get_bucket(dst_bucket)
    b = bucket.blob(dst_blob_name)
    b.upload_from_filename(filename=src_file)
    b.cache_control = 'no-cache, max-age=0'  # change cache control
    if make_public:
        b.make_public()
    return 0
