from src.mp_app.services.manage_drivers.chrome_driver import ChromeDriver
from src.mp_app.services.manage_actions.facebook_action import FacebookAction

if __name__ == "__main__":
    chrome_driver_instance = ChromeDriver({"profile-directory": "Profile 1"})
    facebook_action_instance = FacebookAction(chrome_driver_instance)
    facebook_action_instance.comment_newfeed(
        "https://www.facebook.com/", " like", [r"C:\Users\ADMIN\Downloads\download.jpg"]
    )
    # chrome_driver_instance.health_check()
    # print(chrome_driver_instance.profile_name)
