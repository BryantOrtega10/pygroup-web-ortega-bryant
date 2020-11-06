'''
    Es posible devolver la salida de una función vinculada a una determinada URL en forma de HTML.
    Sin embargo, generar contenido HTML a partir del código Python es engorroso, especialmente cuando 
    es necesario colocar datos variables y elementos del lenguaje Python como condicionales o bucles. 
    Aquí es donde se puede aprovechar el motor de plantillas Jinja2, en el que se basa Flask. 
    En lugar de devolver HTML de código rígido desde la función, la función render_template ()
    puede generar un archivo HTML. Flask intentará encontrar el archivo HTML en la carpeta de "templates",
    en la misma carpeta en la que está presente este script.

    El término "sistema de plantillas web" se refiere al diseño de un script HTML en el que los datos variables
    se pueden insertar de forma dinámica. Un sistema de plantillas web consta de un motor de plantillas, 
    algún tipo de fuente de datos y un procesador de plantillas.
    Flask utiliza el motor de plantillas jinja2. Una plantilla web contiene marcadores de posición intercalados 
    de sintaxis HTML para variables y expresiones que son valores reemplazados cuando se representa la plantilla.

    El motor de plantillas jinja2 utiliza los siguientes delimitadores para escapar de HTML.
    {% ...%} para declaraciones
    {{...}} para que las expresiones se impriman en la salida de la plantilla
    {# ... #} para comentarios no incluidos en la salida de la plantilla
    # ... ## para declaraciones de línea
    
    Fuente: https://www.tutorialspoint.com/flask/flask_templates.htm
'''