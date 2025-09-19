from django.shortcuts import render, HttpResponse 

def hello(request):
    return HttpResponse("""
                        <!DOCTYPE>
                        <head>
                        </head>
                        <body>
                            <a href="/1">loo</a>
                            <p style="color: red;"> oooh nooo </p>
                        </body>
        """)

def loo(request):
    return HttpResponse("""
                        <!DOCTYPE>
                        <head>
                        </head>
                        <body>
                            <p style="color: green;"> oooh nooo </p>
                        </body>
        """)
