import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# Configuración del navegador (sin headless para verlo en acción)
def configurar_navegador():
    opciones = Options()
    opciones.add_argument("--start-maximized")  # Abre el navegador en pantalla completa
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option("useAutomationExtension", False)

    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)

    return webdriver.Chrome(service=service, options=opciones)


# Función para buscar productos en Amazon
def buscar_amazon(producto, paginas=1):
    navegador = configurar_navegador()
    url_base = "https://www.amazon.com.mx"

    # Acceder a la página principal
    navegador.get(url_base)
    time.sleep(10)

    #Buscar el producto en la barra de búsqueda
    search_bar = navegador.find_element(By.ID, "twotabsearchtextbox")
    search_bar.send_keys(producto)
    search_bar.submit()
    time.sleep(3)

    productos = []

    #Iterar sobre las páginas de resultados
    for pagina in range(paginas):
        time.sleep(3)
        soup = BeautifulSoup(navegador.page_source, "html.parser")

        # Extraer productos de la página
        resultados = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in resultados:
            nombre = item.find("span", class_="a-size-medium")
            precio = item.find("span", class_="a-price-whole")
            rating = item.find("span", class_="a-icon-alt")
            entrega = item.find("span", class_="a-text-bold")

            productos.append({
                "Nombre": nombre.text.strip() if nombre else "Sin nombre",
                "Precio": f"${precio.text.strip()}" if precio else "No disponible",
                "Rating": rating.text.strip() if rating else "Sin calificación",
                "Entrega": entrega.text.strip() if entrega else "No especificado"
            })

        #Intentar ir a la siguiente página
        try:
            siguiente_pagina = navegador.find_element(By.LINK_TEXT, "Siguiente")
            siguiente_pagina.click()
            print(f"✅ Avanzando a la página {pagina + 2}...")
            time.sleep(5)
        except:
            print("⚠️ No hay más páginas disponibles.")
            break

    navegador.quit()

    #Guardar en un DataFrame y exportar a CSV
    df = pd.DataFrame(productos)
    df.to_csv(f"{producto.replace(' ', '_')}_amazon.csv", index=False, encoding="utf-8")

    return df


#Ejecución
if __name__ == "__main__":
    busqueda = "Samsung S24"
    paginas_a_buscar = 2  # Puedes cambiar el número de páginas
    df_resultado = buscar_amazon(busqueda, paginas_a_buscar)
    print(df_resultado)












#SI LLEGO HASTA ACA "HOLA Y YA ANDO CANSADO PERO MOTIVADO PARA SEGUIR CON ESTO"
