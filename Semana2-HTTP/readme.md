# Tipos de peticiones HTTP más usados
### GET
El método GET  solicita una representación de un recurso específico. 
Las peticiones que usan el método GET sólo deben recuperar datos.
### POST
El método POST se utiliza para enviar una entidad a un recurso en específico, causando a menudo un cambio en el estado o efectos secundarios en el servidor.
### PUT
El modo PUT reemplaza todas las representaciones actuales del recurso de destino con la carga útil de la petición.
### DELETE
El método DELETE borra un recurso en específico.
### PATCH
El método PATCH es utilizado para aplicar modificaciones parciales a un recurso.

Tomado de: [Métodos de petición HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Methods)

# Códigos de respuesta HTTP más comunes
### 200
OK: El código de respuesta 200 indica que la solicitud ha sido procesada correctamente. 
### 301
Moved Permanently: El código 301 significa que los datos solicitados por el cliente ya no se encuentran bajo la misma dirección de Internet, sino que han sido desplazados de manera permanente.
### 302
Moved Temporarily: Informa que los datos solicitados están disponibles temporalmente en una dirección diferente.
### 403
Forbidden: Indica al cliente que los datos solicitados están protegidos y, por ende, se le ha denegado el acceso debido a la falta de autorización del cliente.
### 404 
Not Found: Cuando el servidor envía el código 404 como respuesta significa que no fue posible encontrar los datos de la página web solicitada en el servidor.
### 500 
Internal Server Error: Este tipo de respuesta actúa como un código de estado colectivo para un error inesperado en el servidor.
### 503
Service Unavailable: Este código de respuesta indica que el servidor web destinado a proporcionar la información está sobrecargado.