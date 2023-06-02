from unittest.mock import patch

import pytest
import requests

from exceptions import ImageDownloadError
from image_downloader import get_image, download_images_from_file


@pytest.fixture(scope="module")
def dummy_image(tmp_path_factory):
    content = b"dummy image data"
    file_path = tmp_path_factory.mktemp("images") / "dummy_image.jpg"
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path


def test_get_image_success(tmp_path, dummy_image):
    url = "http://test.com/valid_image.jpg"
    output_path = tmp_path / "image.jpg"

    with open(dummy_image, "rb") as f:
        expected_content = f.read()

    with pytest.raises(ImageDownloadError):
        get_image(url, str(output_path))

    response_mock = requests.models.Response()
    response_mock.status_code = 200
    response_mock.raw = dummy_image.open("rb")
    response_mock.iter_content = lambda chunk_size: iter(lambda: response_mock.raw.read(chunk_size), b"")

    with patch("image_downloader.requests.get", return_value=response_mock):
        result = get_image(url, str(output_path))

    assert result is True
    assert output_path.exists()

    with open(output_path, "rb") as f:
        assert f.read() == expected_content


def test_get_image_failure(tmp_path):
    url = "http://test.com/invalid_image.jpg"
    output_path = tmp_path / "image.jpg"

    with pytest.raises(ImageDownloadError):
        get_image(url, str(output_path))

    response_mock = requests.models.Response()
    response_mock.status_code = 404

    with patch("image_downloader.requests.get", return_value=response_mock):
        with pytest.raises(ImageDownloadError):
            get_image(url, str(output_path))

    assert not output_path.exists()


def test_get_images_from_file(tmp_path, dummy_image):
    file_content = [
        "http://test.com/dummy_image1.jpg\n",
        "http://test.com/dummy_image2.jpg\n",
        "http://test.com/dummy_image3.jpg\n",
    ]

    file_path = tmp_path / "input.txt"
    file_path.write_text("".join(file_content))

    images_dir = tmp_path / "images_dir"
    images_dir.mkdir()

    expected_output_paths = []

    for url in file_content:
        url = url.strip()
        if url:
            file_name = url.rsplit("/", maxsplit=1)[-1]
            expected_output_path = images_dir / file_name
            expected_output_paths.append(expected_output_path)

    with patch("image_downloader.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.raw = dummy_image.open("rb")
        mock_response.iter_content = lambda chunk_size: iter(lambda: mock_response.raw.read(chunk_size), b"")

        download_images_from_file(str(file_path), str(images_dir))

    for output_path in expected_output_paths:
        assert output_path.exists()

    for output_path in expected_output_paths:
        output_path.unlink()

    images_dir.rmdir()
    file_path.unlink()
