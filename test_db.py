from taskflow.app.users.repositories.users import create_user, get_user_by_id

# user = create_user(
#     username="fardad",
#     email="fardad@test.com",
#     password="fardad123"
# )

# print("user has created successfully!")

get_user = get_user_by_id(
    user_id="1"
)

print("here is", get_user)