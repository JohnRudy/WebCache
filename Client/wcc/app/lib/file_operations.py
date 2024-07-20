from app.webcache_client.schema import File  # type: ignore


def get_file_schema(filepath: str) -> File:
    file_name = filepath.split("/")[-1]
    with open(filepath, "rb") as f:
        return File(name=file_name, content=f.read().decode())


def place_content_into_file(file: File) -> None:
    with open(file.name, "wb") as f:
        f.write(file.content.encode())
