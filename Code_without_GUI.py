import instaloader
import os

def fetch_profile_info():
    L = instaloader.Instaloader()

    try:
        username=input("Enter the username: ")
        password=input("Enter the password: ")

        L.login(username, password)

        profile = instaloader.Profile.from_username(L.context, username)
        
        print("Username:", profile.username)
        print("Number of Posts:", profile.mediacount)
        print("Followers Count:", profile.followers)
        print("Following Count:", profile.followees)
        print("Bio:", profile.biography)
        print("External URL:", profile.external_url)
        
        L.download_profile(profile.username, profile_pic_only=False)

        followers = profile.get_followers()
        followers_list = [follower.username for follower in followers]

        followees = profile.get_followees()
        followees_list = [followee.username for followee in followees]

        with open('followers_list.txt', 'w') as f:
            for follower in followers_list:
                f.write(f"{follower}\n")

        with open('followees_list.txt', 'w') as f:
            for followee in followees_list:
                f.write(f"{followee}\n")

        print("Followers and following lists have been saved to files.")


    except instaloader.exceptions.ProfileNotExistsException:
        print("Profile does not exist.")
    except instaloader.exceptions.ConnectionException:
        print("Network issue or Instagram is down.")
    except instaloader.exceptions.LoginRequiredException:
        print("Login required or login credentials are incorrect.")
    except instaloader.exceptions.InstaloaderException as e:
        print(f"An error occurred: {e}")

def option_two():
    import instaloader

    L = instaloader.Instaloader()
    username=input("Enter the username: ")

    profile = instaloader.Profile.from_username(L.context, username)

    print("Username:", profile.username)

    print("Number of Posts:", profile.mediacount)

    print("Followers Count:", profile.followers)
    print("Following Count:", profile.followees)

    print("Bio:", profile.biography)

    print("External URL:", profile.external_url)

    L.download_profile(profile.username, profile_pic_only=False)


def main():
    print("Choose an option:")
    print("1. Both username & password: ")
    print("2. Only username: ")

    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        fetch_profile_info()
    elif choice == '2':
        option_two()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()