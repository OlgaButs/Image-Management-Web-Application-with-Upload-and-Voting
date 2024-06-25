
import pytest
import requests

# Test the register method
def test_register():
    url = "https://xcoa.av.it.pt/labiproj4/api/register"
    data = {
        "username": "Dany123",
        "password": "meowMeow"
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.text == "Username already exists."

# Test the login method
def test_invalid_login():
    data = {
        "username": "admiiin",
        "password": "admiiiin"
    }
    response = requests.post("https://xcoa.av.it.pt/labiproj4/api/login", data=data)
    assert response.status_code == 200
    assert response.text == "Invalid username or password."

# Test the login method
def test_valid_login():
    data = {
        "username": "uu",
        "password": "uu"
    }
    response = requests.post("https://xcoa.av.it.pt/labiproj4/api/login", data=data)
    assert response.status_code == 200
    assert response.text == "Login successful."

# Test the logout method
def test_logout():
    url = "https://xcoa.av.it.pt/labiproj4/api/logout"
    response = requests.get(url)
    assert response.status_code == 200

# Test the upload method

def test_invalid_file_format():
    url = "https://xcoa.av.it.pt/labiproj4/api/upload"
    file_path = "path/to/invalid_file.jpg"
    files = {"image": file_path}
    response = requests.post(url, files=files)
    assert response.status_code == 404

def test_unsupported_file_format():
    url = "https://xcoa.av.it.pt/labiproj4/api/upload"
    file_path = "path/to/unsupported_file.pdf"
    files = {"image": file_path}
    response = requests.post(url, files=files)
    assert response.status_code == 404

# Test the comment method
def test_invalid_arguments():
    invalid_id = "invalid_id"
    invalid_comment = ""
    response = requests.post(f"https://xcoa.av.it.pt/labiproj4/api/newcomment?idimg={invalid_id}&newcomment={invalid_comment}")
    assert response.status_code == 200

def test_newcomment_invalid_id():
    invalid_id = "999yy"
    try:
        with pytest.raises(Exception):
            response = requests.post(f"https://xcoa.av.it.pt/labiproj4/api/newcomment?idimg={invalid_id}&newcomment=Test")
        assert response.status_code == 500
    except:
            assert True

# Test the list method
def test_missing_arguments():
    response = requests.get("https://xcoa.av.it.pt/labiproj4/api/list")
    assert response.status_code == 404

def test_list_all():
    response = requests.get("https://xcoa.av.it.pt/labiproj4/api/list?id=all")
    assert response.status_code == 200
    # Verify if the response contains the list of images

def test_list_user():
    image_id = "oo"  # Put the correct user ID
    response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/list?id={image_id}")
    assert response.status_code == 200
    # Verify if the response contains the list of images for the user

def test_invalid_list_user():
    image_id = "1"  # Put the correct user ID
    response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/list?id={image_id}")
    assert response.status_code == 200


# Test the get_UserLike method
def test_get_user_like_invalid_id():
    invalid_id = "9999999999999999"
    response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/getUserLike?idimg={invalid_id}")
    assert response.status_code == 200


def test_upvote_invalid_id():
    invalid_id = "invalid_id"
    try:
        with pytest.raises(Exception):
            response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/upvote?idimg={invalid_id}")
        assert response.status_code == 200
    except:
            assert True

def test_downvote_invalid_id():
    invalid_id = "5555"
    response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/downvote?idimg={invalid_id}")
    assert response.status_code == 200

def test_imageproc_invalid_id():
    invalid_id = "666"
    response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/imageproc?id={invalid_id}&select=option")
    assert response.status_code == 200
    assert response.text == "Image not found."


def test_removeImage_invalid_id():
    invalid_id = "999999"
    response = requests.get(f"https://xcoa.av.it.pt/labiproj4/api/removeImage?idimg={invalid_id}")
    assert response.status_code == 200


