from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from dotenv import load_dotenv

from Inchcape.Automatizaciones.config import DatosTicket  

load_dotenv("./Variables.env")

print("Iniciando con solicitante:", DatosTicket.get("NOMBRE_SOLICITANTE"))

def click_with_retry(navegador, selector, max_retries=3, timeout=30):
    for attempt in range(max_retries):
        try:
            elem = WebDriverWait(navegador, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            elem.click()
            return
        except StaleElementReferenceException:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.5)

def GeneradorTicket():
    options = Options()
    options.add_argument(r"--user-data-dir=C:\Users\miguel.tunjano\Desktop\EdgeSeleniumProfile")
    options.add_argument("--profile-directory=Profile1")
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "stylesheet": 2,
            "media_stream": 2
        }
    }
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = "eager"


    navegador = webdriver.Edge(options=options)
    
    navegador.set_window_size(1280, 720)

    navegador.get("https://servicedesk.inchcapedigital.com/app/gbsdesk/ui/requests/add?reqTemplate=138622000009249572")

    requester_select = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_requester > a.select2-choice"))
    )
    requester_select.click()

    search_input = WebDriverWait(navegador, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body .select2-drop-active input.select2-input"))
    )
    search_input.send_keys(DatosTicket.get("NOMBRE_SOLICITANTE"))
    WebDriverWait(navegador, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body .select2-drop-active ul li.select2-highlighted"))
    )
    search_input.send_keys(Keys.RETURN)

    impact_select = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_impact > a.select2-choice"))
    )
    impact_select.click()
    impact_input = WebDriverWait(navegador, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.impact.select2-drop-active input.select2-input"))
    )
    impact_input.send_keys(DatosTicket.get("IMPACTO"))
    WebDriverWait(navegador, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.impact.select2-drop-active ul li.select2-highlighted"))
    )
    impact_input.send_keys(Keys.RETURN)

    urgency_select = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_urgency > a.select2-choice"))
    )
    urgency_select.click()
    urgency_input = WebDriverWait(navegador, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.urgency.select2-drop-active input.select2-input"))
    )
    urgency_input.send_keys(DatosTicket.get("URGENCIA"))
    WebDriverWait(navegador, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.urgency.select2-drop-active ul li.select2-highlighted"))
    )
    urgency_input.send_keys(Keys.RETURN)

    americas_select = WebDriverWait(navegador, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_udf_fields-udf_char190 > a.select2-choice"))
    )
    americas_select.click()
    americas_input = WebDriverWait(navegador, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char190.select2-drop-active input.select2-input"))
    )
    americas_input.send_keys(DatosTicket.get("CIUDAD_DE_IMPACTO"))
    WebDriverWait(navegador, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char190.select2-drop-active ul li.select2-highlighted"))
    )
    americas_input.send_keys(Keys.RETURN)

    click_with_retry(navegador, "#s2id_udf_fields-udf_char187 > a.select2-choice")
    if(DatosTicket.get("CIUDAD_DE_IMPACTO") == "Colombia"):
        compania_select = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_udf_fields-udf_char716 > a.select2-choice"))
        )
        compania_select.click()
        compania_input = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char716.select2-drop-active input.select2-input"))
        )
        compania_input.send_keys("Inchcape")
        WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char716.select2-drop-active ul li.select2-highlighted"))
        )
        compania_input.send_keys(Keys.RETURN)

        click_with_retry(navegador, "#s2id_udf_fields-udf_char187 > a.select2-choice")
        cat_input = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char187 input.select2-input"))
        )
        cat_input.send_keys(DatosTicket.get("CATEGORIA"))
        cat_input.send_keys(Keys.RETURN)

        click_with_retry(navegador, "#s2id_udf_fields-udf_char188 > a.select2-choice")
        subcat_input = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char188 input.select2-input"))
        )
        subcat_input.send_keys(DatosTicket.get("SUBCATEGORIA"))
        subcat_input.send_keys(Keys.RETURN)

        click_with_retry(navegador, "#s2id_udf_fields-udf_char189 > a.select2-choice")
        items_input = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.udf_fields-udf_char189 input.select2-input"))
        )
        items_input.send_keys(DatosTicket.get("ITEMS"))
        items_input.send_keys(Keys.RETURN)

        try:
            WebDriverWait(navegador, 30).until(
                lambda d: "-- Select Group --" not in d.find_element(
                    By.CSS_SELECTOR, "#s2id_group .select2-chosen"
                ).text.strip()
            )
            print("Auto-fill de group detectado")
        except TimeoutException:
            print("No se detectó cambio en group después de items (posiblemente ya estaba seteado)")

        site_select = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_site > a.select2-choice"))
        )
        site_select.click()
        site_input = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.site.select2-drop-active input.select2-input"))
        )
        site_input.send_keys(DatosTicket.get("SITIO"))
        WebDriverWait(navegador, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.site.select2-drop-active ul li.select2-result"))
        )
        site_input.send_keys(Keys.RETURN)

        group_select = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#s2id_group > a.select2-choice"))
        )
        group_select.click()

        group_input = WebDriverWait(navegador, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.group.select2-drop-active input.select2-input"))
        )

        navegador.execute_script("""
            arguments[0].value = '';
            arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
            arguments[0].dispatchEvent(new Event('change', {bubbles:true}));
        """, group_input)

        group_input.send_keys(DatosTicket.get("GRUPO"))

        WebDriverWait(navegador, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.select2-drop.group.select2-drop-active ul li.select2-highlighted"))
        )

        group_input.send_keys(Keys.RETURN)

        try:
            WebDriverWait(navegador, 10).until(
                lambda d: DatosTicket.get("GRUPO").lower() in d.find_element(
                    By.CSS_SELECTOR, "#s2id_group .select2-chosen"
                ).text.strip().lower()
            )
            print("Group OK:", navegador.find_element(By.CSS_SELECTOR, "#s2id_group .select2-chosen").text.strip())
        except TimeoutException:
            print("¡Alerta! Group fue reseteado después de selección")

        temaTicket = navegador.find_element(By.ID, "subject")
        temaTicket.clear()
        temaTicket.send_keys(DatosTicket.get("TITULO_TEMA"))
            
        texto = (
            DatosTicket.get("DESCRIPCION", "")
        )

        iframe = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#htmleditor_description iframe.ze_area"))
        )
        navegador.switch_to.frame(iframe)

        body = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        acciones = ActionChains(navegador)
        acciones.move_to_element(body).click().perform()
        body.clear()
        body.send_keys(texto)

        navegador.switch_to.default_content()

        time.sleep(2)
        
        submit_btn = WebDriverWait(navegador, 30).until(
            EC.element_to_be_clickable((By.ID, "submit-btn"))
        )
        navegador.execute_script("""
            let el = arguments[0];
            while (el && el.scrollHeight <= el.clientHeight) {
                el = el.parentElement;
            }
            if (el) {
                el.scrollTop = arguments[0].offsetTop;
            }
        """, submit_btn)


        ActionChains(navegador)\
            .move_to_element(submit_btn)\
            .pause(0.2)\
            .click_and_hold()\
            .pause(0.1)\
            .release()\
            .perform()