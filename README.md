# OAuth2, OpenID, SAML Authentication

|                       | OAuth2  | OpenID | SAML | 
|----------------       | ------------- |-------------|-------------|
|Significado siglas     | Open authorization     |Open identification             |Security Assertion Markup Language|
|Para que se usan       | Envío continuo de credenciales entre cliente y servidor.| Iniciar sesión en distintos sitios web, sin la necesidad<br> de crear varias cuentas en cada sitio, sino una sola en<br>OpenID la cual es aceptada como cuenta en los distintos<br>sitios web|Es un estándar abierto basado en XML que combina<br>las propiedades de los dos estándares comentados<br>anteriormente. Se trata, por lo tanto, de **un estándar<br>de autenticación y de autorización.**|
|Qué es                 | Es un estándar abierto para la autorización de APIs,<br> que nos permite **compartir información entre sitios <br>sin tener que compartir la identidad.** |Es un estándar para autentificación, que permite a los<br>usuarios mantener una única cuenta (un único nombre<br> de usuario y password), y usar esta única cuenta en varios<br>sitios Web, sin necesidad de registrarse en cada sitio por<br>separado. |Es un estándar de código abierto basado en XML para<br>el intercambio de datos de autentificación y autorización.<br> Está formado por varios componentes que aportan todas<br>las funciones necesarias para definir y transmitir información<br> de forma segura|
|Como funciona          | Delega la capacidad de realizar ciertas acciones, no todas,<br> a las cuales da su consentimiento para hacerlas en su<br> nombre, sin necesidad de compartir sus datos de acceso. <br><br>De esta forma **no tenemos por qué almacenar el nombre de <br>usuario y contraseña del cliente.**     | Un usuario puede identificarse en una página web a través<br>de una URL (o un XRI en la versión actual) y puede ser <br>verificado por cualquier servidor que soporte OpenID,<br>los usuarios no tienen que crearse una nueva cuenta de<br>usuario para obtener acceso. En su lugar, solo necesitan<br>disponer de un identificador creado en un servidor que<br> verifique OpenID, llamado proveedor de identidad.<br><br>El proveedor de identidad puede confirmar la identificación<br> OpenID del usuario al sitio que soporte este sistema y que<br>confíe en él.|Una aserción SAML puede incluir una o más declaraciones<br>o statements sobre las propiedades (identidad, atributos)<br>y los permisos de un usuario. El responsable de crearla es<br>el proveedor de identidad correspondiente, que utiliza XML<br>como lenguaje de marcado. Cada aserción recibe una firma<br>digital, que primero tiene que ser comprobada y verificada<br>por la aplicación pertinente. De esta forma, es posible<br>garantizar la integridad y autenticidad de la aserción, que<br>recibe el nombre, una vez firmada, de token SAML. <br><br>Después de realizar la verificación, el proveedor de servicios<br>analiza el contenido concreto y luego decide si otorga o no<br>acceso al usuario y en caso afirmativo, qué tipo de acceso<br>otorga.|

### Fuentes
* [Qué es OAuth 2](https://openwebinars.net/blog/que-es-oauth2/)

* [Oauth y su versión Oauth2](https://www.ionos.es/digitalguide/servidores/seguridad/oauth-y-su-version-oauth2/)

* [OpenID](http://tejedoresdelweb.com/w/OpenID)

* [¿En qué se diferencian SAML, OpenID y OAuth?](https://inza.wordpress.com/2014/10/17/en-que-se-diferencian-saml-openid-y-oauth/)

* [SAML](https://www.ionos.es/digitalguide/servidores/seguridad/saml/)

