import shelve

def test_file_creation():
    try:
        with shelve.open("test_file.db") as db:
            db["test"] = "This is a test."
            print("Test file created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

test_file_creation()
