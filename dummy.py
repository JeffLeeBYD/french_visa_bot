from playwright.sync_api import Playwright, sync_playwright, expect
import time
import datetime
import utils
import traceback
import pytz

dub_tz = pytz.timezone('Europe/Dublin')

def no_slot_process():
    now = datetime.datetime.now(tz=dub_tz)
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', "a") as file:
        file.write("at " + time_string + ' no slot.\n')

def handle_slot_page(page):
    slot_button = page.query_selector('button:has-text("Validate the calendar")')
    no_slot_text = page.get_by_text("No appointment available for this day")
    # deploy uncomment below
    #slot_button = page.query_selector('button:has-text("Validate the calendar")')
    # test uncomment below
    # slot_button = page.query_selector('button:has-text("Book an appointment")')
    # rubbish below
    #AM_button = page.query_selector('button:has-text("AM")')
    #PM_button = page.query_selector('button:has-text("PM")')
    #slot_button = page.query_selector('button:has-text("confirm")')
    # case that found slots
    #if no_slot_text.is_visible():
    if slot_button is not None and not no_slot_text.is_visible():
        '''now = datetime.datetime.now()
        file_name = now.strftime("%H:%M:%S-%d-%m-%Y") + ".png"
        with open("./results/" + file_name, "wb") as f:
            f.write(screenshot)'''
        box = slot_button.bounding_box()
        y_pos = box["y"]
        if y_pos < 600:
            no_slot_process()
        else:
            screenshot = page.screenshot()
            now = datetime.datetime.now(tz=dub_tz)
            time_stamp = "at " + now.strftime("%Y-%m-%d %H:%M:%S") + " [dublin time]"
            utils.send_message(screenshot, time_stamp)
    else:
        no_slot_process()


# the main func
def run(playwright:Playwright) -> None:
    now = datetime.datetime.now()
    print("\n @ {0} --------- new round ---------".format(now.strftime("%H:%M:%S-%d-%m-%Y")))
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})

    page.goto(
        "https://consulat.gouv.fr/en/ambassade-de-france-en-irlande/appointment?name=Visas")

    image_locator_1 = page.wait_for_selector('img[id="captcha-image"]', state='visible')

    # Capture a screenshot of the image element
    screenshot_buffer = image_locator_1.screenshot()
    result = utils.anti_captcha(screenshot_buffer)
    print("anti_captcha result:", result)

    # submit ocr result
    page.get_by_placeholder("What is the result?").fill(result)
    page.get_by_role("button", name="Access to services").click()

    time.sleep(3)
    
    while page.locator('button[title="Refresh the captcha"]').is_visible():
        page.locator('button[title="Refresh the captcha"]').click()
        time.sleep(7)
        image_locator_2 = page.wait_for_selector('img[id="captcha-image"]', state='visible')

        # Capture a screenshot of the image element
        screenshot_buffer = image_locator_2.screenshot()
        result = utils.anti_captcha(screenshot_buffer)
        print("anti_captcha result:", result)
        # submit ocr result
        page.get_by_placeholder("What is the result?").fill(result)
        page.get_by_role("button", name="Access to services").click()
        time.sleep(3)

    time.sleep(3)
    page.wait_for_selector('button:has-text("To confirm")').click()
    time.sleep(3)
    page.wait_for_selector('label[for="readInformations"]', timeout=60000, state="visible").click()
    page.get_by_role("button", name="Book an appointment").click()
    time.sleep(10)
    print("check check")
    handle_slot_page(page)

    # ---------------------- init complete
    while True:
        page.goto(
        "https://consulat.gouv.fr/en/ambassade-de-france-en-irlande/appointment?name=Visas")
        tick_button_element = page.wait_for_selector('button:has-text("Access to services")', state='visible')
        time.sleep(1)
        tick_button_element.click()
        yes_button_element = page.wait_for_selector('button:has-text("Yes")', state='visible')
        time.sleep(1)
        yes_button_element.click()
        time.sleep(3)
        page.get_by_role("button", name="Book an appointment").click()
        time.sleep(10)
        print("check check")
        handle_slot_page(page)
        time.sleep(55)
    # ---------------------- clear up
    context.close()
    browser.close()


if __name__ == '__main__':
    while True:
        try:
            with sync_playwright() as playwright:
                run(playwright)
        except Exception as error:
            if error == KeyboardInterrupt:
                break
            else:
                print(traceback.format_exc())
