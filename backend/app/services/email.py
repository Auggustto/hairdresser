import smtplib
import email.message
from flask import jsonify


def send_email(user_email, verification_code):
    try:
        body_email = """
        <style>
            /* Estilos comuns para os cards */
            .secao4 {
                margin: 0;
                font-family: Helvetica, sans-serif;
            }

            .secao4-div {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 30px;
                text-align: center;
            }

            .secao4-div-card {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: calc(100% / 3 - 60px);
                margin: 10px;
                padding: 30px;
                border-radius: 15px;
                background-color: white;
                transition: all 0.5s ease;
                border: 0.005rem solid #6b6b6b2c;

                -webkit-box-shadow: 9px 7px 5px rgba(50, 50, 50, 0.77);
                -moz-box-shadow: 9px 7px 5px rgba(50, 50, 50, 0.77);
                box-shadow: 9px 7px 5px rgba(50, 50, 50, 0.77);
            }

            .secao4-div-card:hover {
                transform: scale(1.1);
                z-index: 1;
            }

            .secao4-div-card img {
                width: 35%;
                height: auto;
            }

            .secao4-div-card h3 {
                margin-bottom: 0px;
            }

            /* Estilos para dispositivos móveis */
            @media (max-width: 768px) {
                .secao4-div-card {
                    width: 100%;
                }
            }

            body {
                background: rgb(255, 255, 255);
            }
        </style>



        <!-- Seção com cards -->

        <body>
            <section class="secao4" id="sobre">
                <div class="secao4-div">
                    <!-- Card 1 -->
                    <div class="secao4-div-card">
                        <h1>Recuperação de acesso</h1>
                        <h4>Código de Recuperação</h4>
                        <p>Olá, o seu e-mail de recuperação de senha chegou!</p>
                        <h3>""" + verification_code + """</h3>
                    </div>
                </div>
                </div>
            </section>
        </body>
        """

        msg = email.message.Message()
        msg['Subject'] = "Recuperação de senha"
        msg['From'] = 'automaticrobo001@gmail.com'
        msg['To'] = user_email
        password = 'urpgucutnucepbjc'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(body_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        return jsonify({"message": "E-mail sent sucessfully!"}), 200
    
    except Exception as e:

        return jsonify({"error": str(e)})