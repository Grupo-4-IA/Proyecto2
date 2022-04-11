from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from time import sleep
from selenium import webdriver

class Producto() : 
    def __init__(self, nombre, precio, imagen, mercado) :
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen
        self.mercado = mercado

    def __gt__ (self, Producto) : 
        return self.precio > Producto.precio

@api_view(['GET'])
def returnProducts (request) : 
    productos = [] 
    sleep(8)
    driver = webdriver.Chrome('./chromedriver.exe')
    busqueda = request.GET.get('objetoBuscado', None)
    ###########################################
    #Amazon
    driver.get('https://www.amazon.com/')
    #Solicitar la busqueda
    buscadorAmazonTextBox = driver.find_element_by_id('twotabsearchtextbox')
    buscadorAmazonTextBox.send_keys(busqueda)
    sleep(5)
    buscadorAmazonBoton= driver.find_element_by_id('nav-search-submit-button')
    buscadorAmazonBoton.click()
    sleep(10)


    # Recolectar informacion
    for i in range(5):
        try : 
            nombreProductoAmazonText = driver.find_element_by_xpath('//div[@data-component-type="s-search-result"]['+str(i+1)+']//h2/a/span')
            precioEnteroProductoAmazonText= driver.find_element_by_xpath('//div[@data-component-type="s-search-result"]['+str(i+1)+']//span[@class="a-price-whole"]')
            precioFraccionProductoAmazonText= driver.find_element_by_xpath('//div[@data-component-type="s-search-result"]['+str(i+1)+']//span[@class="a-price-fraction"]')
            imagenProductoAmazoniImg= driver.find_element_by_xpath('//div[@data-component-type="s-search-result"]['+str(i+1)+']//img')

            nombreProductoAmazon= nombreProductoAmazonText.text
            precioProductoAmazon= float(precioEnteroProductoAmazonText.text) + (float(precioFraccionProductoAmazonText.text)/100)
            urlImagenProductoAmazon = imagenProductoAmazoniImg.get_attribute('src')

            productos.append(Producto(nombreProductoAmazon, precioProductoAmazon, urlImagenProductoAmazon, "../../assets/icon/amazon.svg"))

        except :
            print("No existe un elemento de esta clase")

    sleep(8)

    #OLX
    driver.get('https://www.olx.com.ec/')
    #Solicitar la busqueda
    buscadorOLXTextBox = driver.find_element_by_xpath('//input[@data-aut-id="searchBox"]')
    buscadorOLXTextBox.send_keys(busqueda)
    sleep(5)

    buscadorOLXBoton= driver.find_element_by_xpath('//div[@data-aut-id="btnSearch"]')
    buscadorOLXBoton.click()

    sleep(20)

    # Recolectar informacion
    for i in range(5):
        try: 
            nombreProductoOLXText = driver.find_element_by_xpath('//div//ul//li['+str(i+1)+']//a//div//span[@data-aut-id="itemTitle"]')
            precioEnteroProductoOLXText= driver.find_element_by_xpath('//div//ul//li['+str(i+1)+']//a//div//span[@data-aut-id="itemPrice"]')
            imagenProductoOLXImg= driver.find_element_by_xpath('//div//ul//li['+str(i+1)+']//a//figure//img')

            nombreProductoOLX= nombreProductoOLXText.text
            precioProductoOLX= precioEnteroProductoOLXText.text
            urlImagenProductoOLX = imagenProductoOLXImg.get_attribute('src')

            precioProductoOLX = float(precioProductoOLX[2:].replace(',', '.'))

            productos.append(Producto(nombreProductoOLX, precioProductoOLX, urlImagenProductoOLX, "../../assets/icon/olx.svg"))

        except: 
            print("No existe un elemento de esta clase")

    #Ebay
    driver.get('https://www.ebay.com/')
    #Solicitar la busqueda
    buscadorOLXTextBox = driver.find_element_by_xpath('//input[@aria-label="Buscar artículos"]')
    buscadorOLXTextBox.send_keys(busqueda)
    sleep(5)

    buscadorOLXBoton= driver.find_element_by_xpath('//input[@value="Buscar"]')
    buscadorOLXBoton.click()

    sleep(20)

    # Recolectar informacion
    for i in range(5):
        try: 
            nombreProductoEbayText = driver.find_element_by_xpath('//div//ul//li['+str(i+1)+']//div//div//h3')
            precioEnteroProductoEbayText= driver.find_element_by_xpath('//div//ul//li['+str(i+1)+']//div//div//div//div//span[@class="s-item__price"]')
            imagenProductoEbayImg= driver.find_element_by_xpath('//div//ul//li['+str(i+1)+']//div//div//div//a//div//img')

            nombreProductoEbay= nombreProductoEbayText.text
            precioProductoEbay= precioEnteroProductoEbayText.text
            urlImagenProductoEbay = imagenProductoEbayImg.get_attribute('src')

            precioProductoEbay = float(precioProductoEbay[4:])

            productos.append(Producto(nombreProductoEbay, precioProductoEbay, urlImagenProductoEbay, "../../assets/icon/ebay.svg"))
        except:
            print("No existe un elemento de esta clase")

        data = []

        list.sort(productos) 

        for product in productos : 
            data.append({
                "nombre" : product.nombre,
                "precio" : product.precio,
                "imagen" : product.imagen,
                "mercado" : product.mercado
            })

    return JsonResponse(data, safe=False)


# Create your views here.

@api_view(['GET'])
def prueba(request): 
    print("Entre al get")
    frase = request.GET.get('prueba', None)
    data = {
        "respuesta": frase
    }
    return JsonResponse(data)

